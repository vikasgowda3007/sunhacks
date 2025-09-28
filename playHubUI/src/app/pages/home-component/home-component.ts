import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';

@Component({
  selector: 'app-home-component',
  standalone: true,
  imports: [CommonModule],
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
}
