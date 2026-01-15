import { Component } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MapComponent } from './components/map/map.component';
import { Parcel, ParcelService } from './services/parcel.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MapComponent, CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css'
})
export class AppComponent {
  title = 'EthioProps';
  selectedParcel: Parcel | null = null;
  searchQuery: string = '';
  allParcels: Parcel[] = [];
  filteredParcels: Parcel[] = [];
  showSearchResults: boolean = false;
  
  // Layer toggles
  zoningLayerActive: boolean = true;
  parcelBoundariesActive: boolean = false;
  
  // Map style
  mapStyle: 'map' | 'satellite' | 'hybrid' = 'map';

  constructor(private parcelService: ParcelService) {
    this.loadParcels();
  }

  loadParcels() {
    this.parcelService.getParcels().subscribe({
      next: (parcels) => {
        this.allParcels = parcels;
      },
      error: (err) => console.error('Error loading parcels:', err)
    });
  }

  onParcelSelected(parcel: Parcel) {
    this.selectedParcel = parcel;
    this.showSearchResults = false;
    this.searchQuery = '';
  }

  clearSelection() {
    this.selectedParcel = null;
  }

  // Search functionality
  onSearch() {
    const query = this.searchQuery.trim().toLowerCase();
    
    if (!query) {
      this.filteredParcels = [];
      this.showSearchResults = false;
      return;
    }

    this.filteredParcels = this.allParcels.filter(parcel => 
      parcel.parcel_id.toLowerCase().includes(query) ||
      parcel.sub_city?.toLowerCase().includes(query) ||
      parcel.wereda?.toLowerCase().includes(query) ||
      parcel.street_name?.toLowerCase().includes(query) ||
      parcel.landmark?.toLowerCase().includes(query) ||
      parcel.owner_name?.toLowerCase().includes(query) ||
      parcel.property_type?.toLowerCase().includes(query) ||
      parcel.zoning_info?.toLowerCase().includes(query)
    );

    this.showSearchResults = true;
  }

  selectSearchResult(parcel: Parcel) {
    this.selectedParcel = parcel;
    this.showSearchResults = false;
    this.searchQuery = '';
    // Emit event to map to center on this parcel
    // TODO: Add method to center map on parcel
  }

  closeSearchResults() {
    this.showSearchResults = false;
  }

  // Get current location for breadcrumb
  getCurrentLocation(): string {
    if (this.selectedParcel && this.selectedParcel.sub_city) {
      return `${this.selectedParcel.sub_city} Sub-city`;
    }
    return 'All Areas';
  }

  // Layer toggles
  toggleZoningLayer() {
    this.zoningLayerActive = !this.zoningLayerActive;
    console.log('Zoning layer:', this.zoningLayerActive ? 'ON' : 'OFF');
    // TODO: Implement layer visibility toggle on map
  }

  toggleParcelBoundaries() {
    this.parcelBoundariesActive = !this.parcelBoundariesActive;
    console.log('Parcel boundaries:', this.parcelBoundariesActive ? 'ON' : 'OFF');
    // TODO: Implement parcel boundaries toggle
  }

  // Analysis tools
  showDevelopmentStats() {
    alert('Development Statistics:\n\nTotal Parcels: 10\nCommercial: 4\nResidential: 5\nIndustrial: 1\nAgricultural: 1\n\nTotal Area: 51,420 m²');
  }

  startAreaMeasurement() {
    alert('Area Measurement Tool:\n\nClick on the map to start measuring distances and areas.\n(Feature coming soon)');
  }

  // Header actions
  shareView() {
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(() => {
      alert('View link copied to clipboard!');
    }).catch(() => {
      alert(`Share this link:\n${url}`);
    });
  }

  createNewProject() {
    const projectName = prompt('Enter project name:');
    if (projectName) {
      alert(`Project "${projectName}" created!\n\nYou can now start adding parcels to your project.`);
    }
  }

  // Map style toggles
  setMapStyle(style: 'map' | 'satellite' | 'hybrid') {
    this.mapStyle = style;
    console.log('Map style changed to:', style);
  }

  // Drawer actions
  generateFullReport() {
    if (this.selectedParcel) {
      console.log('Generating report for:', this.selectedParcel.parcel_id);
      alert(`Generating full property report for:\n\nParcel ID: ${this.selectedParcel.parcel_id}\nOwner: ${this.selectedParcel.owner_name}\n\nPDF download will start shortly...`);
      // TODO: Implement PDF generation
    }
  }

  goToEntrance() {
    if (this.selectedParcel && this.selectedParcel.entry_lat && this.selectedParcel.entry_lng) {
      console.log('Navigating to entrance:', this.selectedParcel.entry_lat, this.selectedParcel.entry_lng);
      alert(`Navigation to entrance:\n\nLat: ${this.selectedParcel.entry_lat}\nLng: ${this.selectedParcel.entry_lng}\n\nMap will center on entrance point.`);
      // TODO: Implement map pan/zoom to entrance coordinates
    } else {
      alert('Entrance coordinates not available for this parcel.');
    }
  }
}
