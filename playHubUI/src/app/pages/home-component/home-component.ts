import { CommonModule } from '@angular/common';
import { Component, ElementRef, inject, OnInit, ViewChild } from '@angular/core';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';
import { MatButtonModule } from '@angular/material/button';
import { HttpClient, HttpClientModule } from '@angular/common/http';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { MatDialog, MatDialogModule } from '@angular/material/dialog';
import { ResponseDialogComponent } from '../../shared/response-dialog/response-dialog';

@Component({
  selector: 'app-home-component',
  standalone: true,
  imports: [CommonModule, MatFormFieldModule, MatInputModule, MatSelectModule, FormsModule, MatRadioModule, MatButtonModule, HttpClientModule, MatProgressSpinnerModule, MatDialogModule],
  templateUrl: './home-component.html',
  styleUrls: ['./home-component.scss'], // optional CSS file
})
export class HomeComponent {
  intervalId: any;

  constructor(private http: HttpClient) { }
  formData = {
    name: '',
    sport: '',
    proficiency: '',
    date: '',
    time: '',
    type: ''
  };

  readonly dialog = inject(MatDialog);

  @ViewChild('loader') loaderRef!: ElementRef<HTMLDivElement>;

  current = 0;
  slidesArray = [1, 2, 3]; // Number of slides

  nextSlide() {
    this.current = (this.current + 1) % this.slidesArray.length;
  }

  prevSlide() {
    this.current = (this.current - 1 + this.slidesArray.length) % this.slidesArray.length;
  }

  goToSlide(index: number) {
    this.current = index;
  }

  isDateTimeValid(): boolean {
    // Combine date & time
    const [hours, minutes] = this.formData.time.split(':').map(Number);
    const selected = new Date(this.formData.date);
    selected.setHours(hours, minutes, 0, 0);

    // Convert current time to MST (UTC-7)
    const nowUtc = new Date();
    const nowMST = new Date(nowUtc.getTime() - 7 * 60 * 60 * 1000);
    console.log('Selected:', selected, 'Now (MST):', nowMST);

    return selected.getTime() > nowMST.getTime();
  }

  findMatch(form: any) {
    if (form.invalid) return;

    if (!this.isDateTimeValid()) {
      alert('Date and time must be in the future (MST).');
      return;
    }

    this.loaderRef.nativeElement.classList.add('active');

    console.log('Form Data:', form.value);

    setTimeout(() => {
      this.http.post('http://localhost:3000/api/book', this.formData).subscribe({
        next: (res) => {
          console.log('Success:', res);
          this.dialog.open(ResponseDialogComponent, {
            data: { message: 'Match found successfully!' }
          });
          // You can add additional response checks here if needed
          this.loaderRef.nativeElement.classList.remove('active');
        },
        error: (err) => {
          this.dialog.open(ResponseDialogComponent, {
            data: { message: 'Failed to find match.' }
          });
          console.error('Error:', err);
          this.loaderRef.nativeElement.classList.remove('active');
        }
      });
    }, 10000);
  }
}
