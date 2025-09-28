import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

interface Booking {
  serial: number;
  sportType: string;
  courtDateTime: string;
  status: 'Booked' | 'Pending' | 'Cancelled';
}

@Component({
  selector: 'app-bookings',
  imports: [CommonModule],
  templateUrl: './my-booking-component.html', // file must exist in same folder
  styleUrls: ['./my-booking-component.scss'],
  standalone: true,
})
export class MyBookingComponent{
  bookings: Booking[] = [
    { serial: 1, sportType: 'Tennis', courtDateTime: '2025-10-05 10:00 AM', status: 'Booked' },
    { serial: 2, sportType: 'Badminton', courtDateTime: '2025-10-06 02:00 PM', status: 'Pending' },
    { serial: 3, sportType: 'Basketball', courtDateTime: '2025-10-07 06:00 PM', status: 'Cancelled' },
  ];

  getStatusClass(status: string): string {
    switch (status) {
      case 'Booked': return 'status-booked';
      case 'Pending': return 'status-pending';
      case 'Cancelled': return 'status-cancelled';
      default: return '';
    }
  }
}
