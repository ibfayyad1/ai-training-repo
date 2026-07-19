import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-monthly-report',
  standalone: true,
  imports: [CommonModule, SidebarComponent],
  template: `
    <div class="layout">
      <app-sidebar></app-sidebar>
      <main class="main-content">
        <div class="page-header">
          <h1>Monthly Report</h1>
          <p>Generate a comprehensive monthly report with AI-powered analysis. Downloadable as PDF.</p>
        </div>

        <div class="report-card">
          <button class="generate-btn" (click)="generate()" [disabled]="loading">
            <span *ngIf="!loading">&#128196; Generate Monthly Report</span>
            <span *ngIf="loading">&#9203; AI is building your report...</span>
          </button>

          <div class="result" *ngIf="reportText">
            <div class="result-header">
              <h3>Monthly Report Generated</h3>
              <span class="meta">{{ incidentsAnalyzed }} incidents analyzed</span>
            </div>

            <!-- Stats summary -->
            <div class="stats-mini" *ngIf="stats">
              <div><strong>{{ stats.total }}</strong> Total</div>
              <div><strong>{{ stats.this_month }}</strong> This Month</div>
              <div><strong>{{ stats.this_week }}</strong> This Week</div>
            </div>

            <div class="result-body">{{ reportText }}</div>

            <button class="download-btn" *ngIf="pdfPath">&#128196; Download PDF</button>
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
    .report-card { background: #fff; border-radius: 12px; padding: 32px; margin-top: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    .generate-btn { padding: 16px 32px; background: linear-gradient(135deg, #e86a17, #c0392b); color: #fff; border: none; border-radius: 8px; font-size: 15px; font-weight: 600; cursor: pointer; }
    .generate-btn:disabled { opacity: 0.6; cursor: not-allowed; }
    .result { margin-top: 24px; }
    .result-header h3 { font-size: 16px; color: #1b4f72; margin: 0; }
    .result-header .meta { font-size: 11px; color: #6c757d; }
    .stats-mini { display: flex; gap: 24px; margin: 16px 0; padding: 16px; background: #f8f9fa; border-radius: 8px; }
    .stats-mini div { font-size: 13px; color: #333; }
    .stats-mini strong { font-size: 18px; color: #1b4f72; display: block; }
    .result-body { font-size: 14px; line-height: 1.7; color: #333; white-space: pre-wrap; background: #fff9f0; padding: 24px; border-radius: 8px; border-left: 4px solid #e86a17; margin-top: 16px; }
    .download-btn { margin-top: 16px; padding: 12px 24px; background: #28a745; color: #fff; border: none; border-radius: 6px; font-size: 14px; cursor: pointer; }
  `]
})
export class MonthlyReportComponent {
  reportText = '';
  pdfPath = '';
  stats: any = null;
  incidentsAnalyzed = 0;
  loading = false;

  constructor(private api: ApiService) {}

  generate() {
    this.loading = true;
    this.api.generateMonthlyReport().subscribe({
      next: (res) => {
        this.reportText = res.report_text;
        this.pdfPath = res.pdf_path;
        this.stats = res.stats;
        this.incidentsAnalyzed = res.incidents_analyzed;
        this.loading = false;
      },
      error: () => { this.loading = false; }
    });
  }
}
