from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup.as_view(), name='signup'),
    path('create/', views.create.as_view(), name = 'create'),
    path('ajax/track_or_ignore/' ,views.update_list , name = "update_list"),
    path('ajax/file_uploader/', views.file_upload, name = 'file_upload')

]
