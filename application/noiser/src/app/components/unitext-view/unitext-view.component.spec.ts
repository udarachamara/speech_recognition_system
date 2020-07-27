import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { UnitextViewComponent } from './unitext-view.component';

describe('UnitextViewComponent', () => {
  let component: UnitextViewComponent;
  let fixture: ComponentFixture<UnitextViewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ UnitextViewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(UnitextViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
