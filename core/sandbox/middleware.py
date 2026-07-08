"""
Sandbox Banner Middleware

Injects a tamper-resistant sandbox mode banner into storefront and POS pages.
Admin pages get a subtle badge in the header instead.

The banner uses randomized element IDs per render (uuid4), inline styles only,
and a MutationObserver + interval-based tamper detection system that nukes
the page content if the banner is removed or hidden.
"""

import uuid
import logging

from django.utils.deprecation import MiddlewareMixin

from core.license import is_sandbox_mode

logger = logging.getLogger(__name__)

# Paths that should NOT get any injection (banner or badge)
EXCLUDED_PATHS = (
    '/api/', '/webhooks/', '/static/', '/media/',
    '/theme/', '/i18n/', '/__debug__/', '/health/',
)


class SandboxBannerMiddleware(MiddlewareMixin):
    """Inject sandbox banner into storefront/POS HTML responses."""

    def process_response(self, request, response):
        if not is_sandbox_mode():
            return response

        # Only process HTML responses
        content_type = response.get('Content-Type', '')
        if 'text/html' not in content_type:
            return response

        # Skip non-200, streaming, or empty responses
        if response.status_code != 200 or response.streaming:
            return response

        path = request.path

        # Strip language prefix (e.g., /en/admin/ -> /admin/)
        stripped = path
        if len(path) > 3 and path[3] == '/' and path[1:3].isalpha():
            stripped = path[3:]

        # Skip excluded paths entirely
        for exc in EXCLUDED_PATHS:
            if path.startswith(exc) or stripped.startswith(exc):
                return response

        try:
            content = response.content.decode('utf-8')
        except (UnicodeDecodeError, AttributeError):
            return response

        # Determine page type
        # Treat staff-only merchant dashboard as admin to avoid full storefront banner
        # and instead show the subtle header badge.
        is_admin = '/admin/' in path or stripped.startswith('/affiliate/merchant/')
        is_pos = '/pos/' in path or stripped.startswith('/pos/')

        # Get CSP nonce for inline scripts (triggers nonce inclusion in header).
        # Must str() the lazy object — CheckableLazyObject is Falsy until read as string.
        nonce = str(getattr(request, 'csp_nonce', ''))

        if is_admin:
            # Admin badge injected before </body> (doesn't need spacer)
            if '</body>' not in content:
                return response
            inject = self._build_admin_badge(nonce)
            content = content.replace('</body>', inject + '</body>')
        elif is_pos:
            # POS banner injected after <body> to push content down
            if '<body' not in content:
                return response
            inject = self._build_pos_banner(nonce)
            # Find end of <body ...> tag and inject right after it
            body_tag_end = content.find('>', content.find('<body'))
            if body_tag_end != -1:
                content = content[:body_tag_end + 1] + inject + content[body_tag_end + 1:]
        else:
            # Storefront banner injected after <body> to push content down
            if '<body' not in content:
                return response
            inject = self._build_storefront_banner(nonce)
            # Find end of <body ...> tag and inject right after it
            body_tag_end = content.find('>', content.find('<body'))
            if body_tag_end != -1:
                content = content[:body_tag_end + 1] + inject + content[body_tag_end + 1:]

        response.content = content.encode('utf-8')
        response['Content-Length'] = len(response.content)

        return response

    def _build_storefront_banner(self, nonce='') -> str:
        """Full tamper-resistant banner for storefront pages."""
        bid = f'sb_{uuid.uuid4().hex[:12]}'
        sid = f'sh_{uuid.uuid4().hex[:12]}'
        nonce_attr = f' nonce="{nonce}"' if nonce else ''

        return f'''
<div id="{bid}" style="position:fixed;top:0;left:0;right:0;z-index:2147483647;
    background:linear-gradient(135deg,#ff6b35,#ff4444);color:#fff;
    text-align:center;padding:8px 16px;font-family:system-ui,-apple-system,sans-serif;
    font-size:13px;font-weight:600;letter-spacing:0.5px;
    box-shadow:0 2px 8px rgba(0,0,0,0.3);pointer-events:none;
    user-select:none;-webkit-user-select:none;">
    &#9888; SANDBOX MODE &#8212; This is a development/testing environment.
    Orders and payments are simulated. Not for production use.
</div>
<div id="{sid}" style="height:36px;">
    <style>
        @media (max-width: 768px) {{
            #{sid} {{ height: 72px !important; }}
        }}
    </style>
</div>
<script{nonce_attr}>
(function(){{
    var bid="{bid}",sid="{sid}";
    var B=document.getElementById(bid),S=document.getElementById(sid);
    if(!B||!S)return _nuke();

    function _check(){{
        var b=document.getElementById(bid);
        if(!b)return _nuke();
        var cs=window.getComputedStyle(b);
        if(cs.display==='none'||cs.visibility==='hidden'||
           cs.opacity==='0'||parseFloat(cs.height)<5||
           cs.position!=='fixed')return _nuke();
    }}

    function _nuke(){{
        _reportTamper();
        document.documentElement.innerHTML=
            '<html><body style="margin:0;padding:40px;font-family:system-ui,-apple-system,sans-serif;'+
            'background:#1a1a2e;color:#e94560;text-align:center;">'+
            '<h1 style="margin-top:20vh;">&#9888; License Violation</h1>'+
            '<p style="color:#eee;font-size:18px;">'+
            'The sandbox banner was removed or tampered with.<br>'+
            'This is a violation of the Spwig platform license terms.</p>'+
            '<p style="color:#aaa;margin-top:30px;">'+
            'Restore the banner or activate a production license at<br>'+
            '<a href="https://spwig.com" style="color:#e94560;">spwig.com</a></p>'+
            '</body></html>';
    }}

    function _reportTamper(){{
        try{{
            navigator.sendBeacon('/api/sandbox/tamper-report/',
                JSON.stringify({{event:'banner_tamper',url:location.href,ts:Date.now()}}));
        }}catch(e){{}}
    }}

    var obs=new MutationObserver(function(muts){{
        for(var i=0;i<muts.length;i++){{
            var removed=muts[i].removedNodes;
            for(var j=0;j<removed.length;j++){{
                if(removed[j]===B||removed[j]===S)return _nuke();
            }}
        }}
        _check();
    }});
    obs.observe(document.body,{{childList:true,subtree:true,attributes:true,attributeFilter:['style','class']}});

    setInterval(_check,2000);

    var bannerObs=new MutationObserver(function(){{_check();}});
    bannerObs.observe(B,{{attributes:true,attributeFilter:['style','class','id']}});
}})();
</script>'''

    def _build_pos_banner(self, nonce='') -> str:
        """Sandbox banner for POS pages — smaller but still tamper-resistant."""
        bid = f'ps_{uuid.uuid4().hex[:12]}'
        sid = f'psh_{uuid.uuid4().hex[:12]}'
        nonce_attr = f' nonce="{nonce}"' if nonce else ''

        return f'''
<div id="{bid}" style="position:fixed;top:0;left:0;right:0;z-index:2147483647;
    background:#ff6b35;color:#fff;text-align:center;padding:4px 12px;
    font-family:system-ui,-apple-system,sans-serif;font-size:11px;font-weight:600;
    letter-spacing:0.5px;pointer-events:none;user-select:none;">
    &#9888; SANDBOX MODE &#8212; Test environment. Payments are simulated.
</div>
<div id="{sid}" style="height:27px;">
    <style>
        @media (max-width: 768px) {{
            #{sid} {{ height: 54px !important; }}
        }}
    </style>
</div>
<script{nonce_attr}>
(function(){{
    var bid="{bid}",sid="{sid}";
    var B=document.getElementById(bid),S=document.getElementById(sid);
    if(!B||!S)return _nuke();

    function _check(){{
        var b=document.getElementById(bid);
        if(!b)return _nuke();
        var cs=window.getComputedStyle(b);
        if(cs.display==='none'||cs.visibility==='hidden'||cs.opacity==='0')return _nuke();
    }}

    function _nuke(){{
        try{{
            navigator.sendBeacon('/api/sandbox/tamper-report/',
                JSON.stringify({{event:'pos_banner_tamper',url:location.href,ts:Date.now()}}));
        }}catch(e){{}}
        document.documentElement.innerHTML=
            '<html><body style="margin:0;padding:40px;font-family:system-ui;'+
            'background:#1a1a2e;color:#e94560;text-align:center;">'+
            '<h1 style="margin-top:20vh;">&#9888; License Violation</h1>'+
            '<p style="color:#eee;">Sandbox banner tampered with. '+
            'Activate a production license at spwig.com</p></body></html>';
    }}

    var obs=new MutationObserver(function(muts){{
        for(var i=0;i<muts.length;i++){{
            var removed=muts[i].removedNodes;
            for(var j=0;j<removed.length;j++){{if(removed[j]===B||removed[j]===S)return _nuke();}}
        }}
        _check();
    }});
    obs.observe(document.body,{{childList:true,subtree:true,attributes:true,attributeFilter:['style','class']}});

    setInterval(_check,2000);
    new MutationObserver(function(){{_check();}}).observe(B,{{attributes:true,attributeFilter:['style','class','id']}});
}})();
</script>'''

    def _build_admin_badge(self, nonce='') -> str:
        """Subtle SANDBOX badge for admin header."""
        badge_id = f'ab_{uuid.uuid4().hex[:8]}'
        nonce_attr = f' nonce="{nonce}"' if nonce else ''
        return f'''
<script{nonce_attr}>
(function(){{
    var h=document.querySelector('.admin-header .header-brand');
    if(!h){{
        h=document.querySelector('#header') || document.querySelector('header');
    }}
    if(h){{
        var b=document.createElement('span');
        b.id="{badge_id}";
        b.textContent="SANDBOX";
        b.style.cssText="display:inline-flex;align-items:center;margin-left:12px;"+
            "padding:2px 8px;font-size:11px;font-weight:700;letter-spacing:1px;"+
            "background:#ff6b35;color:#fff;border-radius:3px;vertical-align:middle;";
        h.appendChild(b);
    }}
}})();
</script>'''
