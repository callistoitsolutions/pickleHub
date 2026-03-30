# views.py
# PickleHub – Hero Section Views
# UPDATED: buttons_json replaces fixed btn_primary/secondary/whatsapp fields.
# NO forms.py used — data read directly from request.body (JSON).

import json
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core.models import HeroSection,FeaturesSection


# ──────────────────────────────────────────────
# 1. PUBLIC HOME PAGE
# ──────────────────────────────────────────────

def dashboard(request):
    """
    Admin dashboard page.
    Passes hero_json and features_json as JS-injectable strings.
    """
    hero     = HeroSection.get_or_create_default()
    features = FeaturesSection.get_or_create_default()

    hero_data = {
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

    features_data = {
        'items_json': features.items_json,
        'is_visible': features.is_visible,
    }

    return render(request, 'Admin_pages/dashboard.html', {
        'hero_json':     json.dumps(hero_data),
        'features_json': json.dumps(features_data),
    })
# ──────────────────────────────────────────────
# 2. ADMIN HOME PAGE
# ──────────────────────────────────────────────
def hero_section(request):
    """
    Admin builder page.
    Passes hero_json and features_json as JS-injectable strings.
    """
    hero     = HeroSection.get_or_create_default()
    features = FeaturesSection.get_or_create_default()

    hero_data = {
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

    features_data = {
        'items_json': features.items_json,
        'is_visible': features.is_visible,
    }

    return render(request, 'Admin_pages/hero_section.html', {
        'hero_json':     json.dumps(hero_data),
        'features_json': json.dumps(features_data),
    })



def feature_section(request):
    """
    Admin builder page.
    Passes hero_json and features_json as JS-injectable strings.
    """
    hero     = HeroSection.get_or_create_default()
    features = FeaturesSection.get_or_create_default()

    hero_data = {
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

    features_data = {
        'items_json': features.items_json,
        'is_visible': features.is_visible,
    }

    return render(request, 'Admin_pages/feature_section.html', {
        'hero_json':     json.dumps(hero_data),
        'features_json': json.dumps(features_data),
    })
