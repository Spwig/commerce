"""
Subscription Signals

Django signals for subscription lifecycle events.
P2 (Email Notifications) will connect handlers to these signals.
"""

import django.dispatch

# Fired after a subscription event has been processed (both webhook and fallback).
# Provides: event (SubscriptionEvent), subscription (CustomerSubscription)
subscription_event_processed = django.dispatch.Signal()
