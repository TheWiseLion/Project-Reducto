/* tslint:disable:no-unused-variable */

import { TestBed, async, inject } from '@angular/core/testing';
import { ReductoService } from './reducto-service.service';

describe('ReductoService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [ReductoService]
    });
  });

  it('should ...', inject([ReductoService], (service: ReductoService) => {
    expect(service).toBeTruthy();
  }));
});
