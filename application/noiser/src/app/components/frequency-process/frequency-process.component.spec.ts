import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { FrequencyProcessComponent } from './frequency-process.component';

describe('FrequencyProcessComponent', () => {
  let component: FrequencyProcessComponent;
  let fixture: ComponentFixture<FrequencyProcessComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ FrequencyProcessComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(FrequencyProcessComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
