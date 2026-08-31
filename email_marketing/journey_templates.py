"""Starter journeys — ready-made flows a merchant can begin from.

Each starter is just a portable share document (see ``services.journey_io``): the
flow's shape plus the *names* of the emails and segments it expects. Applying one
rebuilds the graph and re-links any email/segment that already exists by name;
the rest are left as clearly-unconfigured steps for the merchant to fill in.

Keeping starters in the share format means there's exactly one code path for
"apply a template" and "import a shared journey".
"""

from email_marketing.services.journey_io import FORMAT_KEY, FORMAT_VERSION


def _linear(name, trigger, steps):
    """Build ``entry → step → step → … → exit`` from a list of step specs.

    Each step is ``("send", "Email name")`` or ``("wait", value, unit)``. Nodes
    are laid out top-to-bottom so the imported graph reads as a clean column.
    """
    nodes = [{"key": "entry", "node_type": "entry", "pos_x": 360, "pos_y": 40, "config": {}}]
    edges = []
    prev = "entry"
    y = 40
    for i, step in enumerate(steps):
        y += 140
        key = f"s{i}"
        if step[0] == "send":
            nodes.append(
                {
                    "key": key,
                    "node_type": "send_email",
                    "pos_x": 360,
                    "pos_y": y,
                    "config": {},
                    "campaign_name": step[1],
                }
            )
        else:  # ("wait", value, unit)
            nodes.append(
                {
                    "key": key,
                    "node_type": "wait_delay",
                    "pos_x": 360,
                    "pos_y": y,
                    "config": {"value": step[1], "unit": step[2]},
                }
            )
        edges.append({"from": prev, "to": key, "branch": "default"})
        prev = key
    y += 140
    nodes.append({"key": "exit", "node_type": "exit", "pos_x": 360, "pos_y": y, "config": {}})
    edges.append({"from": prev, "to": "exit", "branch": "default"})
    return {
        FORMAT_KEY: FORMAT_VERSION,
        "name": name,
        "trigger_event": trigger,
        "nodes": nodes,
        "edges": edges,
    }


# A branch-demonstrating starter: after an order, split VIP vs everyone else.
_VIP_SPLIT_DOC = {
    FORMAT_KEY: FORMAT_VERSION,
    "name": "VIP vs standard offer",
    "trigger_event": "order_placed",
    "nodes": [
        {"key": "entry", "node_type": "entry", "pos_x": 360, "pos_y": 40, "config": {}},
        {
            "key": "wait",
            "node_type": "wait_delay",
            "pos_x": 360,
            "pos_y": 180,
            "config": {"value": 1, "unit": "days"},
        },
        {
            "key": "branch",
            "node_type": "branch",
            "pos_x": 360,
            "pos_y": 320,
            "config": {"condition": "in_segment"},
            "segment_name": "VIP customers",
        },
        {
            "key": "vip",
            "node_type": "send_email",
            "pos_x": 150,
            "pos_y": 480,
            "config": {},
            "campaign_name": "VIP thank-you offer",
        },
        {
            "key": "std",
            "node_type": "send_email",
            "pos_x": 560,
            "pos_y": 480,
            "config": {},
            "campaign_name": "Thanks for your order",
        },
        {"key": "exit", "node_type": "exit", "pos_x": 360, "pos_y": 640, "config": {}},
    ],
    "edges": [
        {"from": "entry", "to": "wait", "branch": "default"},
        {"from": "wait", "to": "branch", "branch": "default"},
        {"from": "branch", "to": "vip", "branch": "yes"},
        {"from": "branch", "to": "std", "branch": "no"},
        {"from": "vip", "to": "exit", "branch": "default"},
        {"from": "std", "to": "exit", "branch": "default"},
    ],
}


