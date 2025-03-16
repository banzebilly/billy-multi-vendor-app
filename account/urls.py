
from django.urls import path, include
from .import views




urlpatterns = [
    path('', views.myAccount),
    path('register_User/', views.register_User, name="register_User"),
    path('register_vendor/', views.register_vendor, name="register_vendor"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('myAccount/', views.myAccount, name="myAccount"),
    path('customer_dashboard/', views.customer_dashboard, name="customer_dashboard"),
    path('vendor_dashboard/', views.vendor_dashboard, name="vendor_dashboard"),

    #============account activations link==================
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    #forgot password url start here==================================
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/', views.reset_password_validate, name='reset_password_validate'),
    path('reset_password/', views.reset_password, name='reset_password'),


    #---------------------vendor url start here-----------------------
    path('vendor/', include('vendor_app.urls')),

]
