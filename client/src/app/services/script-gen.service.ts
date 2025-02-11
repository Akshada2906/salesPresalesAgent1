import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable, throwError } from 'rxjs';
import { catchError, retryWhen, delay, take, concatMap } from 'rxjs/operators';

@Injectable({
  providedIn: 'root',
})
export class ScriptGenService {
  private apiUrl = 'http://127.0.0.1:8000';

  constructor(private http: HttpClient) {}

  // Method to fetch client research data with retry logic
  getClientResearchData(prospectName: string, prospectPosition: string, companyName: string): Observable<any> {
    return this.http.post(`${this.apiUrl}/client_research`, {
      prospect_name: prospectName,
      prospect_position: prospectPosition,
      company_name: companyName
    }).pipe(
      retryWhen(errors =>
        errors.pipe(
          delay(2000),  // Wait for 2 seconds before retry
          take(3),  // Retry 3 times
          concatMap((e, index) => {
            if (index === 2) {
              return throwError(() => new Error('Service is still unavailable. Please try again later.'));
            }
            return throwError(() => e);
          })
        )
      ),
      catchError((err) => {
        return throwError(() => err);
      })
    );
  }
}
