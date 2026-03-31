from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='index'),
    
   # path('products', views.products, name='products'),
   
   path('All_products', views.All_products, name='All_products'),
    
    path('account', views.login, name='login'),
    
    path('cart', views.cart, name='cart'),
    
    #path('product_details', views.product_details, name='product_details'),
    path('products/<slug:slug>/', views.product_details, name='product_details'),
    
    path('payments', views.checkout, name='checkout'),
    
    path('contact', views.contact, name='contact'),
    
    
    path('api/hero/load/',                  views.load_hero,        name='load_hero'),
    path('api/category/load/',              views.load_category,    name='load_category'), 
    
    path('api/hero/save/',                  views.save_hero,        name='save_hero'),
    path('api/features/save/',              views.save_features,    name='save_features'),
    path('api/category/save/',              views.save_category,    name='save_category'),  
]