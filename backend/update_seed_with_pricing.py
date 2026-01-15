import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Parcel, NearbyAmenity

def update_parcels_with_pricing():
    """Update existing parcels with pricing and other new fields"""
    
    parcels = Parcel.objects.all()
    
    for parcel in parcels:
        # Add pricing based on property type and location
        if parcel.property_type == 'RESIDENTIAL':
            base_price_per_sqm = random.randint(80000, 150000)  # ETB per sqm
            parcel.listing_type = random.choice(['SALE', 'LEASE', 'BOTH'])
        elif parcel.property_type == 'COMMERCIAL':
            base_price_per_sqm = random.randint(120000, 250000)
            parcel.listing_type = random.choice(['SALE', 'LEASE', 'BOTH'])
        elif parcel.property_type == 'INDUSTRIAL':
            base_price_per_sqm = random.randint(50000, 100000)
            parcel.listing_type = 'SALE'
        else:  # AGRICULTURAL
            base_price_per_sqm = random.randint(5000, 15000)
            parcel.listing_type = 'SALE'
        
        # Premium locations get higher prices
        if parcel.sub_city in ['Bole', 'Kirkos', 'Yeka']:
            base_price_per_sqm = int(base_price_per_sqm * 1.3)
        
        # Calculate sale price
        if parcel.area_sqm:
            parcel.sale_price = float(parcel.area_sqm) * base_price_per_sqm
            parcel.price_per_sqm = base_price_per_sqm
            
            # Calculate lease prices (if applicable)
            if parcel.listing_type in ['LEASE', 'BOTH']:
                # Monthly lease is roughly 0.5-1% of sale price
                parcel.lease_price_monthly = parcel.sale_price * random.uniform(0.005, 0.01)
                parcel.lease_price_yearly = parcel.lease_price_monthly * 12
        
        # Add title and description
        parcel.title = f"{parcel.property_type.title()} Property in {parcel.sub_city}"
        parcel.description = f"Prime {parcel.property_type.lower()} property located in {parcel.sub_city}, {parcel.landmark}. " \
                           f"Total area: {parcel.area_sqm} sqm. " \
                           f"{'Electricity, water, and sewage available.' if parcel.has_electricity and parcel.has_water and parcel.has_sewage else 'Basic utilities available.'}"
        
        # Add owner contact
        parcel.owner_phone = f"+251-9{random.randint(10000000, 99999999)}"
        parcel.owner_email = f"{parcel.owner_name.lower().replace(' ', '.')}@email.com" if parcel.owner_name else None
        
        # Set status and features
        parcel.status = 'AVAILABLE'
        parcel.is_negotiable = random.choice([True, True, True, False])  # 75% negotiable
        parcel.is_featured = random.choice([True, False, False, False])  # 25% featured
        parcel.views_count = random.randint(0, 500)
        
        parcel.save()
        print(f"Updated {parcel.parcel_id} - {parcel.title}")


def add_nearby_amenities():
    """Add nearby amenities to parcels"""
    
    # Common amenities in Addis Ababa
    amenities_data = {
        'Bole': [
            ('SCHOOL', 'International Community School', 1.2),
            ('HOSPITAL', 'Bole Medical Center', 0.8),
            ('MARKET', 'Edna Mall', 0.5),
            ('BANK', 'Commercial Bank of Ethiopia', 0.3),
            ('TRANSPORT', 'Bole Bus Station', 1.5),
            ('SHOPPING', 'Edna Mall', 0.5),
        ],
        'Kirkos': [
            ('SCHOOL', 'Kirkos Elementary School', 0.9),
            ('HOSPITAL', 'Black Lion Hospital', 2.5),
            ('MARKET', 'Meskel Square Market', 0.7),
            ('BANK', 'Dashen Bank', 0.4),
            ('TRANSPORT', 'Meskel Square Station', 0.6),
        ],
        'Yeka': [
            ('SCHOOL', 'Yeka Secondary School', 1.1),
            ('HOSPITAL', 'Yeka Health Center', 1.8),
            ('MARKET', 'Gerji Market', 1.3),
            ('BANK', 'Awash Bank', 0.9),
            ('TRANSPORT', 'Gerji Bus Stop', 0.7),
        ],
        'Arada': [
            ('SCHOOL', 'Arada Elementary School', 0.8),
            ('HOSPITAL', 'St. Paul Hospital', 1.5),
            ('MARKET', 'Piazza Market', 0.6),
            ('BANK', 'Bank of Abyssinia', 0.3),
            ('TRANSPORT', 'Piazza Bus Station', 0.5),
        ],
        'Gulele': [
            ('SCHOOL', 'Gulele Secondary School', 1.0),
            ('HOSPITAL', 'Gulele Health Center', 1.2),
            ('MARKET', 'Shiro Meda Market', 0.9),
            ('BANK', 'Nib Bank', 0.7),
            ('TRANSPORT', 'Shiro Meda Station', 0.8),
        ],
        'Nifas Silk-Lafto': [
            ('SCHOOL', 'CMC Elementary School', 1.3),
            ('HOSPITAL', 'Lafto Health Center', 1.6),
            ('MARKET', 'Megenagna Market', 0.8),
            ('BANK', 'Wegagen Bank', 0.6),
            ('TRANSPORT', 'Megenagna Roundabout', 0.4),
        ],
    }
    
    parcels = Parcel.objects.all()
    
    for parcel in parcels:
        # Clear existing amenities
        parcel.amenities.all().delete()
        
        # Get amenities for this sub-city
        sub_city_amenities = amenities_data.get(parcel.sub_city, [])
        
        # Add some random variation to distances
        for amenity_type, name, base_distance in sub_city_amenities:
            distance = base_distance + random.uniform(-0.2, 0.3)
            distance = max(0.1, distance)  # Minimum 0.1 km
            
            NearbyAmenity.objects.create(
                parcel=parcel,
                amenity_type=amenity_type,
                name=name,
                distance_km=round(distance, 2)
            )
        
        print(f"Added amenities for {parcel.parcel_id}")


if __name__ == "__main__":
    print("Updating parcels with pricing information...")
    update_parcels_with_pricing()
    print("\nAdding nearby amenities...")
    add_nearby_amenities()
    print("\nUpdate complete!")
