import { Component, signal } from '@angular/core';
import { HeaderComponent } from './shared/header-component/header-component';
import { RouterModule } from '@angular/router';

@Component({
  selector: 'app-root',
  imports: [HeaderComponent, RouterModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('playHubUI');
}
