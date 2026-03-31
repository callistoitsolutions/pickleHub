# views.py
# PickleHub – Hero Section Views
# UPDATED: buttons_json replaces fixed btn_primary/secondary/whatsapp fields.
# NO forms.py used — data read directly from request.body (JSON).

import json
from django.shortcuts import render,HttpResponse,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from core.models import HeroSection,FeaturesSection
from django.db import transaction
from Admin_app.models import *
from django.views.decorators.csrf import csrf_exempt
import traceback


# ──────────────────────────────────────────────
# 1. PUBLIC HOME PAGE
# ──────────────────────────────────────────────

def dashboard(request):
    session_id = request.session.get('Admin_id')
    if session_id:
        admin_obj = AdminDetails.objects.get(id=session_id)

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
            'admin_obj':admin_obj
        })
    else:
        return render(request,'Admin_pages/admin_login.html')
# ──────────────────────────────────────────────
# 2. ADMIN HOME PAGE
# ──────────────────────────────────────────────


############## Views start for admin login #####################

@csrf_exempt
def Admin_Login(request):
    session_id = request.session.get('Admin_id')
    user_type = request.session.get('user_type')
    if request.method == "POST":
        try:
            data = json.loads(request.body.decode('utf-8'))
            admin_email = data['admin_email']
            admin_password = data['admin_password']

            if AdminDetails.objects.filter(admin_email=admin_email, admin_password=admin_password):

                obj = AdminDetails.objects.get(admin_email=admin_email, admin_password=admin_password)
                
                request.session['Admin_id'] = str(obj.id)
                request.session['user_type'] = str('Admin')

                send_data = {'status':1,'msg':'Login Successful...'}
            else:
                send_data = {'status':0,'msg':'Invalid Credentials'}
        except:
            print(traceback.format_exc())
            send_data = {'status':0 , 'msg':'Something went wrong','error':traceback.format_exc()}
        return JsonResponse(send_data)
    else:
        if session_id and user_type == "Admin":
            return redirect('dashboard')
        else:
            return render(request,'Admin_pages/admin_login.html')

########## Views end for admin login ########################


############### Views start for offer banner section ######################

def Offer_Banner_Section(request):
    active_banners = OfferBanner.objects.filter(is_active=True).order_by('order', '-created_at')

    # 1. Create the standard Python list
    banners_list = [banner.to_dict() for banner in active_banners]

    # 2. DO NOT use json.dumps(banners_list) here! 
    # Just pass the raw Python list directly into the context.
    context = {
        'offers_list': banners_list, 
    }

    return render(request,'Admin_pages/Offer_Banner/offer_banner.html',context)

######### Views end for offer banner section ##################################


############ Views start for ajax for save offer banner ########################

@csrf_exempt
def Save_Offer_Ajax(request):
    try:
        data = json.loads(request.body)
        
        with transaction.atomic():
            
            # 1. Get the IDs of the banners that are STILL on the screen
            incoming_ids = [offer.get('id') for offer in data if offer.get('id')]
            
            # 2. TARGETED DELETE: Delete ONLY the rows in the database that are missing from the screen
            OfferBanner.objects.exclude(id__in=incoming_ids).delete()
            
            # 3. Update existing banners or create brand new ones
            for index, offer in enumerate(data):
                offer_id = offer.get('id')
                
                # Set up the base fields every banner shares
                defaults = {
                    'name': offer.get('name', ''),
                    'price': offer.get('price', 0) or 0,
                    'old_price': offer.get('oldPrice') or None,
                    'url': offer.get('url', ''),
                    'order': index, # Saves the exact sequence
                    'is_active': True
                }
                
                # Add the specific fields depending on the banner type
                if offer.get('type') == 'main':
                    defaults.update({
                        'offer_type': 'main',
                        'badge': offer.get('badge', ''),
                        'description': offer.get('desc', ''),
                        'discount_label': offer.get('discount', ''),
                    })
                else:
                    defaults.update({
                        'offer_type': 'potw',
                        'emoji': offer.get('emoji', '🧄'),
                        'weight_type': offer.get('weight', ''),
                    })
                
                # If the banner has an ID, it already exists -> UPDATE IT
                if offer_id:
                    OfferBanner.objects.filter(id=offer_id).update(**defaults)
                
                # If it doesn't have an ID, it was just added -> CREATE IT
                else:
                    OfferBanner.objects.create(**defaults)
            
        return JsonResponse({"status": "success", "message": "Banners synced perfectly!"})
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

