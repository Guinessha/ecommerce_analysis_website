from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import upload_file, dashboard

router = DefaultRouter()

urlpatterns = [
    path('api/', include(router.urls)),
    path('upload/', upload_file, name='upload'),
    path('dashboard/', dashboard, name='dashboard'),
]
