from django.db import models

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
    usage_restrictions = models.TextField(blank=True, null=True)
    survey_date = models.DateField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Parcel {self.parcel_id}"
