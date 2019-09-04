import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { IdealLearnObj } from '../model/ideal-learn-obj';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class IdealLearnObjService {
  private baseUrl = 'http://localhost:8000/ideallos';

  constructor(private http: HttpClient) {
  
   }
   createIdealLearnObj(idealLearnObj: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}`, idealLearnObj);
  }

  getIdealLearnObj(): Observable<any> {
    return this.http.get(`${this.baseUrl}`);
  }
}
