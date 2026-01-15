from rest_framework import serializers
from .models import Parcel, ParcelImage, ParcelDocument, NearbyAmenity, Inquiry, ParcelComparison
import json


class ParcelImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelImage
        fields = ['id', 'image', 'caption', 'is_primary', 'order', 'uploaded_at']


class ParcelDocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParcelDocument
        fields = ['id', 'document_type', 'file', 'title', 'description', 'uploaded_at']


class NearbyAmenitySerializer(serializers.ModelSerializer):
    class Meta:
        model = NearbyAmenity
        fields = ['id', 'amenity_type', 'name', 'distance_km', 'latitude', 'longitude']


class InquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inquiry
        fields = ['id', 'parcel', 'name', 'email', 'phone', 'message', 'inquiry_type', 'created_at', 'is_read']
        read_only_fields = ['created_at', 'is_read']


class ParcelListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for list views"""
    geometry = serializers.SerializerMethodField()
    primary_image = serializers.SerializerMethodField()
    
    class Meta:
        model = Parcel
        fields = [
            'id', 'parcel_id', 'title', 'property_type', 'listing_type', 
            'sale_price', 'lease_price_monthly', 'price_per_sqm', 'area_sqm',
            'sub_city', 'wereda', 'street_name', 'landmark', 'status',
            'has_electricity', 'has_water', 'has_sewage', 'is_featured',
            'centroid_lat', 'centroid_lng', 'geometry', 'primary_image',
            'views_count', 'created_at'
        ]
    
    def get_geometry(self, obj):
        try:
            return json.loads(obj.geometry_json)
        except:
            return None
    
    def get_primary_image(self, obj):
        primary = obj.images.filter(is_primary=True).first()
        if primary:
            return self.context['request'].build_absolute_uri(primary.image.url) if primary.image else None
        first_image = obj.images.first()
        if first_image:
            return self.context['request'].build_absolute_uri(first_image.image.url) if first_image.image else None
        return None


class ParcelDetailSerializer(serializers.ModelSerializer):
    """Detailed serializer with all related data"""
    geometry = serializers.SerializerMethodField()
    images = ParcelImageSerializer(many=True, read_only=True)
    documents = ParcelDocumentSerializer(many=True, read_only=True)
    amenities = NearbyAmenitySerializer(many=True, read_only=True)
    
    class Meta:
        model = Parcel
        fields = '__all__'
    
    def get_geometry(self, obj):
        try:
            return json.loads(obj.geometry_json)
        except:
            return None


class ParcelSerializer(serializers.ModelSerializer):
    geometry = serializers.SerializerMethodField()
    images = ParcelImageSerializer(many=True, read_only=True)

    class Meta:
        model = Parcel
        fields = '__all__'

    def get_geometry(self, obj):
        try:
            return json.loads(obj.geometry_json)
        except:
            return None


class ParcelComparisonSerializer(serializers.ModelSerializer):
    parcels = ParcelDetailSerializer(many=True, read_only=True)
    
    class Meta:
        model = ParcelComparison
        fields = ['id', 'user_session', 'parcels', 'created_at']
