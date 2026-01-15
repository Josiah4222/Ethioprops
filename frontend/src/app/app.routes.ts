import { Routes } from '@angular/router';
import { ParcelDetailComponent } from './components/parcel-detail/parcel-detail.component';
import { ParcelComparisonComponent } from './components/parcel-comparison/parcel-comparison.component';

export const routes: Routes = [
  { path: 'parcel/:id', component: ParcelDetailComponent },
  { path: 'compare', component: ParcelComparisonComponent },
  { path: '', pathMatch: 'full', redirectTo: '' }
];
