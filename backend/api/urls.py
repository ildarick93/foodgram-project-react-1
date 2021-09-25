from rest_framework.authtoken import views
from django.urls import path, include

urlpatterns = [
    path('', include('users.urls')),
    path('', include('recipes.urls')),
    path('v1/auth/', include('djoser.urls.authtoken')),
] 