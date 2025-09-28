import { ComponentFixture, TestBed } from '@angular/core/testing';

import { MyBookingDialog } from './my-booking-dialog';

describe('MyBookingDialog', () => {
  let component: MyBookingDialog;
  let fixture: ComponentFixture<MyBookingDialog>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [MyBookingDialog]
    })
    .compileComponents();

    fixture = TestBed.createComponent(MyBookingDialog);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
