import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { IdealLearnObjCreateComponent } from './ideal-learn-obj-create.component';

describe('IdealLearnObjCreateComponent', () => {
  let component: IdealLearnObjCreateComponent;
  let fixture: ComponentFixture<IdealLearnObjCreateComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ IdealLearnObjCreateComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(IdealLearnObjCreateComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
