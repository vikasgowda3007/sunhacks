
import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-faq',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './faqs-component.html',
  styleUrls: ['./faqs-component.scss']
})
export class FaqsComponent {
  faqs = [
    {
      question: 'What is this website about?',
      answer: 'A platform that lets you check court availability and reserve courts for your preferred sport, time, and proficiency level. You can book as a group or as an individual, and we even auto-pair individual players with others of similar skill.',
      open: false
    },
    {
      question: 'How do I reserve a court?',
      answer: 'Choose your sport, select a date and time, specify your proficiency, and indicate whether you are booking as a group or individual. For individual players, the system can automatically pair you with others who match your skill level. Confirm your booking and your court is reserved',
      open: false
    },
    {
      question: 'Can I cancel my booking?',
      answer: 'Yes, bookings can be canceled before the reserved time.',
      open: false
    },
    {
      question: 'Is there a fee to reserve a court?',
      answer: 'Reservations are free of cost.',
      open: false
    },
    {
      question: 'How does auto-pairing work?',
      answer: 'If you book as an individual, the system will automatically match you with other users of similar proficiency for the same sport and time slot.',
      open: false
    },
    {
      question: 'Can I see who I am paired with?',
      answer: 'Once the pairing is confirmed, you will see the names of your playing partners.',
      open: false
    },
    {
      question: 'How do I report an issue with a court or booking?',
      answer: 'Contact support via email or the contact form on the website.',
      open: false
    }
  ];

  toggleFAQ(faq: any) {
    faq.open = !faq.open;
  }
}

