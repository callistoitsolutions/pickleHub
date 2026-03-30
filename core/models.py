# models.py
# PickleHub – Hero Section Model
# Stores all hero section data as JSON fields for flexibility.
# Run: python manage.py makemigrations && python manage.py migrate

from django.db import models


class HeroSection(models.Model):
    """
    Stores all hero section settings for the home page.
    Each field maps to an input in the admin builder.
    JSON fields store dynamic lists (stats, float badges).
    """

    # ── Basic Text ──────────────────────────────────────────────
    badge_text          = models.CharField(max_length=200, default="🏆 Nagpur's #1 Pickle Store")
    title_line1         = models.CharField(max_length=200, default="Discover")
    title_highlight     = models.CharField(max_length=200, default="Rare & Exclusive")
    title_line2         = models.CharField(max_length=200, default="Pickle Brands")
    subtitle            = models.TextField(
        default="Handpicked regional pickles from Andhra, Rajasthan, Punjab & more — "
                "not available in local stores. Order online with 24-hour delivery across Nagpur."
    )

    # ── Buttons ─────────────────────────────────────────────────
    btn_primary_text    = models.CharField(max_length=100, default="🛍️ Shop Now")
    btn_primary_url     = models.CharField(max_length=300, default="/products/")
    btn_secondary_text  = models.CharField(max_length=100, default="💬 Order on WhatsApp")
    whatsapp_number     = models.CharField(max_length=20, default="919876543210")

    # ── Jar Emoji (floating right) ───────────────────────────────
    jar_emoji           = models.CharField(max_length=10, default="🫙")

    # ── Dynamic Lists stored as JSON ─────────────────────────────
    # stats: [{"num": "50+", "lbl": "Pickle Brands"}, ...]
    stats_json          = models.JSONField(default=list)

    # float_badges: ["🌶️ Extra Spicy", "✅ 100% Natural", ...]
    float_badges_json   = models.JSONField(default=list)

    # ── Visibility toggle ────────────────────────────────────────
    is_visible          = models.BooleanField(default=True)

    # ── Meta ─────────────────────────────────────────────────────
    updated_at          = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = "Hero Section"
        verbose_name_plural = "Hero Section"

    def __str__(self):
        return f"Hero Section (updated {self.updated_at.strftime('%d %b %Y %H:%M')})"

    @classmethod
    def get_or_create_default(cls):
        """
        Returns the single HeroSection row, creating it with defaults if missing.
        Call this in every view instead of .objects.first().
        """
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create(
                stats_json=[
                    {"num": "50+",   "lbl": "Pickle Brands"},
                    {"num": "200+",  "lbl": "Products"},
                    {"num": "5000+", "lbl": "Happy Customers"},
                    {"num": "24Hr",  "lbl": "Delivery"},
                ],
                float_badges_json=[
                    "🌶️ Extra Spicy",
                    "✅ 100% Natural",
                    "🚚 Free Delivery",
                ],
            )
        return obj