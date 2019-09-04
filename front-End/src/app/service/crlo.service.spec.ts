import { TestBed } from '@angular/core/testing';

import { CrloService } from './crlo.service';

describe('CrloService', () => {
  beforeEach(() => TestBed.configureTestingModule({}));

  it('should be created', () => {
    const service: CrloService = TestBed.get(CrloService);
    expect(service).toBeTruthy();
  });
});