STARTERS = [
    {
        "key": "welcome",
        "name": "Welcome series",
        "icon": "fas fa-hand-sparkles",
        "description": "Greet new subscribers, share what you're about, then a first-order nudge.",
        "trigger_event": "customer_signup",
        "doc": _linear(
            "Welcome series",
            "customer_signup",
            [
                ("send", "Welcome to the store"),
                ("wait", 3, "days"),
                ("send", "What we're about"),
                ("wait", 4, "days"),
                ("send", "Here's 10% off your first order"),
            ],
        ),
    },
    {
        "key": "first_order_onboarding",
        "name": "First-order onboarding",
        "icon": "fas fa-box-open",
        "description": "Turn a first-time buyer into a repeat customer with a gentle onboarding.",
        "trigger_event": "first_order",
        "doc": _linear(
            "First-order onboarding",
            "first_order",
            [
                ("send", "Thanks for your first order"),
                ("wait", 2, "days"),
                ("send", "Getting the most out of your purchase"),
                ("wait", 5, "days"),
                ("send", "You might also like…"),
            ],
        ),
    },
    {
        "key": "post_purchase",
        "name": "Post-purchase & review",
        "icon": "fas fa-star",
        "description": "Say thanks after any order, then ask for a review once it's arrived.",
        "trigger_event": "order_placed",
        "doc": _linear(
            "Post-purchase & review",
            "order_placed",
            [
                ("send", "Thanks for your order"),
                ("wait", 7, "days"),
                ("send", "How did we do? Leave a review"),
            ],
        ),
    },
    {
        "key": "vip_split",
        "name": "VIP vs standard offer",
        "icon": "fas fa-code-branch",
        "description": "After an order, branch on your VIP segment to send the right offer.",
        "trigger_event": "order_placed",
        "doc": _VIP_SPLIT_DOC,
    },
    {
        "key": "cart_recovery",
        "name": "Abandoned cart recovery",
        "icon": "fas fa-cart-arrow-down",
        "description": "Win back a shopper who left items behind — a reminder, then a nudge.",
        "trigger_event": "cart_abandoned",
        "doc": _linear(
            "Abandoned cart recovery",
            "cart_abandoned",
            [
                ("send", "You left something behind"),
                ("wait", 1, "days"),
                ("send", "Still thinking it over?"),
            ],
        ),
    },
    {
        "key": "win_back",
        "name": "Win-back lapsed customers",
        "icon": "fas fa-heart",
        "description": "Re-engage customers who haven't bought in a while with a reason to return.",
        "trigger_event": "win_back",
        "doc": _linear(
            "Win-back lapsed customers",
            "win_back",
            [
                ("send", "We miss you"),
                ("wait", 5, "days"),
                ("send", "Here's a little something to come back"),
            ],
        ),
    },
    {
        "key": "review_request",
        "name": "Post-delivery review request",
        "icon": "fas fa-comment-dots",
        "description": "Ask for a review a few days after an order is delivered, once it's arrived.",
        "trigger_event": "order_delivered",
        "doc": _linear(
            "Post-delivery review request",
            "order_delivered",
            [
                ("wait", 3, "days"),
                ("send", "How's your order? Leave a review"),
            ],
        ),
    },
    {
        "key": "back_in_stock",
        "name": "Back-in-stock alert",
        "icon": "fas fa-bell",
        "description": "Tell waiting shoppers the moment a product they wanted is available again.",
        "trigger_event": "back_in_stock",
        "doc": _linear(
            "Back-in-stock alert",
            "back_in_stock",
            [
                ("send", "It's back in stock"),
            ],
        ),
    },
]


def get_starters():
    """The starter catalogue for the picker (metadata only, no docs)."""
    return [
        {
            "key": s["key"],
            "name": s["name"],
            "icon": s["icon"],
            "description": s["description"],
            "trigger_event": s["trigger_event"],
        }
        for s in STARTERS
    ]


def get_starter_doc(key):
    """The portable document for a starter, or None if the key is unknown."""
    for s in STARTERS:
        if s["key"] == key:
            return s["doc"]
    return None
