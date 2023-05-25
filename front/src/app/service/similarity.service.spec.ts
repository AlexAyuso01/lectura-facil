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

  it('should calculate metrics accurately', () => {
    const mockResults = [
      { etiqueta_real: 'SI', predicciones: ['SI', 'NO', 'NO'] },
      { etiqueta_real: 'NO', predicciones: ['NO', 'SI', 'NO'] },
      { etiqueta_real: 'SI', predicciones: ['SI', 'SI', 'SI'] },
    ];
    const expectedMetrics = [
      { accuracy: 1, precision: 1, recall: 1, f1Score: 1 },
      { accuracy: 1 / 3, precision: 0.5, recall: 0.5, f1Score: 0.5 },
      { accuracy: 2 / 3, precision: 1, recall: 0.5, f1Score: 0.67 },
    ];

    const metrics = service.calculateMetrics(mockResults);

    for (let i = 0; i < metrics.length; i++) {
      expect(metrics[i].accuracy).toBeCloseTo(expectedMetrics[i].accuracy, 2);
      expect(metrics[i].precision).toBeCloseTo(expectedMetrics[i].precision, 2);
      expect(metrics[i].recall).toBeCloseTo(expectedMetrics[i].recall, 2);
      expect(metrics[i].f1Score).toBeCloseTo(expectedMetrics[i].f1Score, 2);
    }
  });
});
