import { TestBed } from '@angular/core/testing';

import { IdealLearnObjService } from './ideal-learn-obj.service';

describe('IdealLearnObjService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: IdealLearnObjService = TestBed.get(IdealLearnObjService);
    expect(service).toBeTruthy();
  });
});
