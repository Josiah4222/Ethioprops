import { Component, ViewChild } from '@angular/core';
import { RouterOutlet } from '@angular/router';
import { MapComponent } from './components/map/map.component';
import { Parcel, ParcelService } from './services/parcel.service';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { trigger, state, style, transition, animate } from '@angular/animations';

@Component({
  selector: 'app-root',
  standalone: true,
  imports: [RouterOutlet, MapComponent, CommonModule, FormsModule],
  templateUrl: './app.component.html',
  styleUrl: './app.component.css',
  animations: [
    trigger('slideUp', [
      transition(':enter', [
        style({ transform: 'translateY(100%)', opacity: 0 }),
        animate('300ms ease-out', style({ transform: 'translateY(0)', opacity: 1 }))
      ]),
      transition(':leave', [
        animate('300ms ease-in', style({ transform: 'translateY(100%)', opacity: 0 }))
      ])
    ])
  ]
})
export class AppComponent {
  @ViewChild(MapComponent) mapComponent!: MapComponent;
  
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
  
  // Comparison
  comparisonList: number[] = [];
  showComparisonPanel: boolean = false;

  constructor(private parcelService: ParcelService) {
    this.loadParcels();
  }

  loadParcels() {
    this.parcelService.getParcels().subscribe({
      next: (response: any) => {
        this.allParcels = response.results || response;
      },
      error: (err) => console.error('Error loading parcels:', err)
    });
  }

  onParcelSelected(parcel: Parcel) {
    // Load full parcel details with amenities
    this.parcelService.getParcel(parcel.id).subscribe({
      next: (fullParcel) => {
        this.selectedParcel = fullParcel;
        this.showSearchResults = false;
        this.searchQuery = '';
        
        // Auto-add to comparison if comparison panel is open and not already added
        if (this.showComparisonPanel && !this.isInComparison(fullParcel.id)) {
          if (this.comparisonList.length < 4) {
            this.toggleComparison(fullParcel.id);
            console.log('Auto-added to comparison:', fullParcel.id);
          }
        }
      },
      error: (err) => {
        console.error('Error loading parcel details:', err);
        this.selectedParcel = parcel; // Fallback to basic info
      }
    });
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
  contactOwner() {
    if (this.selectedParcel) {
      const message = `I'm interested in the property:\n\nParcel ID: ${this.selectedParcel.parcel_id}\nLocation: ${this.selectedParcel.sub_city}, ${this.selectedParcel.landmark}\n\nPlease contact me with more information.`;
      
      if (this.selectedParcel.owner_email) {
        window.location.href = `mailto:${this.selectedParcel.owner_email}?subject=Inquiry about ${this.selectedParcel.parcel_id}&body=${encodeURIComponent(message)}`;
      } else if (this.selectedParcel.owner_phone) {
        alert(`Contact Owner:\n\nPhone: ${this.selectedParcel.owner_phone}\n\nYou can call or send a message to inquire about this property.`);
      } else {
        alert('Owner contact information not available.');
      }
    }
  }

  getAmenityIcon(type: string): string {
    const icons: any = {
      'SCHOOL': '🏫',
      'HOSPITAL': '🏥',
      'MARKET': '🛒',
      'BANK': '🏦',
      'TRANSPORT': '🚌',
      'RESTAURANT': '🍽️',
      'SHOPPING': '🛍️',
      'PARK': '🌳',
      'OTHER': '📍'
    };
    return icons[type] || '📍';
  }

  generateFullReport() {
    if (this.selectedParcel) {
      console.log('Generating report for:', this.selectedParcel.parcel_id);
      alert(`Generating full property report for:\n\nParcel ID: ${this.selectedParcel.parcel_id}\nTitle: ${this.selectedParcel.title}\nOwner: ${this.selectedParcel.owner_name}\nPrice: ${this.selectedParcel.sale_price ? this.selectedParcel.sale_price.toLocaleString() + ' ETB' : 'N/A'}\n\nPDF download will start shortly...`);
      // TODO: Implement PDF generation
    }
  }

  goToEntrance() {
    if (this.selectedParcel && this.selectedParcel.entry_lat && this.selectedParcel.entry_lng) {
      const lat = Number(this.selectedParcel.entry_lat);
      const lng = Number(this.selectedParcel.entry_lng);
      
      console.log('Navigating to entrance:', lat, lng);
      
      // Center map on entrance coordinates
      if (this.mapComponent) {
        this.mapComponent.centerOnLocation(lat, lng, 18);
      }
    } else {
      alert('Entrance coordinates not available for this parcel.');
    }
  }

  // Comparison functionality
  toggleComparison(parcelId: number) {
    const index = this.comparisonList.indexOf(parcelId);
    if (index > -1) {
      this.comparisonList.splice(index, 1);
    } else {
      if (this.comparisonList.length < 4) {
        this.comparisonList.push(parcelId);
      } else {
        alert('You can only compare up to 4 parcels at a time');
      }
    }
    this.showComparisonPanel = this.comparisonList.length > 0;
  }

  toggleComparisonAndKeepOpen(parcelId: number) {
    console.log('=== ADD TO COMPARE CLICKED ===');
    console.log('Parcel ID:', parcelId);
    console.log('Before - comparison list:', this.comparisonList);
    
    this.toggleComparison(parcelId);
    
    console.log('After - comparison list:', this.comparisonList);
    console.log('After - show panel:', this.showComparisonPanel);
    // Don't close the drawer - user can click another parcel
  }

  isInComparison(parcelId: number): boolean {
    return this.comparisonList.includes(parcelId);
  }

  removeFromComparison(parcelId: number) {
    const index = this.comparisonList.indexOf(parcelId);
    if (index > -1) {
      this.comparisonList.splice(index, 1);
    }
    this.showComparisonPanel = this.comparisonList.length > 0;
  }

  clearComparison() {
    this.comparisonList = [];
    this.showComparisonPanel = false;
  }

  compareSelected() {
    if (this.comparisonList.length >= 2) {
      // Show comparison in modal instead of new tab
      this.showComparisonModal = true;
      this.loadComparisonData();
    } else {
      alert('Please select at least 2 parcels to compare');
    }
  }

  showComparisonModal = false;
  comparisonData: Parcel[] = [];
  loadingComparison = false;

  loadComparisonData() {
    this.loadingComparison = true;
    this.parcelService.compareParcels(this.comparisonList).subscribe({
      next: (response) => {
        this.comparisonData = response.parcels;
        this.loadingComparison = false;
      },
      error: (err) => {
        console.error('Error loading comparison:', err);
        alert('Failed to load comparison data');
        this.loadingComparison = false;
        this.showComparisonModal = false;
      }
    });
  }

  closeComparisonModal() {
    this.showComparisonModal = false;
    this.comparisonData = [];
  }

  printComparison() {
    window.print();
  }

  getComparisonValue(parcel: Parcel, field: string): any {
    return (parcel as any)[field];
  }

  formatComparisonValue(value: any, type: string): string {
    if (value === null || value === undefined) return 'N/A';
    
    switch (type) {
      case 'currency':
        if (value >= 1000000) {
          return `${(value / 1000000).toFixed(2)}M ETB`;
        }
        return `${value.toLocaleString()} ETB`;
      case 'area':
        return `${value.toLocaleString()} m²`;
      case 'boolean':
        return value ? '✓ Yes' : '✗ No';
      case 'date':
        return new Date(value).toLocaleDateString();
      default:
        return value.toString();
    }
  }

  getComparisonParcels(): Parcel[] {
    return this.allParcels.filter(p => this.comparisonList.includes(p.id));
  }
}
