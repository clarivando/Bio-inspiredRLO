import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CrloComponent } from './crlo.component';

describe('CrloComponent', () => {
  let component: CrloComponent;
  let fixture: ComponentFixture<CrloComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CrloComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CrloComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
