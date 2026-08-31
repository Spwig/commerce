"""The 0006 data migration converts linear JourneyStep chains into node graphs.

This is a one-shot, irreversible conversion, so it gets a real migration test:
build a linear journey (+ an in-flight enrollment) on the pre-migration schema,
run 0006, and assert the resulting graph and re-pointed enrollment.
"""

from django.db import connection
from django.db.migrations.executor import MigrationExecutor
from django.test import TransactionTestCase
from django.utils import timezone


class LinearToGraphMigrationTest(TransactionTestCase):
    migrate_from = ("email_marketing", "0005_journey_journeyenrollment_journeystep_and_more")
    migrate_to = ("email_marketing", "0006_remove_journeyenrollment_current_step_and_more")

    def _migrate(self, target):
        executor = MigrationExecutor(connection)
        executor.migrate([target])
        executor.loader.build_graph()
        return executor.loader.project_state([target]).apps

    def tearDown(self):
        # Restore the DB to the LATEST migration so sibling tests in this process see
        # the current schema. Migrating only to ``migrate_to`` (0006) would leave the
        # reused DB behind the code — e.g. missing Subscriber.first_name (0008) — and
        # break any later TransactionTestCase that uses those columns. Use the app's
        # leaf migration so this stays correct as new migrations are added.
        executor = MigrationExecutor(connection)
        latest = [n for n in executor.loader.graph.leaf_nodes() if n[0] == "email_marketing"]
        executor.migrate(latest)

    def test_linear_journey_becomes_a_node_graph(self):
        old = self._migrate(self.migrate_from)

        Site = old.get_model("sites", "Site")
        Journey = old.get_model("email_marketing", "Journey")
        Campaign = old.get_model("email_marketing", "Campaign")
        JourneyStep = old.get_model("email_marketing", "JourneyStep")
        Subscriber = old.get_model("email_marketing", "Subscriber")
        JourneyEnrollment = old.get_model("email_marketing", "JourneyEnrollment")

        site, _ = Site.objects.get_or_create(pk=1, defaults={"domain": "ex.com", "name": "Ex"})
        journey = Journey.objects.create(
            site=site, name="Welcome", trigger_event="customer_signup", status="active"
        )
        c0 = Campaign.objects.create(site=site, name="c0", subject="s0", message_type="newsletter")
        c1 = Campaign.objects.create(site=site, name="c1", subject="s1", message_type="newsletter")
        JourneyStep.objects.create(
            journey=journey, order=0, delay_value=0, delay_unit="days", campaign=c0
        )
        JourneyStep.objects.create(
            journey=journey, order=1, delay_value=3, delay_unit="days", campaign=c1
        )
        sub = Subscriber.objects.create(site=site, email="mid@ex.com", status="active")
        # An in-flight enrollment paused before step 1.
        JourneyEnrollment.objects.create(
            journey=journey,
            subscriber=sub,
            current_step=1,
            next_step_at=timezone.now(),
            status="active",
        )

        new = self._migrate(self.migrate_to)
        JourneyNode = new.get_model("email_marketing", "JourneyNode")
        JourneyEdge = new.get_model("email_marketing", "JourneyEdge")
        NewEnrollment = new.get_model("email_marketing", "JourneyEnrollment")

        nodes = JourneyNode.objects.filter(journey_id=journey.id)
        # entry + (wait+send) per step + exit = 1 + 2*2 + 1 = 6
        self.assertEqual(nodes.count(), 6)
        self.assertEqual(nodes.filter(node_type="entry").count(), 1)
        self.assertEqual(nodes.filter(node_type="send_email").count(), 2)
        self.assertEqual(nodes.filter(node_type="wait_delay").count(), 2)
        self.assertEqual(nodes.filter(node_type="exit").count(), 1)
        # The chain is fully connected: 5 default edges join 6 nodes.
        self.assertEqual(JourneyEdge.objects.filter(journey_id=journey.id).count(), 5)

        # The second send carries campaign c1; the second wait is a 3-day pause.
        send_configs = sorted(
            n.config.get("campaign_id") for n in nodes.filter(node_type="send_email")
        )
        self.assertEqual(send_configs, sorted([str(c0.id), str(c1.id)]))

        # The in-flight enrollment now sits at a wait node (step 1's pause).
        enr = NewEnrollment.objects.get(subscriber_id=sub.id)
        self.assertIsNotNone(enr.current_node_id)
        moved_to = JourneyNode.objects.get(pk=enr.current_node_id)
        self.assertEqual(moved_to.node_type, "wait_delay")
        self.assertEqual(moved_to.config.get("value"), 3)
