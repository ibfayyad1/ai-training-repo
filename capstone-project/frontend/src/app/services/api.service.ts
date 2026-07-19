import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Incident, Stats, User, AskAIResponse } from '../models/incident.model';

@Injectable({ providedIn: 'root' })
export class ApiService {
  private baseUrl = 'http://localhost:5000/api';

  constructor(private http: HttpClient) {}

  // ---- INCIDENTS ----

  submitIncident(formData: FormData): Observable<any> {
    return this.http.post(`${this.baseUrl}/incidents`, formData);
  }

  getIncidents(filters?: any): Observable<{ count: number; incidents: Incident[] }> {
    let params = '';
    if (filters) {
      const queryParts = Object.entries(filters)
        .filter(([_, v]) => v)
        .map(([k, v]) => `${k}=${v}`);
      if (queryParts.length) params = '?' + queryParts.join('&');
    }
    return this.http.get<{ count: number; incidents: Incident[] }>(`${this.baseUrl}/incidents${params}`);
  }

  getIncident(id: number): Observable<Incident> {
    return this.http.get<Incident>(`${this.baseUrl}/incidents/${id}`);
  }

  updateStatus(id: number, status: string): Observable<any> {
    return this.http.put(`${this.baseUrl}/incidents/${id}`, { status });
  }

  // ---- AI ----

  askAI(question: string): Observable<AskAIResponse> {
    return this.http.post<AskAIResponse>(`${this.baseUrl}/ai/ask`, { question });
  }

  getAnalytics(days?: number): Observable<any> {
    return this.http.post(`${this.baseUrl}/ai/analytics`, { days: days || 30 });
  }

  generateMonthlyReport(month?: string): Observable<any> {
    return this.http.post(`${this.baseUrl}/ai/monthly`, { month });
  }

  // ---- STATS ----

  getStats(): Observable<Stats> {
    return this.http.get<Stats>(`${this.baseUrl}/stats`);
  }

  downloadPdf(incidentId: number): Observable<Blob> {
    return this.http.get(`${this.baseUrl}/pdf/${incidentId}`, { responseType: 'blob' });
  }

  // ---- USERS ----

  getUsers(): Observable<User[]> {
    return this.http.get<User[]>(`${this.baseUrl}/users`);
  }
}
