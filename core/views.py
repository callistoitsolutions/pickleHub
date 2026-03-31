from django.shortcuts import render
from Admin_app.models import *
import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from Admin_app.models import *

from Admin_app.utils import _hero_data, _features_data, _category_data
from products.models import *
from django.core.paginator import Paginator
from django.utils.text import slugify
from django.shortcuts import render, get_object_or_404










def index(request):

    # 🔹 Banner logic
    active_banners = OfferBanner.objects.filter(is_active=True).order_by('order')

    banner_pairs = []
    for i in range(0, len(active_banners), 2):
        pair = {'main': None, 'potw': None}

        if i < len(active_banners):
            banner1 = active_banners[i]
            if banner1.offer_type == 'main':
                pair['main'] = banner1
            else:
                pair['potw'] = banner1

        if i + 1 < len(active_banners):
            banner2 = active_banners[i + 1]
            if banner2.offer_type == 'main':
                pair['main'] = banner2
            else:
                pair['potw'] = banner2

        if pair['main'] or pair['potw']:
            banner_pairs.append(pair)

    # 🔹 Sections
    hero = HeroSection.get_or_create_default()
    features = FeaturesSection.get_or_create_default()
    category = CategorySection.get_or_create_default()

    # 🔹 Data
    brands = Brand.objects.filter(is_active=True).order_by('order')
    reviews = Review.objects.filter(is_active=True).order_by('order')
    newsletter = NewsletterSetting.objects.last()

    # 🔥 Products
    products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('brand', 'category').order_by('sort_order')[:12]

    # 🔥 Category names (for filter buttons)
    categories = [
        item.get('name')
        for item in category.items_json
    ]

    # 🔹 Final context (ONLY ONE)
    context = {
        'banner_pairs': banner_pairs,
        'hero': hero,
        'features': features,
        'brands': brands,
        'reviews': reviews,
        'newsletter': newsletter,

        # Category section
        'category': category,

        # Product section
        'products': products,
        'categories': categories,
    }

    return render(request, 'home/index.html', context)
    

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
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'ok': False, 'error': 'Invalid JSON'}, status=400)
 
    features = FeaturesSection.get_or_create_default()
    features.items_json = data.get('items_json', features.items_json)
    features.is_visible = data.get('is_visible', features.is_visible)
    features.save()
 
    return JsonResponse({'ok': True, 'message': '✅ Features section saved!'})
 


@require_POST
def save_category(request):
    """
    Receives JSON from the category builder.
 
    Expected body:
    {
        "section_title":    "Shop by Category",
        "section_subtitle": "Browse our wide range...",
        "items_json": [
            {
                "emoji":       "🥭",
                "name":        "Mango Pickle",
                "count":       "32 products",
                "url":         "/category/mango/",
                "bg_gradient": "linear-gradient(135deg,#fff3e0,#ffcc80)"
            },
            ...
        ],
        "is_visible": true
    }
    """
    try:
        data = json.loads(request.body)
    except (json.JSONDecodeError, ValueError):
        return JsonResponse({'ok': False, 'error': 'Invalid JSON'}, status=400)
 
    category = CategorySection.get_or_create_default()
    category.section_title    = data.get('section_title',    category.section_title)
    category.section_subtitle = data.get('section_subtitle', category.section_subtitle)
    category.items_json       = data.get('items_json',       category.items_json)
    category.is_visible       = data.get('is_visible',       category.is_visible)
    category.save()
 
    return JsonResponse({'ok': True, 'message': '✅ Category section saved!'})
 
 
# ──────────────────────────────────────────────
# 5. LOAD HERO  (AJAX GET – optional)
# ──────────────────────────────────────────────
def load_hero(request):
    hero = HeroSection.get_or_create_default()
    return JsonResponse({'ok': True, 'hero': _hero_data(hero)})
 
 
# ──────────────────────────────────────────────
# 10. LOAD CATEGORY  (AJAX GET)  ← NEW
# ──────────────────────────────────────────────
 
def load_category(request):
    category = CategorySection.get_or_create_default()
    return JsonResponse({'ok': True, 'category': _category_data(category)})




def login(request):
    return render(request, 'account/login.html')

def cart(request):
    return render(request, 'cart/cart.html')


def product_details(request, slug):
    product  = get_object_or_404(Product, slug=slug, is_active=True)
    related  = Product.objects.filter(
                   category=product.category, is_active=True
               ).exclude(id=product.id).select_related('brand')[:4]
    also_bought = Product.objects.filter(
                      is_active=True
                  ).exclude(id=product.id).exclude(
                      id__in=related.values_list('id', flat=True)
                  ).order_by('-review_count')[:4]

    return render(request, 'products_panel/product_details.html', {
        'product':     product,
        'related':     related,
        'also_bought': also_bought,
    })

def checkout(request):
    return render(request, 'payments/checkout.html')

def contact(request):
    return render(request, 'home/contact.html')


def All_products(request):
    """
    Public products listing page.
    Reads filter querystring params and returns filtered, paginated products.
    """
    settings   = ProductPageSettings.get_or_create_default()
    categories = CategorySection.get_or_create_default()
    brands     = Brand.objects.filter(is_active=True)
    products_qs = Product.objects.filter(is_active=True).select_related('brand', 'category')

    # ── apply filters from GET params ──
    cat_ids    = request.GET.getlist('cat')       # ?cat=1&cat=2
    brand_ids  = request.GET.getlist('brand')     # ?brand=3
    regions    = request.GET.getlist('region')    # ?region=Rajasthan
    price_max  = request.GET.get('price_max', settings.price_max)
    min_rating = request.GET.get('rating', '')
    weights    = request.GET.getlist('weight')
    sort       = request.GET.get('sort', 'popular')

    if cat_ids:
        products_qs = products_qs.filter(category__id__in=cat_ids)
    if brand_ids:
        products_qs = products_qs.filter(brand__id__in=brand_ids)
    if regions:
        products_qs = products_qs.filter(region__in=regions)
    if price_max:
        products_qs = products_qs.filter(price__lte=price_max)
    if min_rating:
        products_qs = products_qs.filter(rating__gte=min_rating)

    # ── sorting ──
    sort_map = {
        'popular':    '-review_count',
        'price_asc':  'price',
        'price_desc': '-price',
        'newest':     '-created_at',
        'rating':     '-rating',
    }
    products_qs = products_qs.order_by(sort_map.get(sort, '-review_count'))

    # ── pagination ──
    paginator = Paginator(products_qs, 12)
    page_num  = request.GET.get('page', 1)
    page_obj  = paginator.get_page(page_num)

    return render(request, 'products_panel/All_products.html', {
        'products':         page_obj,
        'paginator':        paginator,
        'page_obj':         page_obj,
        'categories':       categories,
        'brands':           brands,
        'settings':         settings,
        'total_count':      products_qs.count(),
        'selected_cats':    [int(x) for x in cat_ids   if x.isdigit()],
        'selected_brands':  [int(x) for x in brand_ids if x.isdigit()],
        'selected_regions': regions,
        'current_price_max':int(price_max),
        'current_sort':     sort,
        'current_rating':   min_rating,
    })



