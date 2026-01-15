import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router, RouterModule } from '@angular/router';
import { ParcelService, Parcel, ParcelFilters } from '../../services/parcel.service';

@Component({
  selector: 'app-parcel-list',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './parcel-list.component.html',
  styleUrls: ['./parcel-list.component.css']
})
export class ParcelListComponent implements OnInit {
  parcels: Parcel[] = [];
  filteredParcels: Parcel[] = [];
  loading = false;
  error: string | null = null;
  
  // Filter properties
  filters: ParcelFilters = {
    property_type: '',
    listing_type: '',
    sub_city: '',
    wereda: '',
    min_price: undefined,
    max_price: undefined,
    min_area: undefined,
    max_area: undefined,
    has_electricity: undefined,
    has_water: undefined,
    has_sewage: undefined,
    search: '',
    ordering: '-created_at'
  };
  
  // Filter options
  propertyTypes = ['RESIDENTIAL', 'COMMERCIAL', 'INDUSTRIAL', 'AGRICULTURAL'];
  listingTypes = ['SALE', 'LEASE', 'BOTH'];
  subCities = ['Bole', 'Kirkos', 'Yeka', 'Arada', 'Gulele', 'Nifas Silk-Lafto', 'Addis Ketema', 'Lideta', 'Kolfe Keranio', 'Akaki Kality'];
  sortOptions = [
    { value: '-created_at', label: 'Newest First' },
    { value: 'created_at', label: 'Oldest First' },
    { value: 'sale_price', label: 'Price: Low to High' },
    { value: '-sale_price', label: 'Price: High to Low' },
    { value: 'area_sqm', label: 'Area: Small to Large' },
    { value: '-area_sqm', label: 'Area: Large to Small' },
    { value: '-views_count', label: 'Most Viewed' }
  ];
  
  // Comparison
  comparisonList: number[] = [];
  
  // View mode
  viewMode: 'grid' | 'list' = 'grid';
  
  constructor(
    private parcelService: ParcelService,
    private router: Router
  ) {}
  
  ngOnInit(): void {
    this.loadParcels();
  }
  
  loadParcels(): void {
    this.loading = true;
    this.error = null;
    
    this.parcelService.getParcels(this.filters).subscribe({
      next: (response) => {
        this.parcels = response.results || response;
        this.filteredParcels = this.parcels;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load parcels. Please try again.';
        this.loading = false;
        console.error('Error loading parcels:', err);
      }
    });
  }
  
  applyFilters(): void {
    this.loadParcels();
  }
  
  resetFilters(): void {
    this.filters = {
      property_type: '',
      listing_type: '',
      sub_city: '',
      wereda: '',
      min_price: undefined,
      max_price: undefined,
      min_area: undefined,
      max_area: undefined,
      has_electricity: undefined,
      has_water: undefined,
      has_sewage: undefined,
      search: '',
      ordering: '-created_at'
    };
    this.loadParcels();
  }
  
  toggleComparison(parcelId: number): void {
    const index = this.comparisonList.indexOf(parcelId);
    if (index > -1) {
      this.comparisonList.splice(index, 1);
    } else {
      if (this.comparisonList.length < 3) {
        this.comparisonList.push(parcelId);
      } else {
        alert('You can only compare up to 3 parcels at a time');
      }
    }
  }
  
  isInComparison(parcelId: number): boolean {
    return this.comparisonList.includes(parcelId);
  }
  
  compareSelected(): void {
    if (this.comparisonList.length >= 2) {
      this.router.navigate(['/compare'], { 
        queryParams: { ids: this.comparisonList.join(',') } 
      });
    } else {
      alert('Please select at least 2 parcels to compare');
    }
  }
  
  viewDetails(parcelId: number): void {
    this.router.navigate(['/parcel', parcelId]);
  }
  
  formatPrice(price: number | undefined): string {
    if (!price) return 'N/A';
    return new Intl.NumberFormat('en-ET', {
      style: 'currency',
      currency: 'ETB',
      minimumFractionDigits: 0
    }).format(price);
  }
  
  formatArea(area: number | undefined): string {
    if (!area) return 'N/A';
    return `${area.toLocaleString()} m²`;
  }
  
  toggleViewMode(): void {
    this.viewMode = this.viewMode === 'grid' ? 'list' : 'grid';
  }
}
