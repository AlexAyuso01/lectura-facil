import { TestBed } from '@angular/core/testing';
import {
  HttpClientTestingModule,
  HttpTestingController,
} from '@angular/common/http/testing';
import { SimilarityService } from './similarity.service';
import { HttpClient } from '@angular/common/http';
import { of } from 'rxjs';

describe('SimilarityService', () => {
  let service: SimilarityService;
  let httpMock: HttpTestingController;
  let httpClientSpy: jasmine.SpyObj<HttpClient>;

  beforeEach(() => {
    const spy = jasmine.createSpyObj('HttpClient', ['post']);

    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [SimilarityService, { provide: HttpClient, useValue: spy }],
    });

    httpClientSpy = TestBed.inject(HttpClient) as jasmine.SpyObj<HttpClient>;
    service = TestBed.inject(SimilarityService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify();
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  it('should post file to calculate similarities', () => {
    const mockFile = new File([''], 'filename', { type: 'text/plain' });
    const mockResponse = 'response';

    httpClientSpy.post.and.returnValue(of(mockResponse));

    service
      .calculateSimilarities(mockFile)
      .subscribe(
        (data) => expect(data).toEqual(mockResponse, 'expected data'),
        fail
      );

    expect(httpClientSpy.post.calls.count()).toBe(1, 'one call');
  });

  it('should calculate accuracies correctly', () => {
    const mockResults = [
      { etiqueta_real: 1, predicciones: [1, 0, 0] },
      { etiqueta_real: 0, predicciones: [0, 1, 0] },
      { etiqueta_real: 1, predicciones: [1, 1, 1] },
    ];
    const expectedAccuracies = [1, 1/3, 2/3];

    const accuracies = service.calculateAccuracy(mockResults);

    expect(accuracies).toEqual(expectedAccuracies);
  });
});
