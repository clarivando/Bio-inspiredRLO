import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ProfissionalDetailsComponent } from './profissional-details.component';

describe('ProfissionalDetailsComponent', () => {
  let component: ProfissionalDetailsComponent;
  let fixture: ComponentFixture<ProfissionalDetailsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ProfissionalDetailsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ProfissionalDetailsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
