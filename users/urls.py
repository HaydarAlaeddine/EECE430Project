from django.urls import path, include 
from .views import sign_up,take_appointment,view_profile,get_file
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', sign_up,name='signup'),
    path('login/',auth_views.LoginView.as_view(template_name='users/login.html'),name='login'),
    path('logout/',auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('appointments/',take_appointment,name='appointment'),
    path('profile/',view_profile,name='profile'),
    path('profile/files/<str:description>',get_file,name='get-file')
]
