import { Routes } from '@angular/router';
import { HomeComponent } from './pages/home-component/home-component';
import { MyBookingComponent } from './pages/my-booking-component/my-booking-component';
import { FaqsComponent } from './pages/faqs-component/faqs-component';

export const routes: Routes = [
    { path: '', redirectTo: '/home', pathMatch: 'full' }, // default route
    { path: 'home', component: HomeComponent },
    { path: 'my-booking', component: MyBookingComponent },
    { path: 'faqs', component: FaqsComponent }
];
