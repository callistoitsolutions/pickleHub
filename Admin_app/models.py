from django.db import models

# Create your models here.


############ Offer Banner Modal Starts Here ####################

class OfferBanner(models.Model):
    OFFER_TYPES = (
        ('main', 'Main Offer Banner'),
        ('potw', 'Pickle of the Week'),
    )

    # Core Shared Fields
    offer_type = models.CharField(max_length=10, choices=OFFER_TYPES, default='main')
    name = models.CharField(max_length=200, help_text="Product name (e.g., Andhra Avakaya Mango Pickle)")
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Sale price (₹)")
    old_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, help_text="Original crossed-out price (₹)")
    url = models.CharField(max_length=255, blank=True, null=True, help_text="Relative URL or full link (e.g., /product/mango-pickle/)")
    
    #  Main Offer Specific Fields
    badge = models.CharField(max_length=50, blank=True, null=True, help_text="e.g., 🔥 LIMITED STOCK")
    description = models.CharField(max_length=255, blank=True, null=True, help_text="Short description for the main offer")
    discount_label = models.CharField(max_length=30, blank=True, null=True, help_text="e.g., 33% OFF")

    #  Pickle of the Week Specific Fields
    emoji = models.CharField(max_length=10, blank=True, null=True, default="", help_text="Emoji for the POTW banner")
    weight_type = models.CharField(max_length=100, blank=True, null=True, help_text="e.g., 500g | Traditional Recipe")

    # Management Fields
    order = models.PositiveIntegerField(default=0, help_text="Controls the sequence they appear on the frontend")
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this banner from the frontend")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['order', '-created_at']
        verbose_name = "Offer Banner"
        verbose_name_plural = "Offer Banners"

    def __str__(self):
        return f"[{self.get_offer_type_display()}] {self.name}"

    def to_dict(self):
        """
        Helper method to easily serialize this model instance into the JSON 
        format your JavaScript expects for window.STATE.offers.
        """
        base_dict = {
            'id': self.id,
            'type': self.offer_type,
            'name': self.name,
            'price': str(self.price), # Convert Decimal to string for JS
            'oldPrice': str(self.old_price) if self.old_price else '',
            'url': self.url or '',
        }

        if self.offer_type == 'main':
            base_dict.update({
                'badge': self.badge or '',
                'desc': self.description or '',
                'discount': self.discount_label or '',
            })
        else:
            base_dict.update({
                'emoji': self.emoji or '',
                'weight': self.weight_type or '',
            })
            
        return base_dict
    
############## Offer Banner Modal Ends Here ############################


############# Brand Modal Starts Here #################################

class Brand(models.Model):
    emoji = models.CharField(max_length=10, default="")
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=255, blank=True, null=True)
    
    # Management Fields
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', '-created_at']

    def __str__(self):
        return f"{self.emoji} {self.name}"

    def to_dict(self):
        return {
            'id': self.id,
            'emoji': self.emoji,
            'name': self.name,
            'url': self.url or ''
        }
    
############ Brand Modal Ends Here #################################
