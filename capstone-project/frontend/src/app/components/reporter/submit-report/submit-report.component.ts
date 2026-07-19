import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { ApiService } from '../../../services/api.service';
import { AuthService } from '../../../services/auth.service';

@Component({
  selector: 'app-submit-report',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent],
  template: `
    <div class="layout">
      <app-sidebar></app-sidebar>
      <main class="main-content">
        <div class="page-header">
          <h1>Submit Incident Report</h1>
          <p>Describe the incident and optionally attach a photo. AI will classify and generate a full report.</p>
        </div>

        <div class="form-card" *ngIf="!submitted">
          <div class="form-group">
            <label>Incident Description <span class="required">*</span></label>
            <textarea [(ngModel)]="description" rows="6"
              placeholder="Describe what happened: location, time, parties involved, injuries, etc."></textarea>
          </div>

          <div class="form-group">
            <label>Attach Photo (optional)</label>
            <div class="file-upload" (click)="fileInput.click()" [class.has-file]="selectedFile">
              <input #fileInput type="file" accept="image/*" (change)="onFileSelected($event)" hidden>
              <span *ngIf="!selectedFile">&#128247; Click to upload incident photo</span>
              <span *ngIf="selectedFile">&#9989; {{ selectedFile.name }}</span>
            </div>
          </div>

          <button class="submit-btn" (click)="submit()" [disabled]="loading || !description">
            <span *ngIf="!loading">&#9889; Submit & Process with AI</span>
            <span *ngIf="loading">&#9203; AI Agent is processing...</span>
          </button>
        </div>

        <!-- Result Card -->
        <div class="result-card" *ngIf="submitted && result">
          <div class="result-header success">
            <span>&#9989;</span>
            <h2>Report Submitted Successfully</h2>
          </div>

          <div class="result-body">
            <div class="result-meta">
              <div class="meta-item">
                <label>Report Number</label>
                <strong>{{ result.report_number }}</strong>
              </div>
              <div class="meta-item">
                <label>Category</label>
                <span class="badge badge-category">{{ result.classification?.category }}</span>
              </div>
              <div class="meta-item">
                <label>Severity</label>
                <span class="badge" [class]="'badge-' + result.classification?.severity">{{ result.classification?.severity }}</span>
              </div>
              <div class="meta-item">
                <label>AI Steps Taken</label>
                <strong>{{ result.agent_steps }}</strong>
              </div>
            </div>

            <div class="ai-message">
              <h3>&#9733; AI Agent Response</h3>
              <p>{{ result.message }}</p>
            </div>

            <div class="actions">
              <button class="btn-primary" (click)="reset()">Submit Another Report</button>
              <button class="btn-secondary" *ngIf="result.pdf_available">&#128196; Download PDF</button>
            </div>
          </div>
        </div>
      </main>
    </div>
  `,
  styles: [`
    .layout { display: flex; }
    .main-content {
      margin-left: 260px;
      padding: 32px;
      width: calc(100% - 260px);
      min-height: 100vh;
      background: #f5f7fa;
    }
    .page-header h1 { font-size: 24px; color: #1b4f72; margin: 0; }
    .page-header p { color: #6c757d; font-size: 14px; margin-top: 4px; }
    .form-card {
      background: #fff;
      border-radius: 12px;
      padding: 32px;
      margin-top: 24px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .form-group { margin-bottom: 20px; }
    .form-group label { display: block; font-size: 13px; font-weight: 600; color: #333; margin-bottom: 8px; }
    .required { color: #e74c3c; }
    textarea {
      width: 100%;
      padding: 14px;
      border: 1px solid #dee2e6;
      border-radius: 8px;
      font-size: 14px;
      resize: vertical;
      font-family: inherit;
      transition: border-color 0.2s;
    }
    textarea:focus { outline: none; border-color: #00b4d8; box-shadow: 0 0 0 3px rgba(0,180,216,0.1); }
    .file-upload {
      border: 2px dashed #dee2e6;
      border-radius: 8px;
      padding: 24px;
      text-align: center;
      cursor: pointer;
      color: #6c757d;
      transition: all 0.2s;
    }
    .file-upload:hover { border-color: #00b4d8; background: #f0f9ff; }
    .file-upload.has-file { border-color: #28a745; background: #f0fff4; color: #28a745; }
    .submit-btn {
      width: 100%;
      padding: 16px;
      background: linear-gradient(135deg, #00b4d8, #2e86ab);
      color: #fff;
      border: none;
      border-radius: 8px;
      font-size: 15px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.2s;
    }
    .submit-btn:hover { transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,180,216,0.3); }
    .submit-btn:disabled { opacity: 0.6; cursor: not-allowed; transform: none; }
    .result-card {
      background: #fff;
      border-radius: 12px;
      overflow: hidden;
      margin-top: 24px;
      box-shadow: 0 2px 8px rgba(0,0,0,0.06);
    }
    .result-header {
      padding: 20px 24px;
      display: flex;
      align-items: center;
      gap: 12px;
    }
    .result-header.success { background: #f0fff4; border-bottom: 1px solid #c3e6cb; }
    .result-header h2 { font-size: 18px; color: #155724; margin: 0; }
    .result-header span { font-size: 24px; }
    .result-body { padding: 24px; }
    .result-meta { display: grid; grid-template-columns: repeat(4, 1fr); gap: 16px; margin-bottom: 24px; }
    .meta-item { background: #f8f9fa; padding: 16px; border-radius: 8px; }
    .meta-item label { display: block; font-size: 11px; color: #6c757d; margin-bottom: 4px; }
    .meta-item strong { font-size: 16px; color: #1b4f72; }
    .badge { padding: 4px 10px; border-radius: 4px; font-size: 12px; font-weight: 600; text-transform: uppercase; }
    .badge-category { background: #e3f2fd; color: #1565c0; }
    .badge-low { background: #e8f5e9; color: #2e7d32; }
    .badge-medium { background: #fff3e0; color: #e65100; }
    .badge-high { background: #fbe9e7; color: #bf360c; }
    .badge-critical { background: #fce4ec; color: #b71c1c; }
    .ai-message { background: #f0f9ff; border-left: 4px solid #00b4d8; padding: 16px; border-radius: 0 8px 8px 0; margin-bottom: 20px; }
    .ai-message h3 { font-size: 14px; color: #1b4f72; margin: 0 0 8px; }
    .ai-message p { font-size: 13px; color: #333; margin: 0; line-height: 1.6; white-space: pre-wrap; }
    .actions { display: flex; gap: 12px; }
    .btn-primary { padding: 12px 24px; background: #00b4d8; color: #fff; border: none; border-radius: 6px; cursor: pointer; font-weight: 500; }
    .btn-secondary { padding: 12px 24px; background: #f8f9fa; color: #333; border: 1px solid #dee2e6; border-radius: 6px; cursor: pointer; font-weight: 500; }
  `]
})
export class SubmitReportComponent {
  description = '';
  selectedFile: File | null = null;
  loading = false;
  submitted = false;
  result: any = null;

  constructor(private api: ApiService, private auth: AuthService) {}

  onFileSelected(event: any) {
    this.selectedFile = event.target.files[0];
  }

  submit() {
    if (!this.description) return;
    this.loading = true;

    const formData = new FormData();
    formData.append('description', this.description);
    formData.append('reporter_username', this.auth.getUsername());
    if (this.selectedFile) {
      formData.append('image', this.selectedFile);
    }

    this.api.submitIncident(formData).subscribe({
      next: (res) => {
        this.result = res;
        this.submitted = true;
        this.loading = false;
      },
      error: (err) => {
        this.loading = false;
        alert('Error submitting report: ' + (err.error?.error || 'Unknown error'));
      }
    });
  }

  reset() {
    this.description = '';
    this.selectedFile = null;
    this.submitted = false;
    this.result = null;
  }
}
