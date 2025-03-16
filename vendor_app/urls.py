
from django.urls import path, include
from .import views
from account import views as AcountViews


urlpatterns = [
    path('',  AcountViews.vendor_dashboard, name="vendor"),
    path('profile/', views.v_profile, name="v_profile"),
    path('menu_builder/', views.menu_builder, name="menu_builder"),
    path('menu_builder/category/<int:pk>/', views.fooditems_by_category, name='fooditems_by_category'),

        # Category CRUD
    path('menu-builder/category/add/', views.add_category, name='add_category'),
    path('menu-builder/category/edit/<int:pk>/', views.edit_category, name='edit_category'),
    path('menu-builder/category/delete/<int:pk>/', views.delete_category, name='delete_category'),

      # FoodItem CRUD
    path('menu-builder/food/add/', views.add_food, name='add_food'),
    path('menu-builder/food/edit/<int:pk>/', views.edit_food, name='edit_food'),
    path('menu-builder/food/delete/<int:pk>/', views.delete_food, name='delete_food'),

]
