import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { AuthService } from '../../services/auth.service';

@Component({
  selector: 'app-login',
  standalone: true,
  imports: [CommonModule],
  template: `
    <div class="login-container">
      <div class="login-card">
        <div class="login-header">
          <span class="login-icon">&#9888;</span>
          <h1>Incident Report System</h1>
          <p>AI-Powered • Secure • Intelligent</p>
        </div>

        <div class="login-body">
          <h2>Select Your Role</h2>

          <button class="role-btn reporter-btn" (click)="loginAs('reporter1', 'reporter')">
            <div class="role-icon">&#128100;</div>
            <div class="role-info">
              <strong>Reporter</strong>
              <span>Submit and track incident reports</span>
            </div>
          </button>

          <button class="role-btn admin-btn" (click)="loginAs('admin', 'admin')">
            <div class="role-icon">&#128736;</div>
            <div class="role-info">
              <strong>Admin</strong>
              <span>Dashboard, AI Analytics, Reports</span>
            </div>
          </button>
        </div>

        <div class="login-footer">
          <p>Training Demo - No authentication required</p>
        </div>
      </div>
    </div>
  `,
  styles: [`
    .login-container {
      min-height: 100vh;
      display: flex;
      align-items: center;
      justify-content: center;
      background: linear-gradient(135deg, #0d1b2a 0%, #1b4f72 100%);
    }
    .login-card {
      background: #fff;
      border-radius: 16px;
      width: 400px;
      overflow: hidden;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .login-header {
      background: #0d1b2a;
      padding: 32px;
      text-align: center;
      color: #fff;
    }
    .login-icon {
      font-size: 40px;
      display: block;
      margin-bottom: 12px;
    }
    .login-header h1 {
      font-size: 20px;
      margin: 0;
      font-weight: 600;
    }
    .login-header p {
      font-size: 12px;
      color: #00b4d8;
      margin-top: 6px;
    }
    .login-body {
      padding: 32px;
    }
    .login-body h2 {
      font-size: 16px;
      color: #333;
      margin-bottom: 20px;
      text-align: center;
    }
    .role-btn {
      display: flex;
      align-items: center;
      gap: 16px;
      width: 100%;
      padding: 16px 20px;
      border: 2px solid #e9ecef;
      border-radius: 10px;
      background: #fff;
      cursor: pointer;
      transition: all 0.2s;
      margin-bottom: 12px;
      text-align: left;
    }
    .role-btn:hover {
      border-color: #00b4d8;
      background: #f0f9ff;
      transform: translateY(-2px);
      box-shadow: 0 4px 12px rgba(0,180,216,0.15);
    }
    .role-icon {
      font-size: 28px;
      width: 48px;
      height: 48px;
      background: #f0f4f8;
      border-radius: 10px;
      display: flex;
      align-items: center;
      justify-content: center;
    }
    .role-info strong {
      display: block;
      font-size: 15px;
      color: #1b4f72;
    }
    .role-info span {
      font-size: 12px;
      color: #6c757d;
    }
    .login-footer {
      padding: 16px;
      text-align: center;
      background: #f8f9fa;
      border-top: 1px solid #e9ecef;
    }
    .login-footer p {
      font-size: 11px;
      color: #999;
      margin: 0;
    }
  `]
})
export class LoginComponent {
  constructor(private auth: AuthService, private router: Router) {}

  loginAs(username: string, role: string) {
    this.auth.login(username, role);
    if (role === 'admin') {
      this.router.navigate(['/admin/dashboard']);
    } else {
      this.router.navigate(['/reporter/submit']);
    }
  }
}
