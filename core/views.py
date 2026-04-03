from django.shortcuts import render,HttpResponse
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
from datetime import datetime
from django.db.models import Q
import traceback
from django.contrib.auth.decorators import login_required










def index(request):
    
    # Banner logic
    active_banners = OfferBanner.objects.filter(is_active=True).order_by('order')
    banner_pairs = []
    for i in range(0, len(active_banners), 2):
        pair = {'main': None, 'potw': None}
        if i < len(active_banners):
            banner1 = active_banners[i]
            if banner1.offer_type == 'main': pair['main'] = banner1
            else: pair['potw'] = banner1

        if i + 1 < len(active_banners):
            banner2 = active_banners[i + 1]
            if banner2.offer_type == 'main': pair['main'] = banner2
            else: pair['potw'] = banner2

        if pair['main'] or pair['potw']:
            banner_pairs.append(pair)

    # Sections
    hero = HeroSection.get_or_create_default()
    features = FeaturesSection.get_or_create_default()
    category = CategorySection.get_or_create_default()

    # Data
    brands = Brand.objects.filter(is_active=True).order_by('order')
    reviews = Review.objects.filter(is_active=True).order_by('order')
    newsletter = NewsletterSetting.objects.last()

    # Products
    products = Product.objects.filter(
        is_active=True,
        is_featured=True
    ).select_related('brand', 'category').order_by('sort_order')[:12]

    # Category names
    categories = [item.get('name') for item in category.items_json]

    # 🔹 2. Create the context dictionary (Defaulting user_obj to None)
    context = {
        'banner_pairs': banner_pairs,
        'hero': hero,
        'features': features,
        'brands': brands,
        'reviews': reviews,
        'newsletter': newsletter,
        'category': category,
        'products': products,
        'categories': categories,
        'user_obj': None,  # Will remain None if they are a guest
    }

    # 🔹 3. Handle the logged-in user logic safely
    session_id = request.session.get('User_id')
    if session_id:
        
        user_obj = UserDetails.objects.filter(id=session_id).first()
        if user_obj:
            context['user_obj'] = user_obj

    # 🔹 4. Return the render (Works safely for both scenarios now!)
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


############## Views start for complete profile ##########################


@login_required
def complete_profile(request):
    if request.method == "POST":
        try:
            data        = json.loads(request.body.decode('utf-8'))
            phone       = data.get('user_phone', '').strip()
            city        = data.get('user_city', '').strip()
            # pincode     = data.get('user_pincode', '').strip()

            if not phone:
                return JsonResponse({'status': '0', 'msg': 'Phone number is required'})

            user_id = request.session.get('User_id')
            user    = UserDetails.objects.get(id=user_id)

            # Check phone not already taken by another user
            if UserDetails.objects.filter(user_phone=phone).exclude(id=user_id).exists():
                return JsonResponse({'status': '0', 'msg': 'Phone number already registered'})

            user.user_phone   = phone
            user.user_city    = city
            # user.user_pincode = pincode   # add this field to your model if not exists
            user.save()

            # Clear the flag
            request.session.pop('show_complete_profile', None)

            return JsonResponse({'status': '1', 'msg': 'Profile completed successfully'})

        except Exception as e:
            return JsonResponse({'status': '0', 'msg': str(e)})
        

############## Views end for complete profile #################################




@csrf_exempt
def login(request):
    session_id = request.session.get('User_id')
    user_type  = request.session.get('user_type')

    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            login_placement = data.get('login_placement')
            login_password  = data.get('login_password')

            login_user = UserDetails.objects.filter(
                Q(user_email=login_placement) | Q(user_phone=login_placement),
                user_password=login_password
            ).first()

            if login_user:
                # ── Normal login session ─────────────────────────────────
                request.session['User_id']   = str(login_user.id)
                request.session['user_type'] = 'User'
                request.session.modified     = True
                send_data = {'status': '1', 'msg': 'Login Successful...'}
            else:
                send_data = {'status': '0', 'msg': 'Invalid Credentials'}

        except Exception as e:
            print(traceback.format_exc())
            send_data = {'status': '0', 'msg': 'Something went wrong', 'error': str(e)}

        return JsonResponse(send_data)

    else:
        # ── Already logged in via normal login ───────────────────────────
        if session_id and user_type == 'User':
            return redirect('index')

        # ── Already logged in via Google OAuth ───────────────────────────
        if request.user.is_authenticated:
            return redirect('index')

        return render(request, 'account/login.html')

        

