import { HttpClient, HttpHeaders } from "@angular/common/http";
import { Injectable } from "@angular/core";
import { BehaviorSubject, Observable } from "rxjs";

@Injectable({
  providedIn: "root",
})
export class HttpRequestService {
  httpOptions = {
    headers: new HttpHeaders({ "Content-Type": "application/json" }),
    time: new Date(),
  };

  constructor(private http: HttpClient) {}
  get(url: any): Observable<any> {
    return this.http.get(url, this.httpOptions);
  }

  getWithExplicitHttpOption(url: any, httpOptions: any): Observable<any> {
    return this.http.get(url, httpOptions);
  }

  post(url: any, postData: any): Observable<any> {
    return this.http.post(url, postData, this.httpOptions);
  }

  put(url: any, postData: any): Observable<any> {
    return this.http.put(url, postData, this.httpOptions);
  }

  delete(url: any): Observable<any> {
    return this.http.delete(url, this.httpOptions);
  }
}
