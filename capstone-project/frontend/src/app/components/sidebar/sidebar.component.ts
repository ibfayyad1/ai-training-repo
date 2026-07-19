import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-sidebar',
  standalone: true,
  imports: [CommonModule, RouterModule],
  template: `
    <aside class="sidebar">
      <div class="sidebar-header">
        <div class="logo">
          <span class="logo-icon">&#9888;</span>
          <span class="logo-text">IRS</span>
        </div>
        <p class="logo-subtitle">Incident Report System</p>
      </div>

      <nav class="sidebar-nav">
        <!-- Reporter Navigation -->
        <div *ngIf="!auth.isAdmin()" class="nav-section">
          <p class="nav-label">REPORTER</p>
          <a routerLink="/reporter/submit" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">&#10010;</span>
            <span>Submit Report</span>
          </a>
          <a routerLink="/reporter/my-reports" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">&#9776;</span>
            <span>My Reports</span>
          </a>
        </div>

        <!-- Admin Navigation -->
        <div *ngIf="auth.isAdmin()" class="nav-section">
          <p class="nav-label">ADMIN</p>
          <a routerLink="/admin/dashboard" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">&#9632;</span>
            <span>Dashboard</span>
          </a>
          <a routerLink="/admin/ask-ai" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">&#9733;</span>
            <span>Ask AI</span>
          </a>
          <a routerLink="/admin/analytics" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">&#9650;</span>
            <span>AI Analytics</span>
          </a>
          <a routerLink="/admin/monthly-report" routerLinkActive="active" class="nav-item">
            <span class="nav-icon">&#9998;</span>
            <span>Monthly Report</span>
          </a>
        </div>
      </nav>

      <div class="sidebar-footer">
        <div class="user-info">
          <div class="user-avatar">{{ auth.getUsername().charAt(0).toUpperCase() }}</div>
          <div class="user-details">
            <p class="user-name">{{ auth.getUsername() }}</p>
            <p class="user-role">{{ auth.isAdmin() ? 'Admin' : 'Reporter' }}</p>
          </div>
        </div>
        <button class="logout-btn" (click)="logout()">Logout</button>
      </div>
    </aside>
  `,
  styles: [`
    .sidebar {
      width: 260px;
      height: 100vh;
      background: #0d1b2a;
      display: flex;
      flex-direction: column;
      position: fixed;
      left: 0;
      top: 0;
      z-index: 100;
    }
    .sidebar-header {
      padding: 24px 20px 16px;
      border-bottom: 1px solid #1b3a5c;
    }
    .logo {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .logo-icon {
      font-size: 28px;
      color: #00b4d8;
    }
    .logo-text {
      font-size: 22px;
      font-weight: 700;
      color: #fff;
      letter-spacing: 1px;
    }
    .logo-subtitle {
      font-size: 11px;
      color: #6c8fa7;
      margin-top: 4px;
    }
    .sidebar-nav {
      flex: 1;
      padding: 16px 0;
      overflow-y: auto;
    }
    .nav-section {
      margin-bottom: 20px;
    }
    .nav-label {
      font-size: 10px;
      color: #4a6a80;
      letter-spacing: 1.5px;
      padding: 0 20px;
      margin-bottom: 8px;
      font-weight: 600;
    }
    .nav-item {
      display: flex;
      align-items: center;
      gap: 12px;
      padding: 12px 20px;
      color: #a0b4c4;
      text-decoration: none;
      font-size: 14px;
      transition: all 0.2s;
      border-left: 3px solid transparent;
    }
    .nav-item:hover {
      background: #132d46;
      color: #fff;
    }
    .nav-item.active {
      background: #132d46;
      color: #00b4d8;
      border-left-color: #00b4d8;
    }
    .nav-icon {
      font-size: 16px;
      width: 20px;
      text-align: center;
    }
    .sidebar-footer {
      padding: 16px 20px;
      border-top: 1px solid #1b3a5c;
    }
    .user-info {
      display: flex;
      align-items: center;
      gap: 10px;
      margin-bottom: 12px;
    }
    .user-avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      background: #2e86ab;
      color: #fff;
      display: flex;
      align-items: center;
      justify-content: center;
      font-weight: 600;
      font-size: 14px;
    }
    .user-name {
      color: #fff;
      font-size: 13px;
      font-weight: 500;
    }
    .user-role {
      color: #6c8fa7;
      font-size: 11px;
    }
    .logout-btn {
      width: 100%;
      padding: 8px;
      background: transparent;
      border: 1px solid #2d4a5c;
      color: #a0b4c4;
      border-radius: 6px;
      cursor: pointer;
      font-size: 12px;
      transition: all 0.2s;
    }
    .logout-btn:hover {
      background: #1b3a5c;
      color: #fff;
    }
  `]
})
export class SidebarComponent {
  constructor(public auth: AuthService) {}

  logout() {
    this.auth.logout();
    window.location.href = '/login';
  }
}
