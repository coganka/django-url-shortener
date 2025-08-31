from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LinkViewSet, redirect_view, preview_view, qr_view


router = DefaultRouter()
router.register(r"links", LinkViewSet, basename="link")

urlpatterns = [
    path("api/", include(router.urls)),
    path("<slug:alias>/", redirect_view, name="redirect"),
    path("p/<slug:alias>/", preview_view, name="preview"),
    path("q/<slug:alias>.png", qr_view, name="qr"),
]