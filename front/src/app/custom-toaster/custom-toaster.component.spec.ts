import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CustomToasterComponent } from './custom-toaster.component';

describe('CustomToasterComponent', () => {
  let component: CustomToasterComponent;
  let fixture: ComponentFixture<CustomToasterComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CustomToasterComponent]
    });
    fixture = TestBed.createComponent(CustomToasterComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
