from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_view, name='index'),
    
    path('products', views.products, name='products'),
    
    path('account', views.login, name='login'),
    
    path('cart', views.cart, name='cart'),
    
    path('product', views.product_details, name='product_details'),
    
    path('payments', views.checkout, name='checkout'),
    
    path('contact', views.contact, name='contact'),
    
    path('api/hero/save/',        views.save_hero,   name='save_hero'),
    path('api/hero/load/',        views.load_hero,   name='load_hero'),
    path('api/features/save/',     views.save_features, name='save_features'),
]