import json

from django.shortcuts import render
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt   # remove in production; use Django CSRF token instead
 
from core.models import HeroSection

# Create your views here.



# ──────────────────────────────────────────────
# 2. ADMIN HOME PAGE  (renders the builder UI)
# ──────────────────────────────────────────────
def admin_home(request):
    """
    Renders the admin builder page.
    Passes current hero data as a JSON string so the JS can pre-fill the form.
    """
    hero = HeroSection.get_or_create_default()

    # Serialize to dict for the template / JS pre-fill
    hero_data = {
        'badge_text':         hero.badge_text,
        'title_line1':        hero.title_line1,
        'title_highlight':    hero.title_highlight,
        'title_line2':        hero.title_line2,
        'subtitle':           hero.subtitle,
        'btn_primary_text':   hero.btn_primary_text,
        'btn_primary_url':    hero.btn_primary_url,
        'btn_secondary_text': hero.btn_secondary_text,
        'whatsapp_number':    hero.whatsapp_number,
        'jar_emoji':          hero.jar_emoji,
        'stats_json':         hero.stats_json,
        'float_badges_json':  hero.float_badges_json,
        'is_visible':         hero.is_visible,
    }

    return render(request, 'Admin_pages/admin_home.html', {
        'hero_json': json.dumps(hero_data),   # passed as a JSON string → window.HERO_DATA in JS
    })
