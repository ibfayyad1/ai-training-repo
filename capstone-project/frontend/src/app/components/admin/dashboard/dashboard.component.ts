import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { ApiService } from '../../../services/api.service';
import { Incident, Stats } from '../../../models/incident.model';

@Component({
  selector: 'app-dashboard',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule, SidebarComponent],
  template: `
    <div class="layout">
      <app-sidebar></app-sidebar>
      <main class="main-content">
        <div class="page-header">
          <h1>Dashboard</h1>
          <p>Overview of all incident reports and system statistics.</p>
        </div>

        <!-- Stats Cards -->
        <div class="stats-grid" *ngIf="stats">
          <div class="stat-card">
            <div class="stat-number">{{ stats.total }}</div>
            <div class="stat-label">Total Incidents</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.this_week }}</div>
            <div class="stat-label">This Week</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.this_month }}</div>
            <div class="stat-label">This Month</div>
          </div>
          <div class="stat-card">
            <div class="stat-number">{{ stats.by_status?.open || 0 }}</div>
            <div class="stat-label">Open Cases</div>
          </div>
        </div>

        <!-- Filters -->
        <div class="filters">
          <select [(ngModel)]="filterCategory" (change)="loadIncidents()">
            <option value="">All Categories</option>
            <option value="Traffic">Traffic</option>
            <option value="Fire">Fire</option>
            <option value="Theft">Theft</option>
            <option value="Public Safety">Public Safety</option>
            <option value="Environmental">Environmental</option>
          </select>
          <select [(ngModel)]="filterSeverity" (change)="loadIncidents()">
            <option value="">All Severities</option>
            <option value="low">Low</option>
            <option value="medium">Medium</option>
            <option value="high">High</option>
            <option value="critical">Critical</option>
          </select>
          <select [(ngModel)]="filterStatus" (change)="loadIncidents()">
            <option value="">All Status</option>
            <option value="open">Open</option>
            <option value="reviewing">Reviewing</option>
            <option value="resolved">Resolved</option>
            <option value="closed">Closed</option>
          </select>
        </div>

        <!-- Incidents Table -->
        <div class="table-card">
          <table>
            <thead>
              <tr>
                <th>Report #</th>
                <th>Reporter</th>
                <th>Category</th>
                <th>Severity</th>
                <th>Location</th>
                <th>Status</th>
                <th>Date</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let inc of incidents">
                <td><strong>{{ inc.report_number }}</strong></td>
                <td>{{ inc.reporter_username }}</td>
                <td><span class="badge badge-category">{{ inc.category }}</span></td>
                <td><span class="badge" [class]="'badge-' + inc.severity">{{ inc.severity }}</span></td>
                <td>{{ inc.location || 'N/A' }}</td>
                <td>
                  <select class="status-select" [value]="inc.status" (change)="updateStatus(inc.id, $event)">
                    <option value="open">Open</option>
                    <option value="reviewing">Reviewing</option>
                    <option value="resolved">Resolved</option>
                    <option value="closed">Closed</option>
                  </select>
                </td>
                <td>{{ inc.created_at?.substring(0, 10) }}</td>
                <td>
                  <a [routerLink]="['/admin/report', inc.id]" class="view-btn">View</a>
                </td>
              </tr>
              <tr *ngIf="incidents.length === 0">
                <td colspan="8" class="empty">No incidents found.</td>
              </tr>
            </tbody>
          </table>
        </div>
      </main>
    </div>
  `,
  styles: [`
    .layout { display: flex; }
    .main-content { margin-left: 260px; padding: 32px; width: calc(100% - 260px); min-height: 100vh; background: #f5f7fa; }
    .page-header h1 { font-size: 24px; color: #1b4f72; margin: 0; }
    .page-header p { color: #6c757d; font-size: 14px; margin-top: 4px; }
    .stats-grid { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin: 24px 0; }
    .stat-card { background: #fff; border-radius: 12px; padding: 24px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    .stat-number { font-size: 32px; font-weight: 700; color: #1b4f72; }
    .stat-label { font-size: 12px; color: #6c757d; margin-top: 4px; }
    .filters { display: flex; gap: 12px; margin-bottom: 16px; }
    .filters select { padding: 10px 14px; border: 1px solid #dee2e6; border-radius: 6px; font-size: 13px; background: #fff; }
    .table-card { background: #fff; border-radius: 12px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.06); }
    table { width: 100%; border-collapse: collapse; }
    th { background: #f8f9fa; padding: 14px 16px; text-align: left; font-size: 11px; color: #6c757d; font-weight: 600; text-transform: uppercase; }
    td { padding: 12px 16px; border-top: 1px solid #f0f0f0; font-size: 13px; }
    .badge { padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
    .badge-category { background: #e3f2fd; color: #1565c0; }
    .badge-low { background: #e8f5e9; color: #2e7d32; }
    .badge-medium { background: #fff3e0; color: #e65100; }
    .badge-high { background: #fbe9e7; color: #bf360c; }
    .badge-critical { background: #fce4ec; color: #b71c1c; }
    .status-select { padding: 4px 8px; border: 1px solid #dee2e6; border-radius: 4px; font-size: 12px; }
    .view-btn { color: #00b4d8; text-decoration: none; font-weight: 500; font-size: 12px; }
    .empty { text-align: center; color: #999; padding: 40px !important; }
  `]
})
export class DashboardComponent implements OnInit {
  incidents: Incident[] = [];
  stats: Stats | null = null;
  filterCategory = '';
  filterSeverity = '';
  filterStatus = '';

  constructor(private api: ApiService) {}

  ngOnInit() {
    this.loadIncidents();
    this.api.getStats().subscribe(res => this.stats = res);
  }

  loadIncidents() {
    const filters: any = {};
    if (this.filterCategory) filters.category = this.filterCategory;
    if (this.filterSeverity) filters.severity = this.filterSeverity;
    if (this.filterStatus) filters.status = this.filterStatus;
    this.api.getIncidents(filters).subscribe(res => this.incidents = res.incidents);
  }

  updateStatus(id: number, event: any) {
    this.api.updateStatus(id, event.target.value).subscribe();
  }
}
