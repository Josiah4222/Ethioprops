import os
import django
import json
from datetime import date

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from api.models import Parcel

def seed_parcels():
    # Delete existing parcels to start fresh
    Parcel.objects.all().delete()
    
    parcels = [
        # 1. Bole - Near Edna Mall (Commercial Complex)
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
        
        # 2. Bole - Residential Villa
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
        
        # 3. Meskel Square - Office Building
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
        
        # 4. Stadium Area - Apartment Complex
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
        
        # 5. Piazza - Heritage Building
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
        
        # 6. Bole Arabsa - Modern Villa
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
        
        # 7. Arat Kilo - Mixed Use Building
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
        
        # 8. Lideta - Industrial Warehouse
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
        
        # 9. CMC Area - Condominium
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
        
        # 10. Kolfe - Agricultural Land
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
        },
        
        # 11. Bole Michael - Shopping Center
        {
            "parcel_id": "AA-BOL-W04-P789",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/BOL/2024/3456",
            "area_sqm": 4200.00,
            "dimensions": "60m x 70m",
            "centroid_lat": 8.9920,
            "centroid_lng": 38.7920,
            "entry_lat": 8.9918,
            "entry_lng": 38.7918,
            "sub_city": "Bole",
            "wereda": "04",
            "street_name": "Bole Michael Road",
            "house_number": "3567",
            "landmark": "Near Bole Michael Church",
            "zoning_info": "Commercial - Retail",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Michael Shopping Complex",
            "usage_restrictions": "Retail and entertainment, Maximum 8 floors",
            "survey_date": date(2024, 5, 12),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.79180, 8.99180],
                    [38.79240, 8.99180],
                    [38.79240, 8.99240],
                    [38.79180, 8.99240],
                    [38.79180, 8.99180]
                ]]
            }
        },
        
        # 12. Kazanchis - Hotel Property
        {
            "parcel_id": "AA-BOL-W02-P345",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/BOL/2023/5678",
            "area_sqm": 3500.00,
            "dimensions": "50m x 70m",
            "centroid_lat": 9.0180,
            "centroid_lng": 38.7680,
            "entry_lat": 9.0178,
            "entry_lng": 38.7678,
            "sub_city": "Bole",
            "wereda": "02",
            "street_name": "Kazanchis Road",
            "house_number": "1234",
            "landmark": "Near ECA Conference Center",
            "zoning_info": "Commercial - Hospitality",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Kazanchis Hotels PLC",
            "usage_restrictions": "Hotel and conference facilities, Maximum 15 floors",
            "survey_date": date(2023, 9, 25),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.76780, 9.01780],
                    [38.76830, 9.01780],
                    [38.76830, 9.01830],
                    [38.76780, 9.01830],
                    [38.76780, 9.01780]
                ]]
            }
        },
        
        # 13. Gerji - Residential Compound
        {
            "parcel_id": "AA-YEK-W09-P678",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/YEK/2024/8901",
            "area_sqm": 1200.00,
            "dimensions": "40m x 30m",
            "centroid_lat": 9.0520,
            "centroid_lng": 38.8050,
            "entry_lat": 9.0518,
            "entry_lng": 38.8048,
            "sub_city": "Yeka",
            "wereda": "09",
            "street_name": "Gerji Road",
            "house_number": "G-456",
            "landmark": "Near Gerji Mebrat Hail",
            "zoning_info": "Low-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Hanna Tadesse",
            "usage_restrictions": "Single family, Maximum G+2",
            "survey_date": date(2024, 4, 18),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.80480, 9.05180],
                    [38.80520, 9.05180],
                    [38.80520, 9.05220],
                    [38.80480, 9.05220],
                    [38.80480, 9.05180]
                ]]
            }
        },
        
        # 14. Megenagna - Commercial Plaza
        {
            "parcel_id": "AA-NSL-W09-P890",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/NSL/2024/2345",
            "area_sqm": 2800.00,
            "dimensions": "40m x 70m",
            "centroid_lat": 8.9850,
            "centroid_lng": 38.7650,
            "entry_lat": 8.9848,
            "entry_lng": 38.7648,
            "sub_city": "Nifas Silk-Lafto",
            "wereda": "09",
            "street_name": "Megenagna Road",
            "house_number": "M-234",
            "landmark": "Megenagna Roundabout",
            "zoning_info": "Mixed Commercial",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Megenagna Plaza Ltd",
            "usage_restrictions": "Commercial and office, Maximum 10 floors",
            "survey_date": date(2024, 6, 30),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.76480, 8.98480],
                    [38.76520, 8.98480],
                    [38.76520, 8.98520],
                    [38.76480, 8.98520],
                    [38.76480, 8.98480]
                ]]
            }
        },
        
        # 15. Sarbet - Residential House
        {
            "parcel_id": "AA-GUL-W07-P123",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/GUL/2022/4567",
            "area_sqm": 380.00,
            "dimensions": "19m x 20m",
            "centroid_lat": 9.0250,
            "centroid_lng": 38.7350,
            "entry_lat": 9.0248,
            "entry_lng": 38.7348,
            "sub_city": "Gulele",
            "wereda": "07",
            "street_name": "Sarbet Road",
            "house_number": "S-789",
            "landmark": "Near Sarbet Hospital",
            "zoning_info": "Medium-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Selam Worku",
            "usage_restrictions": "Residential, Maximum G+3",
            "survey_date": date(2022, 8, 14),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.73480, 9.02480],
                    [38.73510, 9.02480],
                    [38.73510, 9.02510],
                    [38.73480, 9.02510],
                    [38.73480, 9.02480]
                ]]
            }
        },
        
        # 16. Merkato - Commercial Building
        {
            "parcel_id": "AA-AKE-W08-P456",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/AKE/2021/6789",
            "area_sqm": 950.00,
            "dimensions": "25m x 38m",
            "centroid_lat": 9.0150,
            "centroid_lng": 38.7250,
            "entry_lat": 9.0148,
            "entry_lng": 38.7248,
            "sub_city": "Addis Ketema",
            "wereda": "08",
            "street_name": "Merkato Main Road",
            "house_number": "MK-567",
            "landmark": "Near Merkato Bus Station",
            "zoning_info": "High-density Commercial",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": False,
            "owner_name": "Merkato Trading House",
            "usage_restrictions": "Commercial only, Maximum G+5",
            "survey_date": date(2021, 11, 8),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.72480, 9.01480],
                    [38.72520, 9.01480],
                    [38.72520, 9.01520],
                    [38.72480, 9.01520],
                    [38.72480, 9.01480]
                ]]
            }
        },
        
        # 17. Lebu - Residential Villa
        {
            "parcel_id": "AA-GUL-W10-P789",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/GUL/2024/9012",
            "area_sqm": 720.00,
            "dimensions": "30m x 24m",
            "centroid_lat": 9.0580,
            "centroid_lng": 38.7150,
            "entry_lat": 9.0578,
            "entry_lng": 38.7148,
            "sub_city": "Gulele",
            "wereda": "10",
            "street_name": "Lebu Road",
            "house_number": "L-345",
            "landmark": "Near Lebu Market",
            "zoning_info": "Low-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Biruk Assefa",
            "usage_restrictions": "Single family, Maximum G+2",
            "survey_date": date(2024, 3, 22),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.71480, 9.05780],
                    [38.71520, 9.05780],
                    [38.71520, 9.05820],
                    [38.71480, 9.05820],
                    [38.71480, 9.05780]
                ]]
            }
        },
        
        # 18. Jemo - Condominium Site
        {
            "parcel_id": "AA-NSL-W11-P234",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/NSL/2023/3456",
            "area_sqm": 550.00,
            "dimensions": "22m x 25m",
            "centroid_lat": 8.9650,
            "centroid_lng": 38.7450,
            "entry_lat": 8.9648,
            "entry_lng": 38.7448,
            "sub_city": "Nifas Silk-Lafto",
            "wereda": "11",
            "street_name": "Jemo Road",
            "house_number": "J-678",
            "landmark": "Near Jemo Condominium",
            "zoning_info": "High-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Meseret Kebede",
            "usage_restrictions": "Residential, Maximum G+4",
            "survey_date": date(2023, 12, 5),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.74480, 8.96480],
                    [38.74510, 8.96480],
                    [38.74510, 8.96510],
                    [38.74480, 8.96510],
                    [38.74480, 8.96480]
                ]]
            }
        },
        
        # 19. Kality - Industrial Complex
        {
            "parcel_id": "AA-AKA-W05-P567",
            "property_type": "INDUSTRIAL",
            "title_deed_ref": "TD/AKA/2020/7890",
            "area_sqm": 18000.00,
            "dimensions": "150m x 120m",
            "centroid_lat": 8.9200,
            "centroid_lng": 38.7300,
            "entry_lat": 8.9195,
            "entry_lng": 38.7295,
            "sub_city": "Akaki Kality",
            "wereda": "05",
            "street_name": "Kality Industrial Road",
            "house_number": "IND-78",
            "landmark": "Near Kality Prison",
            "zoning_info": "Heavy Industrial Zone",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Kality Industries PLC",
            "usage_restrictions": "Industrial manufacturing, Environmental permit required",
            "survey_date": date(2020, 5, 18),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.72950, 8.91950],
                    [38.73050, 8.91950],
                    [38.73050, 8.92050],
                    [38.72950, 8.92050],
                    [38.72950, 8.91950]
                ]]
            }
        },
        
        # 20. Saris - Residential Apartment
        {
            "parcel_id": "AA-ARA-W06-P890",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/ARA/2024/1234",
            "area_sqm": 420.00,
            "dimensions": "21m x 20m",
            "centroid_lat": 9.0380,
            "centroid_lng": 38.7420,
            "entry_lat": 9.0378,
            "entry_lng": 38.7418,
            "sub_city": "Arada",
            "wereda": "06",
            "street_name": "Saris Road",
            "house_number": "SR-234",
            "landmark": "Near Saris Hotel",
            "zoning_info": "Medium-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Kidist Mulugeta",
            "usage_restrictions": "Residential, Maximum G+3",
            "survey_date": date(2024, 1, 15),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.74180, 9.03780],
                    [38.74210, 9.03780],
                    [38.74210, 9.03810],
                    [38.74180, 9.03810],
                    [38.74180, 9.03780]
                ]]
            }
        },
        
        # 21. Shiro Meda - Commercial Textile Center
        {
            "parcel_id": "AA-GUL-W05-P345",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/GUL/2023/5678",
            "area_sqm": 1800.00,
            "dimensions": "45m x 40m",
            "centroid_lat": 9.0420,
            "centroid_lng": 38.7280,
            "entry_lat": 9.0418,
            "entry_lng": 38.7278,
            "sub_city": "Gulele",
            "wereda": "05",
            "street_name": "Shiro Meda Road",
            "house_number": "SM-123",
            "landmark": "Shiro Meda Market",
            "zoning_info": "Commercial - Retail",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Shiro Meda Traders Association",
            "usage_restrictions": "Retail and wholesale, Maximum G+4",
            "survey_date": date(2023, 4, 10),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.72780, 9.04180],
                    [38.72820, 9.04180],
                    [38.72820, 9.04220],
                    [38.72780, 9.04220],
                    [38.72780, 9.04180]
                ]]
            }
        },
        
        # 22. Gofa - Residential House
        {
            "parcel_id": "AA-NSL-W08-P678",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/NSL/2022/8901",
            "area_sqm": 340.00,
            "dimensions": "17m x 20m",
            "centroid_lat": 8.9720,
            "centroid_lng": 38.7520,
            "entry_lat": 8.9718,
            "entry_lng": 38.7518,
            "sub_city": "Nifas Silk-Lafto",
            "wereda": "08",
            "street_name": "Gofa Road",
            "house_number": "GF-456",
            "landmark": "Near Gofa Mazoria",
            "zoning_info": "Medium-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Abebe Desta",
            "usage_restrictions": "Residential, Maximum G+3",
            "survey_date": date(2022, 10, 20),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.75180, 8.97180],
                    [38.75210, 8.97180],
                    [38.75210, 8.97210],
                    [38.75180, 8.97210],
                    [38.75180, 8.97180]
                ]]
            }
        },
        
        # 23. Lafto - Shopping Mall
        {
            "parcel_id": "AA-NSL-W07-P901",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/NSL/2024/4567",
            "area_sqm": 6500.00,
            "dimensions": "65m x 100m",
            "centroid_lat": 8.9680,
            "centroid_lng": 38.7580,
            "entry_lat": 8.9678,
            "entry_lng": 38.7578,
            "sub_city": "Nifas Silk-Lafto",
            "wereda": "07",
            "street_name": "Lafto Road",
            "house_number": "LF-789",
            "landmark": "Lafto Mall",
            "zoning_info": "Commercial - Large Scale Retail",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Lafto Development PLC",
            "usage_restrictions": "Shopping mall and entertainment, Maximum 10 floors",
            "survey_date": date(2024, 7, 5),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.75780, 8.96780],
                    [38.75850, 8.96780],
                    [38.75850, 8.96850],
                    [38.75780, 8.96850],
                    [38.75780, 8.96780]
                ]]
            }
        },
        
        # 24. Kotebe - University Campus
        {
            "parcel_id": "AA-YEK-W11-P234",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/YEK/2019/2345",
            "area_sqm": 35000.00,
            "dimensions": "250m x 140m",
            "centroid_lat": 8.9950,
            "centroid_lng": 38.8200,
            "entry_lat": 8.9945,
            "entry_lng": 38.8195,
            "sub_city": "Yeka",
            "wereda": "11",
            "street_name": "Kotebe Road",
            "house_number": "EDU-01",
            "landmark": "Kotebe University",
            "zoning_info": "Educational Institution",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Kotebe University of Education",
            "usage_restrictions": "Educational use only",
            "survey_date": date(2019, 3, 15),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.81950, 8.99450],
                    [38.82100, 8.99450],
                    [38.82100, 8.99600],
                    [38.81950, 8.99600],
                    [38.81950, 8.99450]
                ]]
            }
        },
        
        # 25. Tulu Dimtu - Residential Villa
        {
            "parcel_id": "AA-YEK-W07-P567",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/YEK/2024/6789",
            "area_sqm": 950.00,
            "dimensions": "38m x 25m",
            "centroid_lat": 9.0380,
            "centroid_lng": 38.8150,
            "entry_lat": 9.0378,
            "entry_lng": 38.8148,
            "sub_city": "Yeka",
            "wereda": "07",
            "street_name": "Tulu Dimtu Road",
            "house_number": "TD-890",
            "landmark": "Near Tulu Dimtu Church",
            "zoning_info": "Low-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Rahel Tesfaye",
            "usage_restrictions": "Single family, Maximum G+2",
            "survey_date": date(2024, 9, 12),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.81480, 9.03780],
                    [38.81520, 9.03780],
                    [38.81520, 9.03820],
                    [38.81480, 9.03820],
                    [38.81480, 9.03780]
                ]]
            }
        },
        
        # 26. Bole Atlas - Office Complex
        {
            "parcel_id": "AA-BOL-W05-P123",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/BOL/2023/7890",
            "area_sqm": 2900.00,
            "dimensions": "58m x 50m",
            "centroid_lat": 8.9880,
            "centroid_lng": 38.7980,
            "entry_lat": 8.9878,
            "entry_lng": 38.7978,
            "sub_city": "Bole",
            "wereda": "05",
            "street_name": "Bole Atlas Road",
            "house_number": "BA-345",
            "landmark": "Near Atlas Hotel",
            "zoning_info": "Commercial - Office",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Atlas Business Center",
            "usage_restrictions": "Office and commercial, Maximum 12 floors",
            "survey_date": date(2023, 6, 18),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.79780, 8.98780],
                    [38.79830, 8.98780],
                    [38.79830, 8.98830],
                    [38.79780, 8.98830],
                    [38.79780, 8.98780]
                ]]
            }
        },
        
        # 27. Hayahulet - Residential Compound
        {
            "parcel_id": "AA-KIR-W05-P456",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/KIR/2022/3456",
            "area_sqm": 580.00,
            "dimensions": "29m x 20m",
            "centroid_lat": 9.0080,
            "centroid_lng": 38.7580,
            "entry_lat": 9.0078,
            "entry_lng": 38.7578,
            "sub_city": "Kirkos",
            "wereda": "05",
            "street_name": "Hayahulet Road",
            "house_number": "HY-678",
            "landmark": "Near Hayahulet Elementary School",
            "zoning_info": "Medium-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Yonas Girma",
            "usage_restrictions": "Residential, Maximum G+3",
            "survey_date": date(2022, 11, 25),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.75780, 9.00780],
                    [38.75810, 9.00780],
                    [38.75810, 9.00810],
                    [38.75780, 9.00810],
                    [38.75780, 9.00780]
                ]]
            }
        },
        
        # 28. Aware - Industrial Park
        {
            "parcel_id": "AA-NSL-W12-P789",
            "property_type": "INDUSTRIAL",
            "title_deed_ref": "TD/NSL/2021/5678",
            "area_sqm": 22000.00,
            "dimensions": "200m x 110m",
            "centroid_lat": 8.9550,
            "centroid_lng": 38.7700,
            "entry_lat": 8.9545,
            "entry_lng": 38.7695,
            "sub_city": "Nifas Silk-Lafto",
            "wereda": "12",
            "street_name": "Aware Industrial Road",
            "house_number": "IND-23",
            "landmark": "Near Aware Industrial Park",
            "zoning_info": "Light Industrial",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Aware Manufacturing Ltd",
            "usage_restrictions": "Light manufacturing, Environmental compliance required",
            "survey_date": date(2021, 7, 8),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.76950, 8.95450],
                    [38.77050, 8.95450],
                    [38.77050, 8.95550],
                    [38.76950, 8.95550],
                    [38.76950, 8.95450]
                ]]
            }
        },
        
        # 29. Entoto - Agricultural Land
        {
            "parcel_id": "AA-GUL-W11-P012",
            "property_type": "AGRICULTURAL",
            "title_deed_ref": "TD/GUL/2018/9012",
            "area_sqm": 45000.00,
            "dimensions": "300m x 150m",
            "centroid_lat": 9.0850,
            "centroid_lng": 38.7450,
            "entry_lat": 9.0845,
            "entry_lng": 38.7445,
            "sub_city": "Gulele",
            "wereda": "11",
            "street_name": "Entoto Road",
            "house_number": "AGR-05",
            "landmark": "Near Entoto Mountain",
            "zoning_info": "Agricultural - Protected Forest Area",
            "road_access": "UNPAVED",
            "has_electricity": False,
            "has_water": False,
            "has_sewage": False,
            "owner_name": "Entoto Forest Cooperative",
            "usage_restrictions": "Agricultural and forestry only, Protected area",
            "survey_date": date(2018, 5, 22),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.74450, 9.08450],
                    [38.74600, 9.08450],
                    [38.74600, 9.08600],
                    [38.74450, 9.08600],
                    [38.74450, 9.08450]
                ]]
            }
        },
        
        # 30. Bole Bulbula - Residential Apartment
        {
            "parcel_id": "AA-BOL-W06-P890",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/BOL/2024/8901",
            "area_sqm": 480.00,
            "dimensions": "24m x 20m",
            "centroid_lat": 8.9820,
            "centroid_lng": 38.7750,
            "entry_lat": 8.9818,
            "entry_lng": 38.7748,
            "sub_city": "Bole",
            "wereda": "06",
            "street_name": "Bole Bulbula Road",
            "house_number": "BB-234",
            "landmark": "Near Bole Bulbula Church",
            "zoning_info": "Medium-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Bethlehem Negash",
            "usage_restrictions": "Residential, Maximum G+3",
            "survey_date": date(2024, 10, 5),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.77480, 8.98180],
                    [38.77510, 8.98180],
                    [38.77510, 8.98210],
                    [38.77480, 8.98210],
                    [38.77480, 8.98180]
                ]]
            }
        },
        
        # 31. Mexico - Commercial Center
        {
            "parcel_id": "AA-KIR-W04-P234",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/KIR/2023/6789",
            "area_sqm": 3100.00,
            "dimensions": "62m x 50m",
            "centroid_lat": 9.0220,
            "centroid_lng": 38.7620,
            "entry_lat": 9.0218,
            "entry_lng": 38.7618,
            "sub_city": "Kirkos",
            "wereda": "04",
            "street_name": "Mexico Road",
            "house_number": "MX-567",
            "landmark": "Near Mexico Square",
            "zoning_info": "Commercial - Mixed Use",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Mexico Plaza PLC",
            "usage_restrictions": "Commercial and office, Maximum 10 floors",
            "survey_date": date(2023, 8, 30),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.76180, 9.02180],
                    [38.76230, 9.02180],
                    [38.76230, 9.02230],
                    [38.76180, 9.02230],
                    [38.76180, 9.02180]
                ]]
            }
        },
        
        # 32. Sidist Kilo - University Building
        {
            "parcel_id": "AA-ARA-W07-P345",
            "property_type": "COMMERCIAL",
            "title_deed_ref": "TD/ARA/2020/4567",
            "area_sqm": 8500.00,
            "dimensions": "85m x 100m",
            "centroid_lat": 9.0320,
            "centroid_lng": 38.7520,
            "entry_lat": 9.0318,
            "entry_lng": 38.7518,
            "sub_city": "Arada",
            "wereda": "07",
            "street_name": "Sidist Kilo Road",
            "house_number": "EDU-02",
            "landmark": "Addis Ababa University",
            "zoning_info": "Educational Institution",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Addis Ababa University",
            "usage_restrictions": "Educational and research use only",
            "survey_date": date(2020, 2, 14),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.75180, 9.03180],
                    [38.75280, 9.03180],
                    [38.75280, 9.03280],
                    [38.75180, 9.03280],
                    [38.75180, 9.03180]
                ]]
            }
        },
        
        # 33. Kera - Residential House
        {
            "parcel_id": "AA-GUL-W08-P678",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/GUL/2023/1234",
            "area_sqm": 520.00,
            "dimensions": "26m x 20m",
            "centroid_lat": 9.0480,
            "centroid_lng": 38.7320,
            "entry_lat": 9.0478,
            "entry_lng": 38.7318,
            "sub_city": "Gulele",
            "wereda": "08",
            "street_name": "Kera Road",
            "house_number": "KR-890",
            "landmark": "Near Kera Church",
            "zoning_info": "Medium-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Tsehay Mengistu",
            "usage_restrictions": "Residential, Maximum G+3",
            "survey_date": date(2023, 10, 8),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.73180, 9.04780],
                    [38.73210, 9.04780],
                    [38.73210, 9.04810],
                    [38.73180, 9.04810],
                    [38.73180, 9.04780]
                ]]
            }
        },
        
        # 34. Kaliti - Warehouse Complex
        {
            "parcel_id": "AA-AKA-W06-P901",
            "property_type": "INDUSTRIAL",
            "title_deed_ref": "TD/AKA/2022/2345",
            "area_sqm": 15000.00,
            "dimensions": "125m x 120m",
            "centroid_lat": 8.9100,
            "centroid_lng": 38.7400,
            "entry_lat": 8.9095,
            "entry_lng": 38.7395,
            "sub_city": "Akaki Kality",
            "wereda": "06",
            "street_name": "Kaliti Road",
            "house_number": "IND-56",
            "landmark": "Near Kaliti Checkpoint",
            "zoning_info": "Industrial - Warehouse",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Kaliti Logistics PLC",
            "usage_restrictions": "Warehouse and distribution only",
            "survey_date": date(2022, 4, 12),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.73950, 8.90950],
                    [38.74050, 8.90950],
                    [38.74050, 8.91050],
                    [38.73950, 8.91050],
                    [38.73950, 8.90950]
                ]]
            }
        },
        
        # 35. Summit - Residential Villa
        {
            "parcel_id": "AA-BOL-W07-P567",
            "property_type": "RESIDENTIAL",
            "title_deed_ref": "TD/BOL/2024/5678",
            "area_sqm": 1100.00,
            "dimensions": "44m x 25m",
            "centroid_lat": 8.9780,
            "centroid_lng": 38.7820,
            "entry_lat": 8.9778,
            "entry_lng": 38.7818,
            "sub_city": "Bole",
            "wereda": "07",
            "street_name": "Summit Road",
            "house_number": "SM-123",
            "landmark": "Near Summit Condominium",
            "zoning_info": "Low-density Residential",
            "road_access": "PAVED",
            "has_electricity": True,
            "has_water": True,
            "has_sewage": True,
            "owner_name": "Samuel Bekele",
            "usage_restrictions": "Single family, Maximum G+2",
            "survey_date": date(2024, 11, 20),
            "geometry": {
                "type": "Polygon",
                "coordinates": [[
                    [38.78180, 8.97780],
                    [38.78230, 8.97780],
                    [38.78230, 8.97830],
                    [38.78180, 8.97830],
                    [38.78180, 8.97780]
                ]]
            }
        },
    ]

    for p_data in parcels:
        geometry_json = json.dumps(p_data.pop("geometry"))
        Parcel.objects.create(
            geometry_json=geometry_json,
            **p_data
        )
    print(f"Successfully seeded {len(parcels)} parcels with realistic Addis Ababa data!")

if __name__ == "__main__":
    seed_parcels()
