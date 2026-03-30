# models.py
# PickleHub – HeroSection + FeaturesSection
# Run: python manage.py makemigrations && python manage.py migrate

from django.db import models


# ══════════════════════════════════════════════════════
# 1. HERO SECTION  (unchanged from previous version)
# ══════════════════════════════════════════════════════
class HeroSection(models.Model):
    badge_text        = models.CharField(max_length=200, default="🏆 Nagpur's #1 Pickle Store")
    title_line1       = models.CharField(max_length=200, default="Discover")
    title_highlight   = models.CharField(max_length=200, default="Rare & Exclusive")
    title_line2       = models.CharField(max_length=200, default="Pickle Brands")
    subtitle          = models.TextField(
        default="Handpicked regional pickles from Andhra, Rajasthan, Punjab & more — "
                "not available in local stores. Order online with 24-hour delivery across Nagpur."
    )
    jar_emoji         = models.CharField(max_length=10, default="🫙")
    hero_image_url    = models.TextField(blank=True, default="")

    # Dynamic lists
    buttons_json      = models.JSONField(default=list)   # [{icon, text, url, type}, ...]
    stats_json        = models.JSONField(default=list)   # [{num, lbl}, ...]
    float_badges_json = models.JSONField(default=list)   # ["🌶️ Extra Spicy", ...]

    is_visible        = models.BooleanField(default=True)
    updated_at        = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return f"Hero Section (updated {self.updated_at.strftime('%d %b %Y %H:%M')})"

    @classmethod
    def get_or_create_default(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create(
                buttons_json=[
                    {"icon": "fa-shopping-bag", "text": "Shop Now",          "url": "/products/",                 "type": "primary"},
                    {"icon": "fa-whatsapp",     "text": "Order on WhatsApp", "url": "https://wa.me/919876543210", "type": "secondary"},
                ],
                stats_json=[
                    {"num": "50+",   "lbl": "Pickle Brands"},
                    {"num": "200+",  "lbl": "Products"},
                    {"num": "5000+", "lbl": "Happy Customers"},
                    {"num": "24Hr",  "lbl": "Delivery"},
                ],
                float_badges_json=["🌶️ Extra Spicy", "✅ 100% Natural", "🚚 Free Delivery"],
            )
        return obj


# ══════════════════════════════════════════════════════
# 2. FEATURES SECTION  (NEW)
# ══════════════════════════════════════════════════════
class FeaturesSection(models.Model):
    """
    Stores the Features Strip section shown below the hero.
    items_json holds the list of feature cards — each card has:
        {
            "ico":   "🚚",
            "title": "Free Delivery",
            "sub":   "Orders above ₹499"
        }
    Admin can add / edit / remove / reorder these from the builder.
    """
    # Dynamic list of feature cards
    items_json = models.JSONField(
        default=list,
        help_text='List of feature cards: [{"ico":"🚚","title":"Free Delivery","sub":"Orders above ₹499"}, ...]'
    )

    is_visible = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Features Section"
        verbose_name_plural = "Features Section"

    def __str__(self):
        return f"Features Section (updated {self.updated_at.strftime('%d %b %Y %H:%M')})"

    @classmethod
    def get_or_create_default(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create(
                items_json=[
                    {"ico": "🚚", "title": "Free Delivery",  "sub": "Orders above ₹499"},
                    {"ico": "🌿", "title": "100% Natural",   "sub": "No preservatives"},
                    {"ico": "🔄", "title": "Easy Returns",   "sub": "7-day return policy"},
                    {"ico": "🔒", "title": "Secure Payment", "sub": "UPI / Razorpay / COD"},
                ]
            )
        return obj