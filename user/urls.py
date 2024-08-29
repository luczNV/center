from django.urls import path
from .views import register_view,home,login_view,profile_view,logout_view
app_name = 'usuarios'
urlpatterns = [
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('profile/', profile_view, name='profile'),
    path('logout/', logout_view, name='logout'),
]