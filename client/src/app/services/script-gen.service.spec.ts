import { TestBed } from '@angular/core/testing';

import { ScriptGenService } from './script-gen.service';

describe('ScriptGenService', () => {
  let service: ScriptGenService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ScriptGenService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
