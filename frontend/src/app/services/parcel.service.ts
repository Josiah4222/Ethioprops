import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Parcel {
  id: number;
  parcel_id: string;
  property_type: string;
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
  usage_restrictions: string;
  survey_date: string;
  centroid_lat: number;
  centroid_lng: number;
  entry_lat: number;
  entry_lng: number;
}

@Injectable({
  providedIn: 'root'
})
export class ParcelService {
  private apiUrl = 'http://localhost:8000/api/parcels/';

  constructor(private http: HttpClient) { }

  getParcels(): Observable<Parcel[]> {
    return this.http.get<Parcel[]>(this.apiUrl);
  }
}
