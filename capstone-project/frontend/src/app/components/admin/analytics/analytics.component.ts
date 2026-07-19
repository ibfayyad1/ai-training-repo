import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule, SidebarComponent],
  template: `
    <div class="layout">
      <app-sidebar></app-sidebar>
      <main class="main-content">
        <div class="page-header">
          <h1>AI Analytics</h1>
          <p>AI analyzes all incidents to detect patterns, trends, and provide recommendations.</p>
        </div>

        <div class="analytics-card">
          <button class="generate-btn" (click)="generate()" [disabled]="loading">
            <span *ngIf="!loading">&#9733; Generate AI Analysis</span>
            <span *ngIf="loading">&#9203; AI is analyzing patterns...</span>
          </button>

          <div class="result" *ngIf="analysis">
            <div class="result-header">
              <h3>AI Pattern Analysis</h3>
              <span class="meta">{{ incidentCount }} incidents analyzed | Technique: Context Window + Chain of Thought</span>
            </div>
            <div class="result-body">{{ analysis }}</div>
          </div>
        </div>
      </main>
    </div>
  `,
  styles: [`
    .layout { display: flex; }
    .main-content { margin-left: 260px; padding: 32px; width: calc(100% - 260px); min-height: 100vh; background: #f5f7fa; }
    .page-header h1 { font-size: 24px; color: #1b4f72; margin: 0; }
    .page-header p { color: #6c757d; font-size: 14px; margin-top: 4px; }
    .analytics-card { background: #fff; border-radius: 12px; padding: 32px; margin-top: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    .generate-btn { padding: 16px 32px; background: linear-gradient(135deg, #00b4d8, #2e86ab); color: #fff; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; }
    .generate-btn:disabled { opacity: 0.6; cursor: not-allowed; }
    .result { margin-top: 24px; }
    .result-header { margin-bottom: 16px; }
    .result-header h3 { font-size: 16px; color: #1b4f72; margin: 0; }
    .result-header .meta { font-size: 11px; color: #00b4d8; }
    .result-body { font-size: 14px; line-height: 1.7; color: #333; white-space: pre-wrap; background: #f8f9fa; padding: 24px; border-radius: 8px; border-left: 4px solid #00b4d8; }
  `]
})
export class AnalyticsComponent {
  analysis = '';
  incidentCount = 0;
  loading = false;

  constructor(private api: ApiService) {}

  generate() {
    this.loading = true;
    this.api.getAnalytics(30).subscribe({
      next: (res) => {
        this.analysis = res.analysis;
        this.incidentCount = res.incident_count;
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }
}
