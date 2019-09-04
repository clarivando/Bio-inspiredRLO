import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CrloService { 

private baseUrl = 'http://localhost:8000/recommend2';
//private baseUrl1 = 'http://localhost:8000/recommend';

constructor(private http: HttpClient) { }

/*getCrloAluno(id: number): Observable<Object> {
  return this.http.get(`${this.baseUrl1}/${id}/`);
}*/

/*getCrloLO(id: number): Observable<Object> {
  return this.http.get(`${this.baseUrl1}/${id}/`);
}*/
retrieve(crlo: Object): Observable<any> {
  return this.http.post(`${this.baseUrl}`, crlo);
}
}
