import { ComponentFixture, TestBed } from '@angular/core/testing';
import { RouterTestingModule } from '@angular/router/testing';
import { ResultsComponent } from './results.component';
import { of, BehaviorSubject } from 'rxjs';
import { SimilarityService } from '../service/similarity.service';
import { ResultsService } from '../service/results.service';

describe('ResultsComponent', () => {
  let component: ResultsComponent;
  let fixture: ComponentFixture<ResultsComponent>;
  let mockSimilarityService: any;
  let mockResultsService: any;

  beforeEach(async () => {
    mockSimilarityService = {
      modelNames: ['Model1', 'Model2'],
      calculateAccuracy: jasmine.createSpy('calculateAccuracy').and.returnValue([90, 85])
    };

    const results = new BehaviorSubject<any[]>([]);
    mockResultsService = {
      getResults: jasmine.createSpy('getResults').and.returnValue(results.asObservable()),
      setResults: jasmine.createSpy('setResults').and.callFake(newResults => {
        results.next(newResults);
      })
    };

    await TestBed.configureTestingModule({
      declarations: [ResultsComponent],
      imports: [RouterTestingModule],
      providers: [
        { provide: SimilarityService, useValue: mockSimilarityService },
        { provide: ResultsService, useValue: mockResultsService }
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(ResultsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
  
  it('should update results when ResultsService emits new values', () => {
    const newResults = [{ id: 1 }, { id: 2 }];
    mockResultsService.setResults(newResults);
    expect(component.results).toEqual(newResults);
    expect(mockSimilarityService.calculateAccuracy).toHaveBeenCalledWith(newResults);
  });
  
});
