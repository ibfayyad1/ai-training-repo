import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { ApiService } from '../../../services/api.service';
import { AuthService } from '../../../services/auth.service';
import { Incident } from '../../../models/incident.model';

@Component({
  selector: 'app-my-reports',
  standalone: true,
  imports: [CommonModule, RouterModule, SidebarComponent],
  template: `
    <div class="layout">
      <app-sidebar></app-sidebar>
      <main class="main-content">
        <div class="page-header">
          <h1>My Reports</h1>
          <p>Track the status of your submitted incident reports.</p>
        </div>

        <div class="table-card">
          <table>
            <thead>
              <tr>
                <th>Report #</th>
                <th>Category</th>
                <th>Severity</th>
                <th>Location</th>
                <th>Status</th>
                <th>Date</th>
                <th>Action</th>
              </tr>
            </thead>
            <tbody>
              <tr *ngFor="let incident of incidents">
                <td><strong>{{ incident.report_number }}</strong></td>
                <td><span class="badge badge-category">{{ incident.category }}</span></td>
                <td><span class="badge" [class]="'badge-' + incident.severity">{{ incident.severity }}</span></td>
                <td>{{ incident.location || 'N/A' }}</td>
                <td><span class="status" [class]="'status-' + incident.status">{{ incident.status }}</span></td>
                <td>{{ incident.created_at | date:'short' }}</td>
                <td>
                  <a [routerLink]="['/reporter/report', incident.id]" class="view-btn">View</a>
                </td>
              </tr>
              <tr *ngIf="incidents.length === 0">
                <td colspan="7" class="empty">No reports yet. Submit your first incident report.</td>
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
    .table-card { background: #fff; border-radius: 12px; padding: 0; margin-top: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); overflow: hidden; }
    table { width: 100%; border-collapse: collapse; }
    th { background: #f8f9fa; padding: 14px 16px; text-align: left; font-size: 12px; color: #6c757d; font-weight: 600; text-transform: uppercase; letter-spacing: 0.5px; }
    td { padding: 14px 16px; border-top: 1px solid #f0f0f0; font-size: 13px; color: #333; }
    tr:hover td { background: #f9fbfd; }
    .badge { padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
    .badge-category { background: #e3f2fd; color: #1565c0; }
    .badge-low { background: #e8f5e9; color: #2e7d32; }
    .badge-medium { background: #fff3e0; color: #e65100; }
    .badge-high { background: #fbe9e7; color: #bf360c; }
    .badge-critical { background: #fce4ec; color: #b71c1c; }
    .status { padding: 3px 8px; border-radius: 4px; font-size: 11px; font-weight: 600; }
    .status-open { background: #e3f2fd; color: #1565c0; }
    .status-reviewing { background: #fff3e0; color: #e65100; }
    .status-resolved { background: #e8f5e9; color: #2e7d32; }
    .status-closed { background: #f5f5f5; color: #757575; }
    .view-btn { color: #00b4d8; text-decoration: none; font-weight: 500; font-size: 12px; }
    .view-btn:hover { text-decoration: underline; }
    .empty { text-align: center; color: #999; padding: 40px !important; }
  `]
})
export class MyReportsComponent implements OnInit {
  incidents: Incident[] = [];

  constructor(private api: ApiService, private auth: AuthService) {}

  ngOnInit() {
    this.api.getIncidents({ reporter_username: this.auth.getUsername() }).subscribe(res => {
      this.incidents = res.incidents;
    });
  }
}
