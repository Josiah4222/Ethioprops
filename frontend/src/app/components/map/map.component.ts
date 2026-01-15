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
      next: (parcels) => {
        parcels.forEach((parcel) => {
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
        layer.bindPopup(`
          <div class="parcel-popup">
            <strong>Parcel ID:</strong> ${parcel.parcel_id}<br>
            <strong>Zoning:</strong> ${parcel.zoning_info}<br>
            <strong>Owner:</strong> ${parcel.owner_name}
          </div>
        `);

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

  ngOnDestroy(): void {
    if (this.map) {
      this.map.remove();
    }
  }
}
