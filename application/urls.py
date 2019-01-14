from django.urls import path
from . import views

urlpatterns = [

    # path('create/', views.create.as_view(), name = 'create'),
    path('ajax/track_or_ignore/' ,views.update_list , name = "update_list"),
    path('ajax/approval_verified/', views.approval_verified, name = 'approval_verified'),
    path('ajax/update_resident/', views.update_resident, name = 'update_resident'),
    path('ajax/update_application/', views.update_application, name = 'update_application'),
    path('ajax/update_alert/', views.update_alert, name = 'update_alert'),
    path('ajax/phase_change/', views.phase_change, name = 'phase_change'),
    path('ajax/update_rfi/', views.update_rfi, name = 'update_rfi'),
    path('ajax/create_response/', views.create_response, name = 'create_response'),


]
