import { Component, signal } from '@angular/core';
import { HomeComponent } from './pages/home-component/home-component';
import { HeaderComponent } from './shared/header-component/header-component';
import { RouterModule } from '@angular/router';
import { routes } from './app.routes';

@Component({
  selector: 'app-root',
  imports: [HomeComponent, HeaderComponent, RouterModule],
  templateUrl: './app.html',
  styleUrl: './app.scss'
})
export class App {
  protected readonly title = signal('playHubUI');
}
