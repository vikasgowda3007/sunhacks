import { AfterViewInit, Component, ElementRef, inject, OnInit, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatDialog } from '@angular/material/dialog';
import { MyBookingDialog } from '../../shared/my-booking-dialog/my-booking-dialog';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';

interface Booking {
  serial: number;
  sportType: string;
  courtDateTime: string;
  status: 'Booked' | 'Pending' | 'Cancelled';
}

@Component({
  selector: 'app-bookings',
  imports: [CommonModule, HttpClientModule, MatProgressSpinnerModule],
  templateUrl: './my-booking-component.html', // file must exist in same folder
  styleUrls: ['./my-booking-component.scss'],
  standalone: true,
})
export class MyBookingComponent {
  bookings: Booking[] = [
    { serial: 1, sportType: 'Tennis', courtDateTime: '2025-10-05 10:00 AM', status: 'Booked' },
    { serial: 2, sportType: 'Badminton', courtDateTime: '2025-10-06 02:00 PM', status: 'Pending' },
    { serial: 3, sportType: 'Basketball', courtDateTime: '2025-10-07 06:00 PM', status: 'Cancelled' },
  ];

  @ViewChild('loader') loaderRef!: ElementRef<HTMLDivElement>;
  @ViewChild('myBookingsTable') myBookingsTableRef!: ElementRef<HTMLTableElement>;

  private dialog = inject(MatDialog);

  constructor(private http: HttpClient) {
    // Wait a tick before opening the dialog
    setTimeout(() => {
      const dialogRef = this.dialog.open(MyBookingDialog, {
        width: '400px'
      });

      dialogRef.afterClosed().subscribe((email: string | null) => {
        if (email) {
          this.loaderRef.nativeElement.classList.add('active');
          this.http.post('http://localhost:3000/api/my-booking', {email: email}).subscribe({
            next: (res) => {
              console.log('Success:', res);
              this.loaderRef.nativeElement.classList.remove('active');
            },
            error: (err) => {
              this.loaderRef.nativeElement.classList.remove('active');
            }
          });
          console.log('Entered email:', email);
        } else {
          console.log('Dialog closed without input.');
        }
      });
    });
  }

  getStatusClass(status: string): string {
    switch (status) {
      case 'Booked': return 'status-booked';
      case 'Pending': return 'status-pending';
      case 'Cancelled': return 'status-cancelled';
      default: return '';
    }
  }
}
