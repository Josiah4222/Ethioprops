from django.contrib import admin
from .models import Parcel, ParcelImage, ParcelDocument, NearbyAmenity, Inquiry, ParcelComparison


class ParcelImageInline(admin.TabularInline):
    model = ParcelImage
    extra = 1


class ParcelDocumentInline(admin.TabularInline):
    model = ParcelDocument
    extra = 1


class NearbyAmenityInline(admin.TabularInline):
    model = NearbyAmenity
    extra = 1


@admin.register(Parcel)
class ParcelAdmin(admin.ModelAdmin):
    list_display = ['parcel_id', 'title', 'property_type', 'listing_type', 'sale_price', 'sub_city', 'status', 'is_featured', 'views_count']
    list_filter = ['property_type', 'listing_type', 'status', 'is_featured', 'sub_city', 'has_electricity', 'has_water', 'has_sewage']
    search_fields = ['parcel_id', 'title', 'description', 'sub_city', 'wereda', 'street_name']
    inlines = [ParcelImageInline, ParcelDocumentInline, NearbyAmenityInline]
    readonly_fields = ['views_count', 'price_per_sqm', 'created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('parcel_id', 'title', 'description', 'property_type', 'listing_type', 'status', 'is_featured')
        }),
        ('Location', {
            'fields': ('country', 'city', 'sub_city', 'wereda', 'street_name', 'house_number', 'landmark')
        }),
        ('Coordinates', {
            'fields': ('centroid_lat', 'centroid_lng', 'entry_lat', 'entry_lng', 'geometry_json')
        }),
        ('Size & Dimensions', {
            'fields': ('area_sqm', 'dimensions', 'adjacent_info', 'zoning_info')
        }),
        ('Pricing', {
            'fields': ('sale_price', 'lease_price_monthly', 'lease_price_yearly', 'price_per_sqm', 'is_negotiable', 'currency')
        }),
        ('Infrastructure', {
            'fields': ('road_access', 'has_electricity', 'has_water', 'has_sewage')
        }),
        ('Ownership', {
            'fields': ('owner_name', 'owner_phone', 'owner_email', 'title_deed_ref', 'usage_restrictions', 'survey_date')
        }),
        ('Statistics', {
            'fields': ('views_count', 'created_at', 'updated_at')
        }),
    )


@admin.register(ParcelImage)
class ParcelImageAdmin(admin.ModelAdmin):
    list_display = ['parcel', 'caption', 'is_primary', 'order', 'uploaded_at']
    list_filter = ['is_primary', 'uploaded_at']
    search_fields = ['parcel__parcel_id', 'caption']


@admin.register(ParcelDocument)
class ParcelDocumentAdmin(admin.ModelAdmin):
    list_display = ['parcel', 'document_type', 'title', 'uploaded_at']
    list_filter = ['document_type', 'uploaded_at']
    search_fields = ['parcel__parcel_id', 'title']


@admin.register(NearbyAmenity)
class NearbyAmenityAdmin(admin.ModelAdmin):
    list_display = ['parcel', 'amenity_type', 'name', 'distance_km']
    list_filter = ['amenity_type']
    search_fields = ['parcel__parcel_id', 'name']


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ['parcel', 'name', 'email', 'inquiry_type', 'created_at', 'is_read']
    list_filter = ['inquiry_type', 'is_read', 'created_at']
    search_fields = ['parcel__parcel_id', 'name', 'email', 'message']
    readonly_fields = ['created_at']


@admin.register(ParcelComparison)
class ParcelComparisonAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_session', 'created_at']
    filter_horizontal = ['parcels']