########### Views end for ajax for save offer banner ############################


########### Views start for brand section ############################

def Brand_Section(request):
    active_brands = Brand.objects.filter(is_active=True).order_by('order')
    brands_list = [brand.to_dict() for brand in active_brands]

    # 2. DO NOT use json.dumps(banners_list) here! 
    # Just pass the raw Python list directly into the context.
    context = {
        'brands_list': brands_list, 
    }

    return render(request,'Admin_pages/Brand/brand.html',context)

############# Views end for brand section ##############################


########### Views start for ajax for save brands ########################

@csrf_exempt
def Save_Brand_Ajax(request):
    try:
        data = json.loads(request.body)
        
        with transaction.atomic():
            # 1. Get IDs of kept brands
            incoming_ids = [brand.get('id') for brand in data if brand.get('id')]
            
            # 2. Delete removed brands
            Brand.objects.exclude(id__in=incoming_ids).delete()
            
            # 3. Update or Create
            for index, brand in enumerate(data):
                brand_id = brand.get('id')
                defaults = {
                    'emoji': brand.get('emoji', ''),
                    'name': brand.get('name', ''),
                    'url': brand.get('url', ''),
                    'order': index,
                    'is_active': True
                }
                
                if brand_id:
                    Brand.objects.filter(id=brand_id).update(**defaults)
                else:
                    Brand.objects.create(**defaults)
            
        return JsonResponse({"status": "success", "message": "Brands synced!"})
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

############# Views end for ajax for save brands ########################


############## Views start for review section #######################

def Review_Section(request):
    active_reviews = Review.objects.filter(is_active=True).order_by('order')
    reviews_list = [review.to_dict() for review in active_reviews]

    # # 2. DO NOT use json.dumps(banners_list) here! 
    # # Just pass the raw Python list directly into the context.
    context = {
        'reviews_list': reviews_list, 
    }

    return render(request,'Admin_pages/Review/review.html',context)

########### Views end for review section ###########################


############## Views start for ajax for save reviews #######################

@csrf_exempt
def Save_Review_Ajax(request):
    try:
        data = json.loads(request.body)

        with transaction.atomic():
            # 1. Get IDs of kept reviews
            incoming_ids = [review.get('id') for review in data if review.get('id')]
            
            # 2. Delete removed reviews (Targeted Delete)
            Review.objects.exclude(id__in=incoming_ids).delete()
            
            # 3. Update or Create existing reviews
            for index, review in enumerate(data):
                review_id = review.get('id')
                defaults = {
                    'avatar': review.get('avatar', '👤'),
                    'name': review.get('name', ''),
                    'city': review.get('city', ''),
                    'rating': int(review.get('rating', 5)), # Ensure this is an integer!
                    'text': review.get('text', ''),
                    'order': index,
                    'is_active': True
                }
                
                if review_id:
                    Review.objects.filter(id=review_id).update(**defaults)
                else:
                    Review.objects.create(**defaults)
                    
        return JsonResponse({"status": "success", "message": "Reviews synced!"})
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

############# Views end for ajax for save reviews #########################


############# Views start for newsletter section ############################

def Newsletter_Section(request):
    newsletter = NewsletterSetting.objects.first()

    context={
        'newsletter':newsletter
    }

    return render(request,'Admin_pages/Newsletter/newsletter.html',context)

############### Views end for newsletter section #############################


########### Views start for ajax for save newsletter #######################

@csrf_exempt
def Save_Newsletter_Ajax(request):
    try:
        data = json.loads(request.body)
        
        # Grab the one row, update it, and save it
        settings, created = NewsletterSetting.objects.get_or_create(id=1)
        
        settings.heading = data.get('heading', '')
        settings.description = data.get('desc', '')
        settings.placeholder = data.get('placeholder', '')
        settings.btn_text = data.get('btnText', '')
        settings.privacy_note = data.get('privacy', '')
        settings.url = data.get('url', '')
        settings.save()
        
        # 👇 THIS is what JavaScript is looking for!
        return JsonResponse({"status": "success", "message": "Newsletter saved!"})
        
    except Exception as e:
        return JsonResponse({"status": "error", "message": str(e)}, status=400)

########### Views end for ajax for save newsletter ############################

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
