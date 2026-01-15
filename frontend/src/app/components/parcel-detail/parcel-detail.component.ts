import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ActivatedRoute, Router, RouterModule } from '@angular/router';
import { ParcelService, Parcel, Inquiry } from '../../services/parcel.service';

@Component({
  selector: 'app-parcel-detail',
  standalone: true,
  imports: [CommonModule, FormsModule, RouterModule],
  templateUrl: './parcel-detail.component.html',
  styleUrls: ['./parcel-detail.component.css']
})
export class ParcelDetailComponent implements OnInit {
  parcel: Parcel | null = null;
  loading = false;
  error: string | null = null;
  
  // Image gallery
  selectedImageIndex = 0;
  
  // Inquiry form
  showInquiryForm = false;
  inquiry: Inquiry = {
    parcel: 0,
    name: '',
    email: '',
    phone: '',
    message: '',
    inquiry_type: 'INFO'
  };
  inquirySubmitting = false;
  inquirySuccess = false;
  
  // Distance calculator
  showDistanceCalculator = false;
  targetLocation = { lat: 0, lng: 0, name: '' };
  calculatedDistance: number | null = null;
  
  // Share
  showShareOptions = false;
  
  constructor(
    private route: ActivatedRoute,
    private router: Router,
    private parcelService: ParcelService
  ) {}
  
  ngOnInit(): void {
    this.route.params.subscribe(params => {
      const id = +params['id'];
      if (id) {
        this.loadParcel(id);
      }
    });
  }
  
  loadParcel(id: number): void {
    this.loading = true;
    this.error = null;
    
    this.parcelService.getParcel(id).subscribe({
      next: (parcel) => {
        this.parcel = parcel;
        this.inquiry.parcel = parcel.id;
        this.loading = false;
      },
      error: (err) => {
        this.error = 'Failed to load parcel details.';
        this.loading = false;
        console.error('Error loading parcel:', err);
      }
    });
  }
  
  selectImage(index: number): void {
    this.selectedImageIndex = index;
  }
  
  nextImage(): void {
    if (this.parcel && this.parcel.images) {
      this.selectedImageIndex = (this.selectedImageIndex + 1) % this.parcel.images.length;
    }
  }
  
  prevImage(): void {
    if (this.parcel && this.parcel.images) {
      this.selectedImageIndex = this.selectedImageIndex === 0 
        ? this.parcel.images.length - 1 
        : this.selectedImageIndex - 1;
    }
  }
  
  toggleInquiryForm(): void {
    this.showInquiryForm = !this.showInquiryForm;
    this.inquirySuccess = false;
  }
  
  submitInquiry(): void {
    if (!this.inquiry.name || !this.inquiry.email || !this.inquiry.phone || !this.inquiry.message) {
      alert('Please fill in all required fields');
      return;
    }
    
    this.inquirySubmitting = true;
    
    this.parcelService.submitInquiry(this.inquiry).subscribe({
      next: () => {
        this.inquirySuccess = true;
        this.inquirySubmitting = false;
        this.inquiry = {
          parcel: this.parcel!.id,
          name: '',
          email: '',
          phone: '',
          message: '',
          inquiry_type: 'INFO'
        };
        setTimeout(() => {
          this.showInquiryForm = false;
          this.inquirySuccess = false;
        }, 3000);
      },
      error: (err) => {
        alert('Failed to submit inquiry. Please try again.');
        this.inquirySubmitting = false;
        console.error('Error submitting inquiry:', err);
      }
    });
  }
  
  toggleDistanceCalculator(): void {
    this.showDistanceCalculator = !this.showDistanceCalculator;
    this.calculatedDistance = null;
  }
  
  calculateDistance(): void {
    if (!this.parcel || !this.targetLocation.lat || !this.targetLocation.lng) {
      alert('Please enter valid coordinates');
      return;
    }
    
    this.parcelService.calculateDistance(
      this.parcel.id,
      this.targetLocation.lat,
      this.targetLocation.lng
    ).subscribe({
      next: (result) => {
        this.calculatedDistance = result.distance_km;
      },
      error: (err) => {
        alert('Failed to calculate distance');
        console.error('Error calculating distance:', err);
      }
    });
  }
  
  printPage(): void {
    window.print();
  }
  
  exportToPDF(): void {
    // In a real app, you'd use a library like jsPDF
    alert('PDF export functionality would be implemented here');
  }
  
  toggleShare(): void {
    this.showShareOptions = !this.showShareOptions;
  }
  
  shareVia(platform: string): void {
    const url = window.location.href;
    const title = this.parcel?.title || 'Property Listing';
    
    let shareUrl = '';
    switch (platform) {
      case 'facebook':
        shareUrl = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`;
        break;
      case 'twitter':
        shareUrl = `https://twitter.com/intent/tweet?url=${encodeURIComponent(url)}&text=${encodeURIComponent(title)}`;
        break;
      case 'whatsapp':
        shareUrl = `https://wa.me/?text=${encodeURIComponent(title + ' ' + url)}`;
        break;
      case 'email':
        shareUrl = `mailto:?subject=${encodeURIComponent(title)}&body=${encodeURIComponent(url)}`;
        break;
    }
    
    if (shareUrl) {
      window.open(shareUrl, '_blank');
    }
  }
  
  copyLink(): void {
    navigator.clipboard.writeText(window.location.href).then(() => {
      alert('Link copied to clipboard!');
    });
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
}
