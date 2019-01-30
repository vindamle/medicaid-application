"""app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.urls import path, include
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name = 'login'),
    path('', include('django.contrib.auth.urls')),

    path('admin/', admin.site.urls),
    path('pending/', PendingView.as_view(), name='pending'),
    path('', ActivityView.as_view(), name = 'home'),
    path('pending_alerts/', PendingAlertsView.as_view(), name = 'pending_alerts'),
    path('not_tracking/', NotTrackingView.as_view(), name = 'not_tracking'),
    path('show/', ShowView.as_view(), name = 'show'),
    path('approvals/', ApprovalsView.as_view(), name = 'approvals'),
    path('application/', include('application.urls')),


]
