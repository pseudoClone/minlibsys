from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from borrowing.views import BorrowingViewSet
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
)
from book.views import BookViewSet
from member.views import MemberRegistrationView

router = DefaultRouter()
router.register(r"borrowings", BorrowingViewSet, basename="borrowing")
router.register(r"books", BookViewSet, basename="book")

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include(router.urls)),
    path(
        "api-auth/",
        include("rest_framework.urls", namespace="rest_framework"),
    ),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/register/", MemberRegistrationView.as_view(), name="registration"
    ),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
]
