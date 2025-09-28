import { Component, Inject } from '@angular/core';
import { MAT_DIALOG_DATA, MatDialogModule, MatDialogRef } from '@angular/material/dialog';
import { CommonModule } from '@angular/common';
import { MatButtonModule } from '@angular/material/button';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { FormsModule } from '@angular/forms';

@Component({
  selector: 'app-my-booking-dialog',
  standalone: true,
  imports: [CommonModule, MatDialogModule, MatButtonModule, MatFormFieldModule, MatInputModule, FormsModule],
  templateUrl: './my-booking-dialog.html',
  styleUrls: ['./my-booking-dialog.scss']
})
export class MyBookingDialog {
  email: string = '';
  constructor(private dialogRef: MatDialogRef<MyBookingDialog>) {}

  submit() {
    // return the email to the caller
    this.dialogRef.close(this.email);
  }

  cancel() {
    this.dialogRef.close(null);
  }
}
