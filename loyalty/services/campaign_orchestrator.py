"""
Campaign Orchestrator Service

Handles campaign triggering, condition evaluation, and execution orchestration.
Integrates with CampaignActionExecutor for action processing.
"""

from django.db import transaction
from django.utils import timezone
from datetime import timedelta
import logging
import random

from loyalty.models import (
    LoyaltyCampaign,
    LoyaltyCampaignExecution,
    LoyaltyMember,
    LoyaltySegment
)

logger = logging.getLogger(__name__)


class CampaignOrchestrator:
    """
    Orchestrates campaign triggering and execution.

    Responsibilities:
    - Trigger campaigns based on events
    - Evaluate trigger conditions
    - Create campaign executions
    - Schedule multi-step journeys
    - Handle A/B test variant assignment
    """

    def trigger_event(self, event: str, member: LoyaltyMember, context: dict = None):
        """
        Trigger all active campaigns for a specific event.

        Args:
            event: Event type (e.g., 'order_placed', 'birthday')
            member: LoyaltyMember instance
            context: Additional context data (order_id, etc.)

        Returns:
            dict: Summary of triggered campaigns
        """
        if context is None:
            context = {}

        logger.info(f"Triggering event '{event}' for member {member.id}")

        # Find active campaigns for this event
        campaigns = LoyaltyCampaign.objects.filter(
            campaign_type=LoyaltyCampaign.TYPE_TRIGGER,
            trigger_event=event,
            is_active=True,
            status=LoyaltyCampaign.STATUS_ACTIVE
        ).prefetch_related('target_tiers')

        triggered_count = 0
        skipped_count = 0
        results = []

        for campaign in campaigns:
            # Check if campaign is within date range
            if not campaign.is_currently_active():
                logger.debug(f"Campaign {campaign.id} not currently active (date range)")
                skipped_count += 1
                continue

            # Check if campaign can trigger for this member
            if not campaign.can_trigger_for_member(member):
                logger.debug(f"Campaign {campaign.id} cannot trigger for member {member.id}")
                skipped_count += 1
                continue

            # Evaluate trigger conditions
            if not self.evaluate_trigger_conditions(campaign, context):
                logger.debug(f"Campaign {campaign.id} conditions not met")
                skipped_count += 1
                continue

            # A/B test variant assignment
            if campaign.is_ab_test:
                # Random assignment based on split percentage
                if random.randint(1, 100) > campaign.ab_split_percentage:
                    logger.debug(f"Campaign {campaign.id} A/B test excluded member")
                    skipped_count += 1
                    continue

            # Execute campaign (async via Celery)
            try:
                result = self.execute_campaign(campaign, member, context)
                results.append(result)
                triggered_count += 1
                logger.info(f"Campaign {campaign.id} triggered for member {member.id}")
            except Exception as e:
                logger.error(f"Failed to trigger campaign {campaign.id}: {str(e)}")
                skipped_count += 1

        return {
            'event': event,
            'member_id': member.id,
            'triggered': triggered_count,
            'skipped': skipped_count,
            'results': results
        }

    def execute_campaign(self, campaign: LoyaltyCampaign, member: LoyaltyMember, context: dict):
        """
        Execute a campaign for a specific member.

        Creates a campaign execution record and triggers action processing.

        Args:
            campaign: LoyaltyCampaign instance
            member: LoyaltyMember instance
            context: Trigger context data

        Returns:
            dict: Execution result with execution_id
        """
        logger.info(f"Executing campaign {campaign.id} for member {member.id}")

        # Create execution record
        execution = self._create_execution(campaign, member, context)

        # Queue campaign execution via Celery
        from loyalty.tasks import trigger_campaign
        trigger_campaign.delay(campaign.id, member.id, context)

        # Update campaign statistics
        campaign.total_triggered += 1
        campaign.last_triggered_at = timezone.now()
        campaign.save(update_fields=['total_triggered', 'last_triggered_at'])

        return {
            'campaign_id': campaign.id,
            'execution_id': execution.id,
            'status': 'queued'
        }

    @transaction.atomic
    def _create_execution(self, campaign: LoyaltyCampaign, member: LoyaltyMember, context: dict):
        """
        Create a campaign execution record.

        Args:
            campaign: LoyaltyCampaign instance
            member: LoyaltyMember instance
            context: Trigger context data

        Returns:
            LoyaltyCampaignExecution: Created execution
        """
        # A/B variant assignment
        ab_variant = ''
        if campaign.is_ab_test:
            ab_variant = campaign.ab_variant

        execution = LoyaltyCampaignExecution.objects.create(
            campaign=campaign,
            member=member,
            status=LoyaltyCampaignExecution.STATUS_PENDING,
            trigger_context=context,
            ab_variant_assigned=ab_variant
        )

        logger.debug(f"Created execution {execution.id} for campaign {campaign.id}")
        return execution

    def evaluate_trigger_conditions(self, campaign: LoyaltyCampaign, context: dict) -> bool:
        """
        Evaluate campaign trigger conditions against context.

        Args:
            campaign: LoyaltyCampaign instance
            context: Trigger context data

        Returns:
            bool: True if all conditions are met
        """
        if not campaign.trigger_conditions:
            return True

        conditions = campaign.trigger_conditions

        # Evaluate min_order_amount
        if 'min_order_amount' in conditions:
            order_total = context.get('order_total', 0)
            if float(order_total) < float(conditions['min_order_amount']):
                logger.debug(f"Order total {order_total} below minimum {conditions['min_order_amount']}")
                return False

        # Evaluate max_order_amount
        if 'max_order_amount' in conditions:
            order_total = context.get('order_total', 0)
            if float(order_total) > float(conditions['max_order_amount']):
                logger.debug(f"Order total {order_total} above maximum {conditions['max_order_amount']}")
                return False

        # Evaluate category_ids (order contains items from specific categories)
        if 'category_ids' in conditions:
            order_category_ids = context.get('category_ids', [])
            required_categories = conditions['category_ids']
            if not any(cat_id in required_categories for cat_id in order_category_ids):
                logger.debug(f"No matching categories")
                return False

        # Evaluate product_ids (order contains specific products)
        if 'product_ids' in conditions:
            order_product_ids = context.get('product_ids', [])
            required_products = conditions['product_ids']
            if not any(prod_id in required_products for prod_id in order_product_ids):
                logger.debug(f"No matching products")
                return False

        # Evaluate nth_purchase
        if 'nth_purchase' in conditions:
            order_count = context.get('order_count', 0)
            if order_count != conditions['nth_purchase']:
                logger.debug(f"Not nth purchase: {order_count} != {conditions['nth_purchase']}")
                return False

        # Evaluate min_days_inactive
        if 'min_days_inactive' in conditions:
            days_inactive = context.get('days_inactive', 0)
            if days_inactive < conditions['min_days_inactive']:
                logger.debug(f"Not inactive long enough: {days_inactive} < {conditions['min_days_inactive']}")
                return False

        # All conditions passed
        return True

    def process_campaign_actions(self, execution: LoyaltyCampaignExecution):
        """
        Process actions for a campaign execution.

        Args:
            execution: LoyaltyCampaignExecution instance

        Returns:
            dict: Processing results
        """
        from loyalty.services.campaign_action_executor import CampaignActionExecutor

        logger.info(f"Processing actions for execution {execution.id}")

        execution.status = LoyaltyCampaignExecution.STATUS_PROCESSING
        execution.save(update_fields=['status'])

        campaign = execution.campaign
        member = execution.member
        context = execution.trigger_context

        executor = CampaignActionExecutor()
        results = {
            'actions_completed': 0,
            'actions_failed': 0,
            'errors': []
        }

        # Determine which actions to execute
        if campaign.is_journey:
            # Multi-step journey - execute current step
            actions = self._get_journey_step_actions(campaign, execution.current_step)
        else:
            # Single-step campaign - execute all actions
            actions = campaign.actions

        # Execute each action
        for action in actions:
            try:
                result = executor.execute_action(action, member, context)
                execution.add_action_result(action['type'], result)

                # Track results
                if action['type'] == 'award_points' and result.get('success'):
                    execution.points_awarded += result.get('points', 0)
                elif action['type'] == 'issue_reward' and result.get('success'):
                    execution.rewards_issued.append(result.get('reward_id'))
                elif action['type'] == 'send_email' and result.get('success'):
                    execution.emails_sent.append(action.get('template'))

                results['actions_completed'] += 1

            except Exception as e:
                logger.error(f"Action {action['type']} failed: {str(e)}")
                results['actions_failed'] += 1
                results['errors'].append(str(e))

        # Save execution results
        execution.save(update_fields=['points_awarded', 'rewards_issued', 'emails_sent'])

        # Handle journey next step scheduling
        if campaign.is_journey:
            self._schedule_next_journey_step(campaign, execution)
        else:
            # Mark as completed
            execution.mark_completed()
            campaign.total_completed += 1
            campaign.save(update_fields=['total_completed'])

        return results

    def _get_journey_step_actions(self, campaign: LoyaltyCampaign, step_number: int) -> list:
        """
        Get actions for a specific journey step.

        Args:
            campaign: LoyaltyCampaign instance
            step_number: Step number to retrieve

        Returns:
            list: Actions for the step
        """
        if not campaign.journey_steps:
            return []

        for step in campaign.journey_steps:
            if step.get('step') == step_number:
                return step.get('actions', [])

        return []

    def _evaluate_journey_step_conditions(
        self,
        step_config: dict,
        member: 'LoyaltyMember',
        execution: LoyaltyCampaignExecution
    ) -> bool:
        """
        Evaluate conditions for a journey step.

        Supports:
        - points_threshold: Minimum points required
        - tier_required: Required tier ID
        - orders_since_start: Minimum orders since journey started
        - spent_since_start: Minimum spend since journey started
        - has_redeemed_since_start: Whether member redeemed during journey
        - custom_conditions: Additional custom conditions

        Args:
            step_config: Step configuration dict
            member: LoyaltyMember instance
            execution: LoyaltyCampaignExecution instance

        Returns:
            bool: True if conditions pass
        """
        conditions = step_config.get('conditions', {})

        if not conditions:
            return True

        # Points threshold
        if 'points_threshold' in conditions:
            try:
                balance = member.balance
                if balance.available_points < conditions['points_threshold']:
                    logger.debug(
                        f"Member {member.id} below points threshold: "
                        f"{balance.available_points} < {conditions['points_threshold']}"
                    )
                    return False
            except Exception as e:
                logger.error(f"Error checking points threshold: {e}")
                return False

        # Tier requirement
        if 'tier_required' in conditions:
            if not member.current_tier or member.current_tier.id != conditions['tier_required']:
                logger.debug(f"Member {member.id} not in required tier")
                return False

        # Orders since journey started
        if 'orders_since_start' in conditions:
            from orders.models import Order

            orders_count = Order.objects.filter(
                user=member.customer,
                status='completed',
                created_at__gte=execution.triggered_at
            ).count()

            if orders_count < conditions['orders_since_start']:
                logger.debug(
                    f"Member {member.id} insufficient orders since start: "
                    f"{orders_count} < {conditions['orders_since_start']}"
                )
                return False

        # Spend since journey started
        if 'spent_since_start' in conditions:
            from orders.models import Order
            from django.db.models import Sum

            total_spent = Order.objects.filter(
                user=member.customer,
                status='completed',
                created_at__gte=execution.triggered_at
            ).aggregate(total=Sum('total_amount'))['total'] or 0

            if total_spent < conditions['spent_since_start']:
                logger.debug(
                    f"Member {member.id} insufficient spend since start: "
                    f"{total_spent} < {conditions['spent_since_start']}"
                )
                return False

        # Has redeemed since start
        if 'has_redeemed_since_start' in conditions:
            from loyalty.models import LoyaltyRedemption

            has_redeemed = LoyaltyRedemption.objects.filter(
                member=member,
                created_at__gte=execution.triggered_at
            ).exists()

            if conditions['has_redeemed_since_start'] != has_redeemed:
                logger.debug(
                    f"Member {member.id} redemption requirement not met"
                )
                return False

        # All conditions passed
        return True

    def _get_next_journey_step(
        self,
        campaign: LoyaltyCampaign,
        execution: LoyaltyCampaignExecution,
        current_step: int
    ) -> tuple:
        """
        Determine the next journey step, supporting branching logic.

        Args:
            campaign: LoyaltyCampaign instance
            execution: LoyaltyCampaignExecution instance
            current_step: Current step number

        Returns:
            tuple: (next_step_number, delay_days) or (None, None) if journey complete
        """
        # Find current step configuration
        step_config = None
        for step in campaign.journey_steps:
            if step.get('step') == current_step:
                step_config = step
                break

        if not step_config:
            logger.warning(f"No step config found for step {current_step}")
            return (None, None)

        # Check for exit conditions
        exit_conditions = step_config.get('exit_conditions', {})
        if exit_conditions:
            if self._evaluate_journey_step_conditions(
                {'conditions': exit_conditions},
                execution.member,
                execution
            ):
                logger.info(f"Exit conditions met for execution {execution.id}")
                return (None, None)

        # Check for branching
        branches = step_config.get('branches', [])
        if branches:
            for branch in branches:
                branch_conditions = branch.get('conditions', {})
                if self._evaluate_journey_step_conditions(
                    {'conditions': branch_conditions},
                    execution.member,
                    execution
                ):
                    # Branch conditions met - go to branch step
                    next_step = branch.get('next_step')
                    delay_days = branch.get('delay_days', 0)
                    logger.info(
                        f"Branch conditions met for execution {execution.id}: "
                        f"going to step {next_step}"
                    )
                    return (next_step, delay_days)

        # No branching or conditions not met - use default next step
        next_step_delay_days = step_config.get('next_step_delay_days')

        if next_step_delay_days is None:
            # No next step defined - journey complete
            return (None, None)

        next_step_number = current_step + 1
        return (next_step_number, next_step_delay_days)

    def _schedule_next_journey_step(self, campaign: LoyaltyCampaign, execution: LoyaltyCampaignExecution):
        """
        Schedule the next step in a multi-step journey.

        Supports advanced features:
        - Conditional branching
        - Exit conditions
        - Variable delays

        Args:
            campaign: LoyaltyCampaign instance
            execution: LoyaltyCampaignExecution instance
        """
        current_step = execution.current_step

        # Mark current step as completed
        if current_step not in execution.steps_completed:
            execution.steps_completed.append(current_step)
            execution.save(update_fields=['steps_completed'])

        # Determine next step using branching logic
        next_step_number, delay_days = self._get_next_journey_step(
            campaign,
            execution,
            current_step
        )

        if next_step_number is None:
            # Journey complete or exit conditions met
            logger.info(f"Journey completed for execution {execution.id} at step {current_step}")
            execution.mark_completed()
            campaign.total_completed += 1
            campaign.save(update_fields=['total_completed'])
            return

        # Schedule next step
        next_step_at = timezone.now() + timedelta(days=delay_days)

        execution.current_step = next_step_number
        execution.next_step_at = next_step_at
        execution.save(update_fields=['current_step', 'next_step_at'])

        logger.info(
            f"Scheduled step {next_step_number} for execution {execution.id} at {next_step_at} "
            f"(delay: {delay_days} days)"
        )

    def process_journey_step(self, execution_id: int, step_number: int):
        """
        Process a specific journey step.

        Args:
            execution_id: LoyaltyCampaignExecution ID
            step_number: Step number to process

        Returns:
            dict: Processing result
        """
        try:
            execution = LoyaltyCampaignExecution.objects.select_related('campaign', 'member').get(id=execution_id)
        except LoyaltyCampaignExecution.DoesNotExist:
            logger.error(f"Execution {execution_id} not found")
            return {'success': False, 'error': 'Execution not found'}

        logger.info(f"Processing journey step {step_number} for execution {execution_id}")

        # Verify step number matches
        if execution.current_step != step_number:
            logger.warning(f"Step mismatch: expected {execution.current_step}, got {step_number}")
            return {'success': False, 'error': 'Step number mismatch'}

        # Evaluate step conditions
        campaign = execution.campaign
        step_config = None
        for step in campaign.journey_steps:
            if step.get('step') == step_number:
                step_config = step
                break

        if not step_config:
            logger.error(f"Step {step_number} config not found")
            return {'success': False, 'error': 'Step config not found'}

        # Check step conditions
        if not self._evaluate_journey_step_conditions(step_config, execution.member, execution):
            logger.info(f"Step {step_number} conditions not met, skipping to next step")
            # Mark as completed but skip to next step
            if step_number not in execution.steps_completed:
                execution.steps_completed.append(step_number)
                execution.save(update_fields=['steps_completed'])
            self._schedule_next_journey_step(campaign, execution)
            return {'success': True, 'skipped': True}

        # Process actions for this step
        result = self.process_campaign_actions(execution)

        return {'success': True, 'result': result}

    def _evaluate_step_conditions(self, member: LoyaltyMember, conditions: dict) -> bool:
        """
        Evaluate conditions for a journey step.

        Args:
            member: LoyaltyMember instance
            conditions: Condition dictionary

        Returns:
            bool: True if conditions are met
        """
        # Check min_orders
        if 'min_orders' in conditions:
            order_count = member.customer.orders.filter(status='completed').count()
            if order_count < conditions['min_orders']:
                return False

        # Check min_points
        if 'min_points' in conditions:
            if member.balance.available_points < conditions['min_points']:
                return False

        # Check tier_required
        if 'tier_required' in conditions:
            if not member.current_tier or member.current_tier.id != conditions['tier_required']:
                return False

        return True
