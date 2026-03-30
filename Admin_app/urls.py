from django.urls import path
from . import views

urlpatterns = [
    
    path('hero_section', views.hero_section, name='hero_section'),
    path('feature_section', views.feature_section, name='feature_section'),
    path('dashboard/', views.dashboard, name='dashboard'),
]