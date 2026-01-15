import { Component, AfterViewInit, OnDestroy, Inject, PLATFORM_ID, Output, EventEmitter, Input, SimpleChanges, OnChanges } from '@angular/core';
import { isPlatformBrowser } from '@angular/common';
import * as L from 'leaflet';
import { ParcelService, Parcel } from '../../services/parcel.service';

@Component({
  selector: 'app-map',
  standalone: true,
  imports: [],
  templateUrl: './map.component.html',
  styleUrl: './map.component.css'
})
export class MapComponent implements AfterViewInit, OnDestroy, OnChanges {
  private map: L.Map | undefined;
  private parcelLayer: L.FeatureGroup | undefined;
  private currentTileLayer: L.TileLayer | undefined;
  private satelliteLayer: L.TileLayer | undefined;
  private labelsLayer: L.TileLayer | undefined;

  @Input() mapStyle: 'map' | 'satellite' | 'hybrid' = 'map';
  @Output() parcelSelected = new EventEmitter<Parcel>();

  constructor(
    @Inject(PLATFORM_ID) private platformId: Object,
    private parcelService: ParcelService
  ) { }

  ngAfterViewInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.initMap();
      this.loadParcels();
    }
  }

  ngOnChanges(changes: SimpleChanges): void {
    if (changes['mapStyle'] && !changes['mapStyle'].firstChange && this.map) {
      this.switchMapStyle(this.mapStyle);
    }
  }

  private initMap(): void {
    const lat = 9.0128;
    const lng = 38.7500;

    this.map = L.map('map', {
      center: [lat, lng],
      zoom: 15,
      zoomControl: false
    });

    // Initialize with standard map view
    this.currentTileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
      maxZoom: 19,
      attribution: '© OpenStreetMap contributors'
    }).addTo(this.map);

    L.control.zoom({
      position: 'bottomright'
    }).addTo(this.map);

    this.parcelLayer = L.featureGroup().addTo(this.map);
  }

  private switchMapStyle(style: 'map' | 'satellite' | 'hybrid'): void {
    if (!this.map) return;

    // Remove current layers
    if (this.currentTileLayer) {
      this.map.removeLayer(this.currentTileLayer);
    }
    if (this.satelliteLayer) {
      this.map.removeLayer(this.satelliteLayer);
    }
    if (this.labelsLayer) {
      this.map.removeLayer(this.labelsLayer);
    }

    switch (style) {
      case 'map':
        this.currentTileLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: '© OpenStreetMap contributors'
        }).addTo(this.map);
        break;

      case 'satellite':
        // Using Esri World Imagery for satellite view
        this.satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
          maxZoom: 19,
          attribution: '© Esri, Maxar, Earthstar Geographics'
        }).addTo(this.map);
        break;

      case 'hybrid':
        // Satellite imagery with labels overlay
        this.satelliteLayer = L.tileLayer('https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
          maxZoom: 19,
          attribution: '© Esri, Maxar, Earthstar Geographics'
        }).addTo(this.map);
        
        // Add labels on top
        this.labelsLayer = L.tileLayer('https://{s}.basemaps.cartocdn.com/light_only_labels/{z}/{x}/{y}.png', {
          maxZoom: 19,
          attribution: '© CARTO'
        }).addTo(this.map);
        break;
    }
  }

  private loadParcels(): void {
    this.parcelService.getParcels().subscribe({
      next: (response: any) => {
        const parcels = response.results || response;
        parcels.forEach((parcel: Parcel) => {
          if (parcel.geometry) {
            this.addParcelToMap(parcel);
          }
        });
      },
      error: (err) => console.error('Error loading parcels:', err)
    });
  }

  private addParcelToMap(parcel: Parcel): void {
    if (!this.map || !this.parcelLayer) return;

    const geojsonLayer = L.geoJSON(parcel.geometry, {
      style: {
        color: '#007a33',
        weight: 2,
        fillColor: '#007a33',
        fillOpacity: 0.1,
      },
      onEachFeature: (feature, layer) => {
        // Build popup content with available data
        let popupContent = `<div class="parcel-popup" style="min-width: 200px;">`;
        popupContent += `<strong style="font-size: 14px; color: #007a33;">${parcel.parcel_id}</strong><br>`;
        
        if (parcel.title) {
          popupContent += `<div style="margin: 5px 0; font-size: 12px;">${parcel.title}</div>`;
        }
        
        if (parcel.property_type) {
          popupContent += `<span style="background: #e8f5e9; padding: 2px 8px; border-radius: 3px; font-size: 11px; display: inline-block; margin: 3px 0;">${parcel.property_type}</span><br>`;
        }
        
        if (parcel.sub_city) {
          popupContent += `<div style="margin-top: 5px; font-size: 12px;">📍 ${parcel.sub_city}`;
          if (parcel.landmark) {
            popupContent += ` - ${parcel.landmark}`;
          }
          popupContent += `</div>`;
        }
        
        if (parcel.area_sqm) {
          popupContent += `<div style="font-size: 12px; margin-top: 3px;">📏 ${parcel.area_sqm.toLocaleString()} m²</div>`;
        }
        
        if (parcel.sale_price) {
          popupContent += `<div style="font-size: 12px; margin-top: 3px; color: #1976d2; font-weight: bold;">💰 ${parcel.sale_price.toLocaleString()} ETB</div>`;
        }
        
        popupContent += `<div style="margin-top: 8px; padding-top: 5px; border-top: 1px solid #e0e0e0; font-size: 11px; color: #666;">Click for full details</div>`;
        popupContent += `</div>`;
        
        layer.bindPopup(popupContent);

        layer.on('mouseover', () => {
          (layer as any).setStyle({ fillOpacity: 0.3, weight: 3 });
        });

        layer.on('mouseout', () => {
          (layer as any).setStyle({ fillOpacity: 0.1, weight: 2 });
        });

        layer.on('click', () => {
          this.parcelSelected.emit(parcel);
        });
      }
    }).addTo(this.parcelLayer);
  }

  // Public method to center map on coordinates
  public centerOnLocation(lat: number, lng: number, zoom: number = 18): void {
    if (this.map) {
      this.map.setView([lat, lng], zoom);
      
      // Add a temporary marker at the location
      const marker = L.marker([lat, lng], {
        icon: L.icon({
          iconUrl: 'https://raw.githubusercontent.com/pointhi/leaflet-color-markers/master/img/marker-icon-2x-red.png',
          shadowUrl: 'https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.7.1/images/marker-shadow.png',
          iconSize: [25, 41],
          iconAnchor: [12, 41],
          popupAnchor: [1, -34],
          shadowSize: [41, 41]
        })
      }).addTo(this.map);
      
      marker.bindPopup('<strong>Entrance Location</strong>').openPopup();
      
      // Remove marker after 5 seconds
      setTimeout(() => {
        marker.remove();
      }, 5000);
    }
  }

  ngOnDestroy(): void {
    if (this.map) {
      this.map.remove();
    }
  }
}
