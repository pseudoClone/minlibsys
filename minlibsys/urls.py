from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from borrowing.views import BorrowingViewSet

router = DefaultRouter()
router.register(r"borrowings", BorrowingViewSet, basename="borrowing")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api-auth/", include("rest_framework.urls", namespace="rest_framework")
    ),
]
