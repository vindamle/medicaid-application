from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup.as_view(), name='signup'),
    path('create/', views.create.as_view(), name = 'create'),
    # path('activity/', views.create.as_view(), name = 'activity'),

]
