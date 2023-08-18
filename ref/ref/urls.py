"""ref URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

from django.urls import path
from app.views import send_auth_code, verify_auth_code, update_invite_code, profile

urlpatterns = [
    path('api/send_auth_code/', send_auth_code, name='send_auth_code'),
    path('api/verify_auth_code/', verify_auth_code, name='verify_auth_code'),
    path('api/update_invite_code/', update_invite_code, name='update_invite_code'),
    path('api/profile/', profile, name='profile'),
]
