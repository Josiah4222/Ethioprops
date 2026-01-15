from django.db import models
from django.contrib.auth.models import User

class Parcel(models.Model):
    # 1. Location Coordinates
    centroid_lat = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    centroid_lng = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    entry_lat = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    entry_lng = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)

    # 2. Property Identification
    parcel_id = models.CharField(max_length=100, unique=True, help_text="Official parcel ID / cadastral number")
    PROPERTY_TYPES = [
        ('RESIDENTIAL', 'Residential'),
        ('COMMERCIAL', 'Commercial'),
        ('INDUSTRIAL', 'Industrial'),
        ('AGRICULTURAL', 'Agricultural'),
    ]
    property_type = models.CharField(max_length=20, choices=PROPERTY_TYPES, null=True, blank=True)
    title_deed_ref = models.CharField(max_length=100, blank=True, null=True, help_text="Title deed or registration reference")

    # 3. Boundaries & Size
    area_sqm = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    geometry_json = models.TextField(help_text="GeoJSON Polygon coordinates for boundaries")
    adjacent_info = models.TextField(blank=True, null=True, help_text="Adjacent streets, landmarks, or neighbors")
    dimensions = models.CharField(max_length=100, blank=True, null=True, help_text="Plot dimensions (e.g., 20m x 40m)")

    # 4. Address / Administrative Info
    country = models.CharField(max_length=100, default="Ethiopia")
    city = models.CharField(max_length=100, default="Addis Ababa")
    sub_city = models.CharField(max_length=100, blank=True, null=True)
    wereda = models.CharField(max_length=100, blank=True, null=True)
    street_name = models.CharField(max_length=255, blank=True, null=True)
    house_number = models.CharField(max_length=50, blank=True, null=True)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    zoning_info = models.TextField(blank=True, null=True)

    # 5. Access / Infrastructure
    ROAD_ACCESS_TYPES = [
        ('PAVED', 'Paved'),
        ('UNPAVED', 'Unpaved'),
    ]
    road_access = models.CharField(max_length=20, choices=ROAD_ACCESS_TYPES, null=True, blank=True)
    has_electricity = models.BooleanField(default=False)
    has_water = models.BooleanField(default=False)
    has_sewage = models.BooleanField(default=False)

    # 6. Ownership & Legal
    owner_name = models.CharField(max_length=255, blank=True, null=True)
    owner_phone = models.CharField(max_length=20, blank=True, null=True)
    owner_email = models.EmailField(blank=True, null=True)
    usage_restrictions = models.TextField(blank=True, null=True)
    survey_date = models.DateField(null=True, blank=True)
    
    # 7. Pricing Information
    LISTING_TYPES = [
        ('SALE', 'For Sale'),
        ('LEASE', 'For Lease'),
        ('BOTH', 'Sale or Lease'),
    ]
    listing_type = models.CharField(max_length=10, choices=LISTING_TYPES, default='SALE')
    sale_price = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, help_text="Sale price in ETB")
    lease_price_monthly = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, help_text="Monthly lease in ETB")
    lease_price_yearly = models.DecimalField(max_digits=15, decimal_places=2, null=True, blank=True, help_text="Yearly lease in ETB")
    price_per_sqm = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Price per square meter")
    is_negotiable = models.BooleanField(default=True)
    currency = models.CharField(max_length=3, default='ETB')
    
    # 8. Status
    STATUS_CHOICES = [
        ('AVAILABLE', 'Available'),
        ('PENDING', 'Pending'),
        ('SOLD', 'Sold'),
        ('LEASED', 'Leased'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='AVAILABLE')
    is_featured = models.BooleanField(default=False)
    views_count = models.IntegerField(default=0)
    
    # 9. Description
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parcel {self.parcel_id}"
    
    def save(self, *args, **kwargs):
        # Auto-calculate price per sqm
        if self.sale_price and self.area_sqm and self.area_sqm > 0:
            self.price_per_sqm = float(self.sale_price) / float(self.area_sqm)
        super().save(*args, **kwargs)


class ParcelImage(models.Model):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='parcel_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)
    is_primary = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['order', '-is_primary', '-uploaded_at']
    
    def __str__(self):
        return f"Image for {self.parcel.parcel_id}"


class ParcelDocument(models.Model):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='documents')
    DOCUMENT_TYPES = [
        ('TITLE_DEED', 'Title Deed'),
        ('SURVEY', 'Survey Document'),
        ('PERMIT', 'Building Permit'),
        ('OTHER', 'Other'),
    ]
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    file = models.FileField(upload_to='parcel_documents/')
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.document_type} for {self.parcel.parcel_id}"


class NearbyAmenity(models.Model):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='amenities')
    AMENITY_TYPES = [
        ('SCHOOL', 'School'),
        ('HOSPITAL', 'Hospital'),
        ('MARKET', 'Market'),
        ('BANK', 'Bank'),
        ('TRANSPORT', 'Public Transport'),
        ('RESTAURANT', 'Restaurant'),
        ('SHOPPING', 'Shopping Center'),
        ('PARK', 'Park'),
        ('OTHER', 'Other'),
    ]
    amenity_type = models.CharField(max_length=20, choices=AMENITY_TYPES)
    name = models.CharField(max_length=255)
    distance_km = models.DecimalField(max_digits=5, decimal_places=2, help_text="Distance in kilometers")
    latitude = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    longitude = models.DecimalField(max_digits=12, decimal_places=9, null=True, blank=True)
    
    class Meta:
        ordering = ['distance_km']
        verbose_name_plural = 'Nearby Amenities'
    
    def __str__(self):
        return f"{self.name} ({self.distance_km}km from {self.parcel.parcel_id})"


class Inquiry(models.Model):
    parcel = models.ForeignKey(Parcel, on_delete=models.CASCADE, related_name='inquiries')
    name = models.CharField(max_length=255)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    INQUIRY_TYPES = [
        ('VIEWING', 'Request Viewing'),
        ('INFO', 'Request Information'),
        ('OFFER', 'Make Offer'),
        ('OTHER', 'Other'),
    ]
    inquiry_type = models.CharField(max_length=20, choices=INQUIRY_TYPES, default='INFO')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    
    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Inquiries'
    
    def __str__(self):
        return f"Inquiry from {self.name} for {self.parcel.parcel_id}"


class ParcelComparison(models.Model):
    user_session = models.CharField(max_length=255, help_text="Session ID for anonymous users")
    parcels = models.ManyToManyField(Parcel, related_name='comparisons')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Comparison {self.id}"
