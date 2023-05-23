import { TestBed } from '@angular/core/testing';
import { ResultsService } from './results.service';

describe('ResultsService', () => {
  let service: ResultsService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ResultsService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should set and get results correctly', (done: DoneFn) => {
    const testResults = [{ data: 'test' }];
    service.setResults(testResults);

    service.getResults().subscribe((results) => {
      expect(results).toEqual(testResults);
      done();
    });
  });
});
