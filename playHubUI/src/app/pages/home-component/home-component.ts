import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import {MatSelectModule} from '@angular/material/select';
import {MatInputModule} from '@angular/material/input';
import {MatFormFieldModule} from '@angular/material/form-field';
import { FormsModule } from '@angular/forms';
import { MatRadioModule } from '@angular/material/radio';

@Component({
  selector: 'app-home-component',
  standalone: true,
  imports: [CommonModule, MatFormFieldModule, MatInputModule, MatSelectModule, FormsModule, MatRadioModule],
  templateUrl: './home-component.html',
  styleUrls: ['./home-component.scss'], // optional CSS file
})
export class HomeComponent {
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

  findMatch() {
    // Logic to find a match
    console.log('Finding a match...');
  }
}
