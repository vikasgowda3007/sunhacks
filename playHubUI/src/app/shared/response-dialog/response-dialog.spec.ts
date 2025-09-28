import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ResponseDialog } from './response-dialog';

describe('ResponseDialog', () => {
  let component: ResponseDialog;
  let fixture: ComponentFixture<ResponseDialog>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ResponseDialog]
    })
    .compileComponents();

    fixture = TestBed.createComponent(ResponseDialog);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
