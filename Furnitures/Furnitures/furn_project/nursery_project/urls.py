"""
URL configuration for nursery_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from plants import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('home/', views.home, name='home'),
    path('admin-page/', views.admin_page, name='admin_page'),
    path('add-plant/', views.add_plant, name='add_plant'),
    path('view-plant/<int:id>/', views.view_plant, name='view_plant'),
    path('edit-plant/<int:id>/', views.edit_plant, name='edit_plant'),
    path('delete-plant/<int:id>/', views.delete_plant, name='delete_plant'),
    path('all-plants/', views.view_all_plants, name='view_all_plants'),
    # Add this in your urlpatterns
path('us-view-plants/', views.us_view_plants, name='us_view_plants'),
path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
path('remove-from-cart/', views.remove_from_cart, name='remove_from_cart'),
    path('plant-details/<int:id>/', views.us_view_plant_details, name='us_view_plant_details'),
    
    # Buy Plant
path('buy-plant/<int:id>/', views.buy_plant, name='buy_plant'),

# Dummy online payment page
path('online-payment/<int:booking_id>/', views.online_payment, name='online_payment'),

# Congratulations / order success page
path('order-success/<int:booking_id>/', views.order_success, name='order_success'),
path('my-orders/', views.user_my_orders, name='user_my_orders'),
path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
path('logout/', views.user_logout, name='logout'),

    path('admin-manage-orders/', views.admin_manage_orders, name='admin_manage_orders'),
    path('mark-delivered/<int:booking_id>/', views.mark_delivered, name='mark_delivered'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    
 path('manage-orders/', views.admin_manage_orders, name='admin_manage_orders'),
path('mark-delivered/<int:id>/', views.mark_delivered, name='mark_delivered'),
path('cancel-booking/<int:id>/', views.cancel_booking, name='cancel_booking'),
path('delete-booking/<int:id>/', views.delete_booking, name='delete_booking'),
path('edit-booking/<int:id>/', views.edit_booking, name='edit_booking'),

 path('services/', views.services_view, name='services'),
 path('about/', views.about, name='about'),
 path('contact/', views.contact, name='contact'),
  path('admin/user-issues/', views.admin_user_issues, name='admin_user_issues'),
  path('plants/', views.user_view_home_plants, name='user_view_home_plants'),
   path('plant/<int:id>/', views.plant_detail, name='plant_detail'),
   path('deliver-booking/<int:id>/', views.deliver_booking, name='deliver_booking'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)