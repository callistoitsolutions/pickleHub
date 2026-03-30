from django.shortcuts import render
from .models import HeroSection
# Create your views here.
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt






# views.py
# PickleHub – Hero Section Views
# NO forms.py used — all data is read directly from request.POST / request.body (JSON).







# ──────────────────────────────────────────────
# 1. PUBLIC HOME PAGE
# ──────────────────────────────────────────────
def index_view(request):
    """
    Public-facing home page.
    Passes the single HeroSection object to the template.
    """
    hero = HeroSection.get_or_create_default()
    return render(request, 'core/index.html', {'hero': hero})




# ──────────────────────────────────────────────
# 3. SAVE HERO (AJAX POST from admin builder)
# ──────────────────────────────────────────────
@require_POST
def save_hero(request):
    """
    Receives JSON from the admin builder's "Save & Publish" button.
    Updates (or creates) the single HeroSection row.

    Expected JSON body:
    {
        "badge_text": "...",
        "title_line1": "...",
        "title_highlight": "...",
        "title_line2": "...",
        "subtitle": "...",
        "btn_primary_text": "...",
        "btn_primary_url": "...",
        "btn_secondary_text": "...",
        "whatsapp_number": "...",
        "jar_emoji": "...",
        "stats_json": [...],
        "float_badges_json": [...],
        "is_visible": true
    }
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'ok': False, 'error': 'Invalid JSON'}, status=400)

    hero = HeroSection.get_or_create_default()

    # Update only fields that are present in the payload
    hero.badge_text         = data.get('badge_text',         hero.badge_text)
    hero.title_line1        = data.get('title_line1',        hero.title_line1)
    hero.title_highlight    = data.get('title_highlight',    hero.title_highlight)
    hero.title_line2        = data.get('title_line2',        hero.title_line2)
    hero.subtitle           = data.get('subtitle',           hero.subtitle)
    hero.btn_primary_text   = data.get('btn_primary_text',   hero.btn_primary_text)
    hero.btn_primary_url    = data.get('btn_primary_url',    hero.btn_primary_url)
    hero.btn_secondary_text = data.get('btn_secondary_text', hero.btn_secondary_text)
    hero.whatsapp_number    = data.get('whatsapp_number',    hero.whatsapp_number)
    hero.jar_emoji          = data.get('jar_emoji',          hero.jar_emoji)
    hero.stats_json         = data.get('stats_json',         hero.stats_json)
    hero.float_badges_json  = data.get('float_badges_json',  hero.float_badges_json)
    hero.is_visible         = data.get('is_visible',         hero.is_visible)

    hero.save()

    return JsonResponse({'ok': True, 'message': '✅ Hero section saved!'})


# ──────────────────────────────────────────────
# 4. LOAD HERO  (AJAX GET – optional, for page refresh without reload)
# ──────────────────────────────────────────────
def load_hero(request):
    """
    Returns current hero data as JSON.
    Useful if you want to reload data without page refresh.
    """
    hero = HeroSection.get_or_create_default()
    return JsonResponse({
        'ok': True,
        'hero': {
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
    })


def products(request):
    return render(request, 'products_panel/all_pickle.html')

def login(request):
    return render(request, 'account/login.html')

def cart(request):
    return render(request, 'cart/cart.html')

def product_details(request):
    return render(request, 'products_panel/product_details.html')

def checkout(request):
    return render(request, 'payments/checkout.html')

def contact(request):
    return render(request, 'core/contact.html')



