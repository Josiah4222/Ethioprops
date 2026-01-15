import os
import django
import json
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Parcel

def seed_parcels():
    # Delete existing parcels to start fresh with new schema
    Parcel.objects.all().delete()
    
    parcels = [
        # Bole - Near Edna Mall (Commercial Complex)
        {
            "parcel_id": "AA-BOL-W03-P001",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/BOL/2024/1523",
            "area_sqm": 5800.50,
            "dimensions": "80m x 72.5m",
            "centroid_lat": 8.9950,
            "centroid_lng": 38.7850,
            "entry_lat": 8.9945,
            "entry_lng": 38.7845,
            "sub_city": "Bole",
            "wereda": "03",
            "street_name": "Bole Road",
            "house_number": "2458",
            "landmark": "Near Edna Mall",
            "zoning_info": "High-density Commercial - Mixed Use",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Bole Commercial Center PLC",
            "usage_restrictions": "Maximum 12 floors, Ground floor retail mandatory",
            "survey_date": date(2024, 8, 15),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.78450, 8.99450],
                    [38.78500, 8.99450],
                    [38.78500, 8.99500],
                    [38.78450, 8.99500],
                    [38.78450, 8.99450]
                ]]
            }
        },
        
        # Bole - Residential Villa
        {
            "parcel_id": "AA-BOL-W03-P002",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/BOL/2023/2891",
            "area_sqm": 650.00,
            "dimensions": "25m x 26m",
            "centroid_lat": 8.9960,
            "centroid_lng": 38.7865,
            "entry_lat": 8.9958,
            "entry_lng": 38.7863,
            "sub_city": "Bole",
            "wereda": "03",
            "street_name": "Cameroon Street",
            "house_number": "H-145",
            "landmark": "Behind Bole Medhanialem Church",
            "zoning_info": "Medium-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Alemayehu Tesfaye",
            "usage_restrictions": "Residential only, Maximum G+3",
            "survey_date": date(2023, 11, 20),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.78630, 8.99580],
                    [38.78660, 8.99580],
                    [38.78660, 8.99610],
                    [38.78630, 8.99610],
                    [38.78630, 8.99580]
                ]]
            }
        },
        
        # Meskel Square Area - Office Building
        {
            "parcel_id": "AA-KIR-W01-P015",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/KIR/2025/0456",
            "area_sqm": 3200.75,
            "dimensions": "50m x 64m",
            "centroid_lat": 9.0128,
            "centroid_lng": 38.7500,
            "entry_lat": 9.0125,
            "entry_lng": 38.7498,
            "sub_city": "Kirkos",
            "wereda": "01",
            "street_name": "Ras Mekonnen Avenue",
            "house_number": "1024",
            "landmark": "Near Meskel Square",
            "zoning_info": "Central Business District - High Rise",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Meskel Plaza Development",
            "usage_restrictions": "Commercial/Office use, Maximum 20 floors",
            "survey_date": date(2025, 3, 10),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.74980, 9.01250],
                    [38.75030, 9.01250],
                    [38.75030, 9.01300],
                    [38.74980, 9.01300],
                    [38.74980, 9.01250]
                ]]
            }
        },
        
        # Stadium Area - Apartment Complex
        {
            "parcel_id": "AA-KIR-W02-P089",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/KIR/2022/1678",
            "area_sqm": 450.00,
            "dimensions": "18m x 25m",
            "centroid_lat": 9.0145,
            "centroid_lng": 38.7520,
            "entry_lat": 9.0143,
            "entry_lng": 38.7518,
            "sub_city": "Kirkos",
            "wereda": "02",
            "street_name": "Haile Gebreselassie Road",
            "house_number": "567",
            "landmark": "Near Stadium",
            "zoning_info": "High-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Tigist Bekele",
            "usage_restrictions": "Residential, Maximum G+4",
            "survey_date": date(2022, 6, 5),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.75180, 9.01430],
                    [38.75210, 9.01430],
                    [38.75210, 9.01460],
                    [38.75180, 9.01460],
                    [38.75180, 9.01430]
                ]]
            }
        },
        
        # Piazza - Heritage Building
        {
            "parcel_id": "AA-AKE-W05-P234",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/AKE/2020/3421",
            "area_sqm": 280.00,
            "dimensions": "14m x 20m",
            "centroid_lat": 9.0350,
            "centroid_lng": 38.7380,
            "entry_lat": 9.0348,
            "entry_lng": 38.7378,
            "sub_city": "Addis Ketema",
            "wereda": "05",
            "street_name": "Piazza",
            "house_number": "89",
            "landmark": "Near Taitu Hotel",
            "zoning_info": "Heritage Conservation Zone - Low Rise",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": False,
            "owner_name": "Yohannes Gebre",
            "usage_restrictions": "Heritage area - Maximum G+2, Facade preservation required",
            "survey_date": date(2020, 9, 12),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.73780, 9.03480],
                    [38.73810, 9.03480],
                    [38.73810, 9.03510],
                    [38.73780, 9.03510],
                    [38.73780, 9.03480]
                ]]
            }
        },
        
        # Bole Arabsa - Modern Villa
        {
            "parcel_id": "AA-YEK-W08-P456",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/YEK/2024/5623",
            "area_sqm": 800.00,
            "dimensions": "32m x 25m",
            "centroid_lat": 9.0450,
            "centroid_lng": 38.8100,
            "entry_lat": 9.0448,
            "entry_lng": 38.8098,
            "sub_city": "Yeka",
            "wereda": "08",
            "street_name": "Bole Arabsa Road",
            "house_number": "K-234",
            "landmark": "Near Ayat Real Estate",
            "zoning_info": "Low-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Mekdes Alemu",
            "usage_restrictions": "Single family residence, Maximum G+2",
            "survey_date": date(2024, 2, 18),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.80980, 9.04480],
                    [38.81020, 9.04480],
                    [38.81020, 9.04520],
                    [38.80980, 9.04520],
                    [38.80980, 9.04480]
                ]]
            }
        },
        
        # Arat Kilo - Mixed Use Building
        {
            "parcel_id": "AA-ARA-W04-P178",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/ARA/2023/2134",
            "area_sqm": 1500.00,
            "dimensions": "30m x 50m",
            "centroid_lat": 9.0300,
            "centroid_lng": 38.7450,
            "entry_lat": 9.0298,
            "entry_lng": 38.7448,
            "sub_city": "Arada",
            "wereda": "04",
            "street_name": "Churchill Avenue",
            "house_number": "456",
            "landmark": "Near Arat Kilo",
            "zoning_info": "Mixed Commercial/Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Arada Business Center",
            "usage_restrictions": "Ground floor commercial, Upper floors residential/office",
            "survey_date": date(2023, 7, 22),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.74480, 9.02980],
                    [38.74530, 9.02980],
                    [38.74530, 9.03020],
                    [38.74480, 9.03020],
                    [38.74480, 9.02980]
                ]]
            }
        },
        
        # Lideta - Industrial Warehouse
        {
            "parcel_id": "AA-LID-W06-P089",
            "property_type": "INDUSTRIAL",
            "title_deed_ref": "TD/LID/2021/4567",
            "area_sqm": 12000.00,
            "dimensions": "100m x 120m",
            "centroid_lat": 9.0050,
            "centroid_lng": 38.7200,
            "entry_lat": 9.0045,
            "entry_lng": 38.7195,
            "sub_city": "Lideta",
            "wereda": "06",
            "street_name": "Industrial Road",
            "house_number": "IND-45",
            "landmark": "Near Akaki River",
            "zoning_info": "Light Industrial Zone",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Ethiopian Manufacturing PLC",
            "usage_restrictions": "Light manufacturing only, Environmental compliance required",
            "survey_date": date(2021, 4, 30),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.71950, 9.00450],
                    [38.72050, 9.00450],
                    [38.72050, 9.00550],
                    [38.71950, 9.00550],
                    [38.71950, 9.00450]
                ]]
            }
        },
        
        # CMC Area - Condominium
        {
            "parcel_id": "AA-NSL-W10-P567",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/NSL/2025/7890",
            "area_sqm": 500.00,
            "dimensions": "20m x 25m",
            "centroid_lat": 8.9800,
            "centroid_lng": 38.7600,
            "entry_lat": 8.9798,
            "entry_lng": 38.7598,
            "sub_city": "Nifas Silk-Lafto",
            "wereda": "10",
            "street_name": "CMC Road",
            "house_number": "N-789",
            "landmark": "Near Megenagna",
            "zoning_info": "Medium-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Dawit Hailu",
            "usage_restrictions": "Residential, Maximum G+3",
            "survey_date": date(2025, 1, 8),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.75980, 8.97980],
                    [38.76010, 8.97980],
                    [38.76010, 8.98010],
                    [38.75980, 8.98010],
                    [38.75980, 8.97980]
                ]]
            }
        },
        
        # Kolfe - Agricultural Land
        {
            "parcel_id": "AA-KOL-W12-P234",
            "property_type": "AGRICULTURAL",
            "title_deed_ref": "TD/KOL/2019/8901",
            "area_sqm": 25000.00,
            "dimensions": "200m x 125m",
            "centroid_lat": 8.9500,
            "centroid_lng": 38.6800,
            "entry_lat": 8.9495,
            "entry_lng": 38.6795,
            "sub_city": "Kolfe Keranio",
            "wereda": "12",
            "street_name": "Kolfe Road",
            "house_number": "AGR-12",
            "landmark": "Near Kolfe Church",
            "zoning_info": "Agricultural - Future Urban Development",
            "road_access": "UNPAVED",
            "has_electricity": False,
            "has_water": False,
            "has_sewage": False,
            "owner_name": "Farmers Cooperative Union",
            "usage_restrictions": "Agricultural use, Future rezoning planned",
            "survey_date": date(2019, 10, 15),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.67950, 8.94950],
                    [38.68050, 8.94950],
                    [38.68050, 8.95050],
                    [38.67950, 8.95050],
                    [38.67950, 8.94950]
                ]]
            }
        }
    ]

    for p_data in parcels:
        geometry_json = json.dumps(p_data.pop("geometry"))
        Parcel.objects.create(
            geometry_json=geometry_json,
            **p_data
        )
    print("Re-seeded with detailed property info successfully!")

if __name__ == "__main__":
    seed_parcels()
