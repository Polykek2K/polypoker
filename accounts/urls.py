from django.urls import path
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('p/<str:username>/', views.profile, name='profile'),
    path('p/<slug:id>/edit', views.Edit.as_view(), name='edit')
]
