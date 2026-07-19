import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { ApiService } from '../../../services/api.service';
import { Incident } from '../../../models/incident.model';

@Component({
  selector: 'app-view-report',
  standalone: true,
  imports: [CommonModule, SidebarComponent],
  template: `
    <div class="layout">
      <app-sidebar></app-sidebar>
      <main class="main-content" *ngIf="incident">
        <div class="page-header">
          <h1>Report {{ incident.report_number }}</h1>
          <span class="badge" [class]="'badge-' + incident.severity">{{ incident.severity }}</span>
          <span class="status" [class]="'status-' + incident.status">{{ incident.status }}</span>
        </div>

        <div class="report-grid">
          <!-- Classification Card -->
          <div class="card classification-card">
            <h3>AI Classification</h3>
            <div class="meta-grid">
              <div><label>Category</label><strong>{{ incident.category }}</strong></div>
              <div><label>Severity</label><strong>{{ incident.severity }}</strong></div>
              <div><label>Location</label><strong>{{ incident.location || 'N/A' }}</strong></div>
              <div><label>Confidence</label><strong>{{ incident.confidence }}%</strong></div>
            </div>
          </div>

          <!-- Original Description -->
          <div class="card">
            <h3>Original Report</h3>
            <p class="description">{{ incident.description }}</p>
          </div>

          <!-- Image Analysis -->
          <div class="card" *ngIf="incident.image_analysis">
            <h3>&#128247; AI Image Analysis</h3>
            <p class="analysis">{{ incident.image_analysis }}</p>
          </div>

          <!-- AI Generated Report -->
          <div class="card full-width" *ngIf="incident.ai_report">
            <h3>&#9733; AI-Generated Report</h3>
            <div class="ai-report">{{ incident.ai_report }}</div>
          </div>

          <!-- Actions -->
          <div class="card full-width actions-card">
            <button class="btn-primary" (click)="downloadPdf()">&#128196; Download PDF Report</button>
          </div>
        </div>
      </main>
    </div>
  `,
  styles: [`
    .layout { display: flex; }
    .main-content { margin-left: 260px; padding: 32px; width: calc(100% - 260px); min-height: 100vh; background: #f5f7fa; }
    .page-header { display: flex; align-items: center; gap: 12px; margin-bottom: 24px; }
    .page-header h1 { font-size: 24px; color: #1b4f72; margin: 0; }
    .report-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
    .card { background: #fff; border-radius: 12px; padding: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    .card h3 { font-size: 14px; color: #1b4f72; margin: 0 0 16px; }
    .full-width { grid-column: 1 / -1; }
    .meta-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
    .meta-grid label { display: block; font-size: 11px; color: #6c757d; }
    .meta-grid strong { font-size: 15px; color: #333; }
    .description { font-size: 14px; color: #333; line-height: 1.6; }
    .analysis { font-size: 13px; color: #555; line-height: 1.6; background: #f8f9fa; padding: 16px; border-radius: 8px; }
    .ai-report { font-size: 13px; color: #333; line-height: 1.7; white-space: pre-wrap; background: #f0f9ff; padding: 20px; border-radius: 8px; border-left: 4px solid #00b4d8; }
    .badge { padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; text-transform: uppercase; }
    .badge-low { background: #e8f5e9; color: #2e7d32; }
    .badge-medium { background: #fff3e0; color: #e65100; }
    .badge-high { background: #fbe9e7; color: #bf360c; }
    .badge-critical { background: #fce4ec; color: #b71c1c; }
    .status { padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; }
    .status-open { background: #e3f2fd; color: #1565c0; }
    .status-reviewing { background: #fff3e0; color: #e65100; }
    .status-resolved { background: #e8f5e9; color: #2e7d32; }
    .actions-card { display: flex; gap: 12px; }
    .btn-primary { padding: 12px 24px; background: #00b4d8; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; font-size: 14px; }
    .btn-primary:hover { background: #0096b7; }
  `]
})
export class ViewReportComponent implements OnInit {
  incident: Incident | null = null;

  constructor(private api: ApiService, private route: ActivatedRoute) {}

  ngOnInit() {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    this.api.getIncident(id).subscribe(res => this.incident = res);
  }

  downloadPdf() {
    if (!this.incident) return;
    this.api.downloadPdf(this.incident.id).subscribe(blob => {
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `report_${this.incident!.report_number}.pdf`;
      a.click();
    });
  }
}
