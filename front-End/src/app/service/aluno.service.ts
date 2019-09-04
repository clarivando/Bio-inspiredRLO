import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class AlunoService {

  private baseUrl = 'http://localhost:8000/alunos';

  constructor(private http: HttpClient) { }

  getAluno(id: number): Observable<Object> {
    return this.http.get(`${this.baseUrl}/${id}`);
  }

  createAluno(aluno: Object): Observable<Object> {
    return this.http.post(`${this.baseUrl}`, aluno);
  }

  updateAluno(id: number, value: any): Observable<Object> {
    return this.http.put(`${this.baseUrl}/${id}`, value);
  }

  deleteAluno(id: number): Observable<any> {
    return this.http.delete(`${this.baseUrl}/${id}`, { responseType: 'text' });
  }

  getAlunosList(): Observable<any> {
    return this.http.get(`${this.baseUrl}`);
  }
}
