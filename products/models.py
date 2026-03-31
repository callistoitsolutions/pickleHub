from django.db import models






# ══════════════════════════════════════════════════════
# 5. PRODUCT
# ══════════════════════════════════════════════════════
class Product(models.Model):
    """
    Individual pickle product shown on the products listing page.
    Links to Brand and Category (FK).
    """

    BADGE_CHOICES = [
        ('Bestseller',   'Bestseller'),
        ('New Arrival',  'New Arrival'),
        ('Premium',      'Premium'),
        ('Hot 🔥',       'Hot 🔥'),
        ('Organic',      'Organic'),
        ('Limited',      'Limited'),
        ('Rare Find',    'Rare Find'),
        ('Nagpur Special','Nagpur Special'),
        ('',             'No Badge'),
    ]

    # ── identity ──
    emoji        = models.CharField(max_length=10, default='🫙')
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    name         = models.CharField(max_length=300)
    slug         = models.SlugField(max_length=300, unique=True)

    # ── relations ──
    brand        = models.ForeignKey(
                       'Admin_app.Brand',
                       on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='products'
                   )
    category     = models.ForeignKey(
                       'Admin_app.CategorySection',        # reuse existing CategorySection
                       on_delete=models.SET_NULL,
                       null=True, blank=True,
                       related_name='products',
                       help_text='Links to CategorySection for filter sidebar'
                   )

    # ── display details ──
    weight       = models.CharField(max_length=100, default='500g')
    oil_type     = models.CharField(max_length=100, default='Mustard Oil')
    region       = models.CharField(max_length=200, blank=True, default='',
                       help_text='e.g. Andhra Pradesh, Rajasthan')
    badge        = models.CharField(max_length=50, choices=BADGE_CHOICES, blank=True, default='')
    badge_color  = models.CharField(max_length=200,
                       default='linear-gradient(135deg,#e85d04,#f48c06)',
                       help_text='CSS gradient for the badge background')
    card_bg      = models.CharField(max_length=200,
                       default='linear-gradient(135deg,#fff3e0,#ffcc80)',
                       help_text='CSS gradient for product card background')

    # ── pricing ──
    price        = models.PositiveIntegerField(default=0, help_text='Sale price in ₹')
    old_price    = models.PositiveIntegerField(default=0, help_text='Original price in ₹')
    discount     = models.CharField(max_length=20, blank=True, default='',
                       help_text='e.g. 29% off — auto-calculated or manual override')

    # ── stock / social proof ──
    stock        = models.PositiveIntegerField(default=100)
    low_stock_threshold = models.PositiveIntegerField(default=20)
    low_stock_label     = models.CharField(max_length=100, blank=True, default='',
                              help_text='e.g. "🔥 Only 12 left" — leave blank to auto-generate')
    rating       = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    review_count = models.PositiveIntegerField(default=0)

    # ── whatsapp ──
    whatsapp_number = models.CharField(max_length=20, default='919876543210',
                          help_text='Without + sign e.g. 919876543210')

    # ── flags ──
    is_active    = models.BooleanField(default=True)
    is_featured  = models.BooleanField(default=False,
                       help_text='Show in Best Sellers / homepage featured grid')
    sort_order   = models.PositiveIntegerField(default=0)
    created_at   = models.DateTimeField(auto_now_add=True)
    updated_at   = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Product'
        verbose_name_plural = 'Products'
        ordering            = ['sort_order', '-created_at']

    def __str__(self):
        return f'{self.emoji} {self.name}'

    # ── helpers ──
    @property
    def discount_pct(self):
        """Auto-calculate discount % from price / old_price."""
        if self.old_price and self.old_price > self.price:
            return int(round((self.old_price - self.price) / self.old_price * 100))
        return 0

    @property
    def discount_label(self):
        """Return manual override if set, otherwise auto-calculate."""
        return self.discount or (f'{self.discount_pct}% off' if self.discount_pct else '')

    @property
    def is_low_stock(self):
        return self.stock <= self.low_stock_threshold

    @property
    def low_stock_text(self):
        if self.low_stock_label:
            return self.low_stock_label
        if self.is_low_stock:
            return f'🔥 Only {self.stock} left'
        return ''

    @property
    def stars_html(self):
        full  = int(self.rating)
        half  = 1 if (self.rating - full) >= 0.5 else 0
        empty = 5 - full - half
        return '★' * full + ('½' if half else '') + '☆' * empty

    def get_absolute_url(self):
        from django.urls import reverse
        return reverse('product_details', kwargs={'slug': self.slug})


# ══════════════════════════════════════════════════════
# 6. PRODUCT PAGE SETTINGS  (filter sidebar config)
# ══════════════════════════════════════════════════════
class ProductPageSettings(models.Model):
    """
    Controls which filter sections are visible on the products listing page
    and their configuration.  Singleton — always use get_or_create_default().
    """
    # ── filter visibility toggles ──
    show_category_filter = models.BooleanField(default=True)
    show_brand_filter    = models.BooleanField(default=True)
    show_price_filter    = models.BooleanField(default=True)
    show_region_filter   = models.BooleanField(default=True)
    show_rating_filter   = models.BooleanField(default=True)
    show_weight_filter   = models.BooleanField(default=True)

    # ── price range config ──
    price_min = models.PositiveIntegerField(default=50)
    price_max = models.PositiveIntegerField(default=800)

    # ── region options (JSON list of {name, count}) ──
    regions_json = models.JSONField(
        default=list,
        help_text='[{"name":"Andhra Pradesh","count":35}, ...]'
    )

    # ── weight options (JSON list of {label}) ──
    weights_json = models.JSONField(
        default=list,
        help_text='[{"label":"100g - 200g"}, ...]'
    )

    # ── page meta ──
    page_title    = models.CharField(max_length=200,
                        default='All Pickles - Shop by Brand, Category & Region | PickleHub Nagpur')
    whatsapp_number = models.CharField(max_length=20, default='919876543210')

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name        = 'Product Page Settings'
        verbose_name_plural = 'Product Page Settings'

    def __str__(self):
        return f'Product Page Settings (updated {self.updated_at.strftime("%d %b %Y %H:%M")})'

    @classmethod
    def get_or_create_default(cls):
        obj = cls.objects.first()
        if obj is None:
            obj = cls.objects.create(
                regions_json=[
                    {'name': 'Andhra Pradesh', 'count': 35},
                    {'name': 'Rajasthan',       'count': 28},
                    {'name': 'Punjab',          'count': 16},
                    {'name': 'Gujarat',         'count': 19},
                    {'name': 'Kerala',          'count': 14},
                ],
                weights_json=[
                    {'label': '100g - 200g'},
                    {'label': '250g - 500g'},
                    {'label': '500g - 1kg'},
                    {'label': '1kg+'},
                ],
            )
        return obj
