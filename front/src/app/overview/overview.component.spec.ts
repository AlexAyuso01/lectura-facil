import { HttpClientTestingModule } from '@angular/common/http/testing';
import { ComponentFixture, TestBed } from '@angular/core/testing';
import { Router } from '@angular/router';
import { RouterTestingModule } from '@angular/router/testing';
import { ToastrService } from 'ngx-toastr';
import { of, throwError } from 'rxjs';
import { ResultsService } from '../service/results.service';
import { SimilarityService } from '../service/similarity.service';
import { CustomToasterComponent } from '../custom-toaster/custom-toaster.component';
import { OverviewComponent } from './overview.component';

describe('OverviewComponent', () => {
  let component: OverviewComponent;
  let fixture: ComponentFixture<OverviewComponent>;
  let similarityService: SimilarityService;
  let resultsService: ResultsService;
  let toastr: ToastrService;
  let router: Router;
  let calculateSimilaritiesSpy: jasmine.Spy;
  let setResultsSpy: jasmine.Spy;
  let errorSpy: jasmine.Spy;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [OverviewComponent],
      imports: [HttpClientTestingModule, RouterTestingModule],
      providers: [
        {
          provide: SimilarityService,
          useValue: { calculateSimilarities: () => {} },
        },
        { provide: ResultsService, useValue: { setResults: () => {} } },
        { provide: ToastrService, useValue: { error: () => {} } },
      ],
    }).compileComponents();

    fixture = TestBed.createComponent(OverviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();

    similarityService = TestBed.inject(SimilarityService);
    resultsService = TestBed.inject(ResultsService);
    toastr = TestBed.inject(ToastrService);
    router = TestBed.inject(Router);

    calculateSimilaritiesSpy = spyOn(
      similarityService,
      'calculateSimilarities'
    );
    setResultsSpy = spyOn(resultsService, 'setResults');
    errorSpy = spyOn(toastr, 'error');
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should set file when onFileSelected is called with event', () => {
    const blob = new Blob(['test-file'], { type: 'text/plain' });
    const file = new File([blob], 'test.txt');
    const event = {
      target: {
        files: [file],
      },
    } as any;

    component.onFileSelected(event);
    expect(component.file).toEqual(file);
  });

  it('should not call calculateSimilarities when onSubmit is called without file', () => {
    component.onSubmit();
    expect(calculateSimilaritiesSpy).not.toHaveBeenCalled();
  });

  it('should call calculateSimilarities and handle response when onSubmit is called with file', () => {
    const navigateSpy = spyOn(router, 'navigate');
    const response = ['test-response'];
    calculateSimilaritiesSpy.and.returnValue(of(response));

    const blob = new Blob(['test-file'], { type: 'text/plain' });
    const file = new File([blob], 'test.txt');
    component.file = file;

    component.onSubmit();

    expect(calculateSimilaritiesSpy).toHaveBeenCalledWith(file);
    expect(setResultsSpy).toHaveBeenCalledWith(response);
    expect(navigateSpy).toHaveBeenCalledWith(['/results']);
    expect(component.results).toEqual(response);
    expect(component.isLoading).toBeFalse();
  });

  it('should handle error when calculateSimilarities fails', () => {
    const errorResponse = new Error('test-error');
    calculateSimilaritiesSpy.and.returnValue(throwError(errorResponse));

    const blob = new Blob(['test-file'], { type: 'text/plain' });
    const file = new File([blob], 'test.txt');
    component.file = file;

    component.onSubmit();

    expect(calculateSimilaritiesSpy).toHaveBeenCalledWith(file);
    expect(errorSpy).toHaveBeenCalledWith(
      'Se produjo un error al calcular las similitudes: el formato del CSV no es correcto',
      'Error',
      {
        toastComponent: CustomToasterComponent,
        timeOut: 10000,
      }
    );
    expect(component.isLoading).toBeFalse();
  });
});
