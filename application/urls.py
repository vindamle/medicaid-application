from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup.as_view(), name='signup'),
    path('create/', views.create.as_view(), name = 'create'),
    path('ajax/track_or_ignore/' ,views.update_list , name = "update_list"),
    path('ajax/approval_verified/', views.approval_verified, name = 'approval_verified'),
    path('ajax/update_resident/', views.update_resident, name = 'update_resident'),
    path('ajax/update_application/', views.update_application, name = 'update_application'),
    path('ajax/update_alert/', views.update_alert, name = 'update_alert')

]
