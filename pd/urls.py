from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from wordbox import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landing, name='landing'),
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
    path('accounts/signup/', views.signup, name='signup'),
    path('wordbox/', include('wordbox.urls')),
    path('', include('wordbox.urls')),
]
