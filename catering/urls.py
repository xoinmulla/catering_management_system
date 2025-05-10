from django.urls import path
from .views import add_client, client_list ,add_event,contact,home
from . import views


urlpatterns = [
    path('add-client/', add_client, name='add_client'),
    path('clients/', client_list, name='client_list'),  # ✅ Ensure this exists
    path('add-event/', add_event, name='add_event'),
    path("contact/", contact, name="contact"),
    path("home/", home, name="home"),
    path('staff/', views.staff_list, name='staff_list'),
    path('staff/add/', views.add_staff, name='add_staff'),
    path('staff/delete/<int:staff_id>/', views.delete_staff, name='delete_staff'),
    path('staff/edit/<int:staff_id>/', views.edit_staff, name='edit_staff'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    path('reset-password/<uidb64>/<token>/', views.reset_password_view, name='reset_password'),

]
