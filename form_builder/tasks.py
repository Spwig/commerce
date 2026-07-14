"""
Form Builder Celery Tasks.
Handles asynchronous execution of form actions after submission.
"""

import logging

from celery import shared_task

logger = logging.getLogger(__name__)


ACTION_EXECUTORS = {
    "email_notification": "form_builder.actions.email.EmailNotificationAction",
    "auto_reply": "form_builder.actions.email.AutoReplyAction",
    "webhook": "form_builder.actions.webhook.WebhookAction",
}


def _get_executor_class(action_type):
    """Dynamically import and return the executor class for an action type."""
    dotted_path = ACTION_EXECUTORS.get(action_type)
    if not dotted_path:
        return None
    module_path, class_name = dotted_path.rsplit(".", 1)
    from importlib import import_module

    module = import_module(module_path)
    return getattr(module, class_name)


@shared_task(name="form_builder.execute_form_actions")
def execute_form_actions(response_id):
    """
    Execute all active actions for a form response.

    Called after form submission to trigger notifications, auto-replies,
    and webhooks configured for the form.
    """
    from .models import FormResponse

    try:
        response = FormResponse.objects.select_related("form").get(pk=response_id)
    except FormResponse.DoesNotExist:
        logger.error("execute_form_actions: Response %s not found", response_id)
        return {"status": "error", "error": f"Response {response_id} not found"}

    actions = response.form.actions.filter(is_active=True).order_by("order")
    if not actions.exists():
        return {"status": "no_actions"}

    results = {}
    for action in actions:
        executor_class = _get_executor_class(action.action_type)
        if not executor_class:
            logger.warning(
                "execute_form_actions: Unknown action type '%s' for action %s",
                action.action_type,
                action.pk,
            )
            results[str(action.pk)] = {"status": "error", "error": "Unknown action type"}
            continue

        try:
            executor = executor_class(action, response)
            result = executor.execute()
            results[str(action.pk)] = result
        except Exception as e:
            logger.error("execute_form_actions: Action %s failed: %s", action.pk, e)
            results[str(action.pk)] = {"status": "error", "error": str(e)}

    # Store action results on the response
    response.action_results = results
    response.save(update_fields=["action_results"])

    logger.info(
        "execute_form_actions: Completed %d actions for response %s", len(results), response_id
    )
    return {"status": "completed", "results": results}
