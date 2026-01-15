import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { ParcelService, Parcel } from '../../services/parcel.service';

@Component({
  selector: 'app-parcel-comparison',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './parcel-comparison.component.html',
  styleUrls: ['./parcel-comparison.component.css']
})
export class ParcelComparisonComponent implements OnInit {
  parcels: Parcel[] = [];
  loading = false;
  error: string | null = null;

  // Comparison categories
  comparisonCategories = [
    {
      name: 'Basic Information',
      fields: [
        { key: 'parcel_id', label: 'Parcel ID', type: 'text' },
        { key: 'title', label: 'Title', type: 'text' },
        { key: 'property_type', label: 'Property Type', type: 'badge' },
        { key: 'status', label: 'Status', type: 'badge' },
        { key: 'listing_type', label: 'Listing Type', type: 'text' }
      ]
    },
    {
      name: 'Pricing',
      fields: [
        { key: 'sale_price', label: 'Sale Price', type: 'currency' },
        { key: 'lease_price_monthly', label: 'Monthly Lease', type: 'currency' },
        { key: 'price_per_sqm', label: 'Price per m²', type: 'currency' },
        { key: 'is_negotiable', label: 'Negotiable', type: 'boolean' }
      ]
    },
    {
      name: 'Property Details',
      fields: [
        { key: 'area_sqm', label: 'Area', type: 'area' },
        { key: 'dimensions', label: 'Dimensions', type: 'text' },
        { key: 'zoning_info', label: 'Zoning', type: 'text' }
      ]
    },
    {
      name: 'Location',
      fields: [
        { key: 'sub_city', label: 'Sub-City', type: 'text' },
        { key: 'wereda', label: 'Wereda', type: 'text' },
        { key: 'street_name', label: 'Street', type: 'text' },
        { key: 'landmark', label: 'Landmark', type: 'text' }
      ]
    },
    {
      name: 'Infrastructure',
      fields: [
        { key: 'has_electricity', label: 'Electricity', type: 'boolean' },
        { key: 'has_water', label: 'Water', type: 'boolean' },
        { key: 'has_sewage', label: 'Sewage', type: 'boolean' },
        { key: 'road_access', label: 'Road Access', type: 'text' }
      ]
    },
    {
      name: 'Owner Information',
      fields: [
        { key: 'owner_name', label: 'Owner', type: 'text' },
        { key: 'owner_phone', label: 'Phone', type: 'text' },
        { key: 'owner_email', label: 'Email', type: 'text' }
      ]
    },
    {
      name: 'Statistics',
      fields: [
        { key: 'views_count', label: 'Views', type: 'number' },
        { key: 'created_at', label: 'Listed Date', type: 'date' }
      ]
    }
  ];

  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private parcelService: ParcelService
  ) {}

  ngOnInit(): void {
    console.log('Comparison component initialized');
    this.route.queryParams.subscribe(params => {
      console.log('Query params:', params);
      const ids = params['ids'];
      if (ids) {
        const parcelIds = ids.split(',').map((id: string) => parseInt(id.trim()));
        console.log('Parsed parcel IDs:', parcelIds);
        this.loadParcels(parcelIds);
      } else {
        this.error = 'No parcels selected for comparison';
        console.error('No IDs in query params');
      }
    });
  }

  loadParcels(ids: number[]): void {
    console.log('Loading parcels for comparison:', ids);
    if (ids.length < 2 || ids.length > 4) {
      this.error = 'Please select 2-4 parcels to compare';
      console.error('Invalid number of parcels:', ids.length);
      return;
    }

    this.loading = true;
    this.error = null;

    console.log('Calling API to compare parcels...');
    this.parcelService.compareParcels(ids).subscribe({
      next: (response) => {
        console.log('Comparison response:', response);
        this.parcels = response.parcels;
        this.loading = false;
        console.log('Loaded parcels:', this.parcels);
      },
      error: (err) => {
        this.error = 'Failed to load parcels for comparison';
        this.loading = false;
        console.error('Error loading comparison:', err);
      }
    });
  }

  getFieldValue(parcel: Parcel, key: string): any {
    return (parcel as any)[key];
  }

  formatValue(value: any, type: string): string {
    if (value === null || value === undefined) return 'N/A';

    switch (type) {
      case 'currency':
        return this.formatCurrency(value);
      case 'area':
        return `${value.toLocaleString()} m²`;
      case 'boolean':
        return value ? '✓ Yes' : '✗ No';
      case 'date':
        return new Date(value).toLocaleDateString();
      case 'number':
        return value.toLocaleString();
      default:
        return value.toString();
    }
  }

  formatCurrency(value: number): string {
    if (!value) return 'N/A';
    if (value >= 1000000) {
      return `${(value / 1000000).toFixed(2)}M ETB`;
    }
    return `${value.toLocaleString()} ETB`;
  }

  getBestValue(field: any): number | null {
    if (field.type !== 'currency' && field.type !== 'area' && field.type !== 'number') {
      return null;
    }

    const values = this.parcels
      .map((p, index) => ({ value: this.getFieldValue(p, field.key), index }))
      .filter(v => v.value !== null && v.value !== undefined);

    if (values.length === 0) return null;

    // For price fields, lowest is best
    if (field.key.includes('price')) {
      return values.reduce((min, v) => v.value < min.value ? v : min).index;
    }

    // For area and other numbers, highest is best
    return values.reduce((max, v) => v.value > max.value ? v : max).index;
  }

  isBestValue(parcelIndex: number, field: any): boolean {
    const bestIndex = this.getBestValue(field);
    return bestIndex === parcelIndex;
  }

  removeParcel(index: number): void {
    const remainingIds = this.parcels
      .filter((_, i) => i !== index)
      .map(p => p.id)
      .join(',');
    
    if (remainingIds) {
      this.router.navigate(['/compare'], { queryParams: { ids: remainingIds } });
    } else {
      this.router.navigate(['/']);
    }
  }

  viewDetails(parcelId: number): void {
    window.open(`/parcel/${parcelId}`, '_blank');
  }

  exportToPDF(): void {
    window.print();
  }

  shareComparison(): void {
    const url = window.location.href;
    navigator.clipboard.writeText(url).then(() => {
      alert('Comparison link copied to clipboard!');
    }).catch(() => {
      alert(`Share this link:\n${url}`);
    });
  }

  backToSearch(): void {
    this.router.navigate(['/']);
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

  // Helper methods for summary section
  getLowestPriceParcel(): Parcel | null {
    if (this.parcels.length === 0) return null;
    return this.parcels.reduce((min, p) => {
      if (!min || (p.sale_price && (!min.sale_price || p.sale_price < min.sale_price))) {
        return p;
      }
      return min;
    });
  }

  getLargestAreaParcel(): Parcel | null {
    if (this.parcels.length === 0) return null;
    return this.parcels.reduce((max, p) => {
      if (!max || (p.area_sqm && (!max.area_sqm || p.area_sqm > max.area_sqm))) {
        return p;
      }
      return max;
    });
  }

  getBestPricePerSqmParcel(): Parcel | null {
    if (this.parcels.length === 0) return null;
    return this.parcels.reduce((min, p) => {
      if (!min || (p.price_per_sqm && (!min.price_per_sqm || p.price_per_sqm < min.price_per_sqm))) {
        return p;
      }
      return min;
    });
  }

  getMostViewedParcel(): Parcel | null {
    if (this.parcels.length === 0) return null;
    return this.parcels.reduce((max, p) => {
      if (!max || (p.views_count && (!max.views_count || p.views_count > max.views_count))) {
        return p;
      }
      return max;
    });
  }

  hasAmenities(): boolean {
    return this.parcels.some(p => p.amenities && p.amenities.length > 0);
  }

  getCurrentDate(): Date {
    return new Date();
  }
}