############### Views start for user logout ##########################

@csrf_exempt
def User_Logout(request):
    try:
        del request.session['User_id']
        return JsonResponse({"status":"1",'msg': 'Logout Successfully '})
    except:
        print(traceback.format_exc())

############# Views end for user logout ################################
    


############# Views start for ajax for register user #######################

@csrf_exempt
def Users_Ajax(request):
    data = request.POST.dict()

    if data.get('id') == "":
        data.pop("id", None)         
        data['user_register_date'] = datetime.today()
        data['user_register_time'] = datetime.now()
        if UserDetails.objects.filter(user_phone=data['user_phone']).exists():
            return JsonResponse({"status":"0", "msg" : f"User already exists .."})
        else:
            UserDetails.objects.create(**data)
            return JsonResponse({"status":"1", "msg" : f"User account has been created successfully"})

    # UPDATE MODE
    # else:
    #     try:
    #         withdraw = WithdrawDetails.objects.get(id=data['id'])
    #     except WithdrawDetails.DoesNotExist:
    #         return JsonResponse({'status': '0', 'msg': 'Withdraw Details not found'})

    #     member = MemberDetails.objects.get(user_id=data['fk_member'])
        
    #     if data['withdraw_status'] == "Done":
    #         if withdraw.is_withdraw == False:
    #             try:
                    
                    
    #                 withdraw.is_withdraw = True
                    

                    
    #                 # STEP 2: DEDUCT withdrawal ONLY from activation
    #                 # if member.user_activation >= withdraw_amount:
    #                 #     member.user_activation -= withdraw_amount  #  DEDUCT ONLY!
                        
    #                 #     super_amount = float(getattr(super_admin, 'super_total_amount', 0) or 0)
    #                 #     super_admin.super_total_amount = super_amount - withdraw_amount
                        
    #                 #     super_admin.save()
    #                 #     member.save()
    #                 #     withdraw.is_withdraw = True
                        
    #                 #     print(f"COMPLETE: Remaining activation ₹{member.user_activation}")
    #                 #     print(f"EARNINGS KEPT: Match=₹{member.user_total_match}, Level=₹{member.user_total_level_amount}")
    #                 # else:
    #                 #     return JsonResponse({
    #                 #         'status': '0', 
    #                 #         'msg': f'Insufficient: ₹{member.user_activation:.2f}'
    #                 #     })
    #             except (ValueError, TypeError) as e:
    #                 print(f"Error: {e}")
    #                 return JsonResponse({'status': '0', 'msg': 'Invalid amount'})

    #     # Donation logic (unchanged)
    #     if withdraw.donation_paid == False:
    #         DonationDetails.objects.create(
    #             donor_id=withdraw.fk_member.user_id,
    #             donor_name=withdraw.fk_member.user_name,
    #             donor_email=withdraw.fk_member.user_email,
    #             donor_phone=withdraw.fk_member.user_phone,
    #             donor_address=withdraw.fk_member.user_address,
    #             donation_amount=data['donation_amount'],
    #             donation_payment_mode="UPI",
    #             donation_status="Done",
    #             donation_date=datetime.today(),
    #             donation_time=datetime.now()
    #         )
    #         withdraw.donation_paid = True

    #     # Update withdraw fields (unchanged)
    #     for key, value in data.items():
    #         if key != 'fk_member':
    #             setattr(withdraw, key, value)

    #     withdraw.save()
    #     return JsonResponse({"status":"1", "msg" : f"Withdraw updated successfully"})

############ Views end for ajax for register user ##############################



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



