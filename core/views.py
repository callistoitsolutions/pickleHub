from django.shortcuts import render
from .models import HeroSection,FeaturesSection
# Create your views here.
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt






# views.py
# PickleHub – Hero Section Views
# NO forms.py used — all data is read directly from request.POST / request.body (JSON).







# views.py
# PickleHub – Views for Hero + Features sections
# NO forms.py used — all data via request.body JSON.




# ──────────────────────────────────────────────
# 1. PUBLIC HOME PAGE
# ──────────────────────────────────────────────
def index_view(request):
    """
    Public home page — passes both hero and features to the template.
    """
    hero     = HeroSection.get_or_create_default()
    features = FeaturesSection.get_or_create_default()
    return render(request, 'core/index.html', {
        'hero':     hero,
        'features': features,
    })


# ──────────────────────────────────────────────
# 2. ADMIN HOME PAGE
# ──────────────────────────────────────────────


# ──────────────────────────────────────────────
# 3. SAVE HERO  (AJAX POST)
# ──────────────────────────────────────────────
@require_POST
def save_hero(request):
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'ok': False, 'error': 'Invalid JSON'}, status=400)

    hero = HeroSection.get_or_create_default()
    hero.badge_text        = data.get('badge_text',        hero.badge_text)
    hero.title_line1       = data.get('title_line1',       hero.title_line1)
    hero.title_highlight   = data.get('title_highlight',   hero.title_highlight)
    hero.title_line2       = data.get('title_line2',       hero.title_line2)
    hero.subtitle          = data.get('subtitle',          hero.subtitle)
    hero.jar_emoji         = data.get('jar_emoji',         hero.jar_emoji)
    hero.hero_image_url    = data.get('hero_image_url',    hero.hero_image_url)
    hero.buttons_json      = data.get('buttons_json',      hero.buttons_json)
    hero.stats_json        = data.get('stats_json',        hero.stats_json)
    hero.float_badges_json = data.get('float_badges_json', hero.float_badges_json)
    hero.is_visible        = data.get('is_visible',        hero.is_visible)
    hero.save()

    return JsonResponse({'ok': True, 'message': '✅ Hero section saved!'})


# ──────────────────────────────────────────────
# 4. SAVE FEATURES  (AJAX POST)  ← NEW
# ──────────────────────────────────────────────
@require_POST
def save_features(request):
    """
    Receives JSON from the admin builder's Features Strip tab.

    Expected JSON body:
    {
        "items_json": [
            {"ico": "🚚", "title": "Free Delivery", "sub": "Orders above ₹499"},
            ...
        ],
        "is_visible": true
    }
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'ok': False, 'error': 'Invalid JSON'}, status=400)

    features = FeaturesSection.get_or_create_default()
    features.items_json = data.get('items_json', features.items_json)
    features.is_visible = data.get('is_visible', features.is_visible)
    features.save()

    return JsonResponse({'ok': True, 'message': '✅ Features section saved!'})


# ──────────────────────────────────────────────
# 5. LOAD HERO  (AJAX GET – optional)
# ──────────────────────────────────────────────
def load_hero(request):
    hero = HeroSection.get_or_create_default()
    return JsonResponse({
        'ok': True,
        'hero': {
            'badge_text':        hero.badge_text,
            'title_line1':       hero.title_line1,
            'title_highlight':   hero.title_highlight,
            'title_line2':       hero.title_line2,
            'subtitle':          hero.subtitle,
            'jar_emoji':         hero.jar_emoji,
            'hero_image_url':    hero.hero_image_url,
            'buttons_json':      hero.buttons_json,
            'stats_json':        hero.stats_json,
            'float_badges_json': hero.float_badges_json,
            'is_visible':        hero.is_visible,
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



