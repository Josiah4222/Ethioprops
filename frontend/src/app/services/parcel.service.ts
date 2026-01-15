import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface ParcelImage {
  id: number;
  image: string;
  caption?: string;
  is_primary: boolean;
  order: number;
  uploaded_at: string;
}

export interface ParcelDocument {
  id: number;
  document_type: string;
  file: string;
  title: string;
  description?: string;
  uploaded_at: string;
}

export interface NearbyAmenity {
  id: number;
  amenity_type: string;
  name: string;
  distance_km: number;
  latitude?: number;
  longitude?: number;
}

export interface Parcel {
  id: number;
  parcel_id: string;
  title?: string;
  description?: string;
  property_type: string;
  listing_type: string;
  title_deed_ref: string;
  area_sqm: number;
  geometry: any;
  adjacent_info: string;
  dimensions: string;
  country: string;
  city: string;
  sub_city: string;
  wereda: string;
  street_name: string;
  house_number: string;
  landmark: string;
  zoning_info: string;
  road_access: string;
  has_electricity: boolean;
  has_water: boolean;
  has_sewage: boolean;
  owner_name: string;
  owner_phone?: string;
  owner_email?: string;
  usage_restrictions: string;
  survey_date: string;
  centroid_lat: number;
  centroid_lng: number;
  entry_lat: number;
  entry_lng: number;
  sale_price?: number;
  lease_price_monthly?: number;
  lease_price_yearly?: number;
  price_per_sqm?: number;
  is_negotiable: boolean;
  currency: string;
  status: string;
  is_featured: boolean;
  views_count: number;
  primary_image?: string;
  images?: ParcelImage[];
  documents?: ParcelDocument[];
  amenities?: NearbyAmenity[];
  created_at: string;
  updated_at: string;
}

export interface ParcelFilters {
  property_type?: string;
  listing_type?: string;
  sub_city?: string;
  wereda?: string;
  street?: string;
  min_price?: number;
  max_price?: number;
  min_area?: number;
  max_area?: number;
  has_electricity?: boolean;
  has_water?: boolean;
  has_sewage?: boolean;
  status?: string;
  search?: string;
  ordering?: string;
}

export interface Inquiry {
  parcel: number;
  name: string;
  email: string;
  phone: string;
  message: string;
  inquiry_type: string;
}

export interface Statistics {
  overall: {
    avg_price: number;
    min_price: number;
    max_price: number;
    avg_area: number;
    avg_price_per_sqm: number;
    total_parcels: number;
  };
  by_property_type: any;
  by_location: any[];
}

@Injectable({
  providedIn: 'root'
})
export class ParcelService {
  private apiUrl = 'http://localhost:8000/api';

  constructor(private http: HttpClient) { }

  getParcels(filters?: ParcelFilters): Observable<any> {
    let params = new HttpParams();
    
    if (filters) {
      Object.keys(filters).forEach(key => {
        const value = (filters as any)[key];
        if (value !== undefined && value !== null && value !== '') {
          params = params.set(key, value.toString());
        }
      });
    }
    
    return this.http.get<any>(`${this.apiUrl}/parcels/`, { params });
  }

  getParcel(id: number): Observable<Parcel> {
    return this.http.get<Parcel>(`${this.apiUrl}/parcels/${id}/`);
  }

  getFeaturedParcels(): Observable<Parcel[]> {
    return this.http.get<Parcel[]>(`${this.apiUrl}/parcels/featured/`);
  }

  getStatistics(): Observable<Statistics> {
    return this.http.get<Statistics>(`${this.apiUrl}/parcels/statistics/`);
  }

  calculateDistance(parcelId: number, lat: number, lng: number): Observable<any> {
    const params = new HttpParams()
      .set('lat', lat.toString())
      .set('lng', lng.toString());
    return this.http.get(`${this.apiUrl}/parcels/${parcelId}/calculate_distance/`, { params });
  }

  compareParcels(parcelIds: number[]): Observable<any> {
    return this.http.post(`${this.apiUrl}/parcels/compare/`, { parcel_ids: parcelIds });
  }

  submitInquiry(inquiry: Inquiry): Observable<any> {
    return this.http.post(`${this.apiUrl}/inquiries/`, inquiry);
  }

  getParcelImages(parcelId: number): Observable<ParcelImage[]> {
    const params = new HttpParams().set('parcel_id', parcelId.toString());
    return this.http.get<ParcelImage[]>(`${this.apiUrl}/parcel-images/`, { params });
  }

  getParcelDocuments(parcelId: number): Observable<ParcelDocument[]> {
    const params = new HttpParams().set('parcel_id', parcelId.toString());
    return this.http.get<ParcelDocument[]>(`${this.apiUrl}/parcel-documents/`, { params });
  }

  getNearbyAmenities(parcelId: number): Observable<NearbyAmenity[]> {
    const params = new HttpParams().set('parcel_id', parcelId.toString());
    return this.http.get<NearbyAmenity[]>(`${this.apiUrl}/nearby-amenities/`, { params });
  }
}
