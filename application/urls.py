from django.urls import path
from . import views

urlpatterns = [

    # path('create/', views.create.as_view(), name = 'create'),
    path('ajax/track_or_ignore/' ,views.track_untrack_resident , name = "track_untrack_resident"),
    path('ajax/application_tracking/', views.application_tracking, name = 'application_tracking'),
    path('ajax/approval_verified/', views.approval_verified, name = 'approval_verified'),
    path('ajax/update_resident/', views.update_resident, name = 'update_resident'),
    path('ajax/update_application/', views.update_application, name = 'update_application'),
    path('ajax/update_confirmation/', views.update_confirmation, name = 'update_confirmation'),
    path('ajax/update_alert/', views.update_alert, name = 'update_alert'),
    path('ajax/phase_change/', views.phase_change, name = 'phase_change'),
    path('ajax/update_rfi/', views.update_rfi, name = 'update_rfi'),
    path('ajax/create_response/', views.create_response, name = 'create_response'),
    path('ajax/create_nami/', views.create_nami, name = 'create_nami'),
    path('ajax/update_approval/', views.update_approval, name = 'update_approval'),
    path('ajax/update_denial/', views.update_denial, name = 'update_denial'),
    path('ajax/update_nami/', views.update_nami, name = 'update_nami'),
    path('ajax/delete_nami/', views.delete_nami, name = 'delete_nami'),
    path('ajax/create_application/', views.create_application, name = 'create_application'),
    path('ajax/delete_response/', views.delete_response, name = 'delete_response'),
    path('ajax/create_fair_hearing/', views.create_fair_hearing, name = 'create_fair_hearing'),
    path('ajax/update_fair_hearing/', views.update_fair_hearing, name = 'update_fair_hearing'),
    path('ajax/delete_fair_hearing/', views.delete_fair_hearing, name = 'delete_fair_hearing'),
    path('ajax/update_document/', views.update_document, name = 'update_document'),
    path('ajax/get_app_deadline/', views.get_app_deadline, name = 'get_app_deadline'),
]
