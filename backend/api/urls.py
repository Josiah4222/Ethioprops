from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    ParcelViewSet, InquiryViewSet, ParcelImageViewSet, 
    ParcelDocumentViewSet, NearbyAmenityViewSet
)

router = DefaultRouter()
router.register(r'parcels', ParcelViewSet)
router.register(r'inquiries', InquiryViewSet)
router.register(r'parcel-images', ParcelImageViewSet)
router.register(r'parcel-documents', ParcelDocumentViewSet)
router.register(r'nearby-amenities', NearbyAmenityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
