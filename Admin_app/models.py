from django.db import models

# Create your models here.


############# Admin Details Modal Starts Here #####################

class AdminDetails(models.Model):
    admin_name = models.CharField(max_length=200,blank=True,null=True)
    admin_email = models.CharField(max_length=200,blank=True,null=True)
    admin_password = models.CharField(max_length=200,blank=True,null=True)
    

    def __str__(self):
        return f"{self.admin_email}-{self.admin_password}"


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


########### Review Modal Starts Here ############################

class Review(models.Model):
    avatar = models.CharField(max_length=10, default='', help_text="Emoji or short text")
    name = models.CharField(max_length=100)
    city = models.CharField(max_length=100, blank=True)
    rating = models.IntegerField(default=5, help_text="1 to 5 stars")
    text = models.TextField()
    
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f"Review by {self.name} ({self.rating} Stars)"

    def to_dict(self):
        return {
            'id': self.id,
            'avatar': self.avatar,
            'name': self.name,
            'city': self.city,
            'rating': self.rating,
            'text': self.text,
            'order': self.order
        }
    
################## Review Modal Ends Here ###############################


############ Newsletter Modal Starts Here ################################

class NewsletterSetting(models.Model):
    heading = models.CharField(max_length=200, default=" Get 15% OFF Your First Order!")
    description = models.TextField(default="Subscribe to receive exclusive deals, new pickle arrivals & Nagpur-only offers straight to your inbox.")
    placeholder = models.CharField(max_length=100, default="Enter your email address...")
    btn_text = models.CharField(max_length=50, default="Subscribe 🎉")
    privacy_note = models.CharField(max_length=200, default="No spam. Unsubscribe anytime. 🔒 Privacy protected.")
    url = models.CharField(max_length=500, default="/newsletter/subscribe/", blank=True)

    def __str__(self):
        return "Global Newsletter Settings"
    
############ Newsletter Modal Ends Here #################################
