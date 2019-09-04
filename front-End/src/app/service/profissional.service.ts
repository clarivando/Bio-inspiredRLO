import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ProfissionalService {

  private baseUrl = 'http://localhost:8080/api/aluno';

  constructor(private http: HttpClient) { }

  getProfissional(id: number): Observable<Object> {
    return this.http.get(`${this.baseUrl}/${id}`);
  }

  createProfissional(profissional: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}`, profissional);
  }

  updateProfissional(id: number, value: any): Observable<Object> {
    return this.http.put(`${this.baseUrl}/${id}`, value);
  }

  deleteProfissional(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`, { responseType: 'text' });
  }

  getProfissionaisList(): Observable<any> {
    return this.http.get(`${this.baseUrl}`);
  }
}
