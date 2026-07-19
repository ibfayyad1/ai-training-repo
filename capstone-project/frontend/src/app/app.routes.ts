import { Routes } from '@angular/router';

export const routes: Routes = [
  { path: '', redirectTo: '/login', pathMatch: 'full' },
  { path: 'login', loadComponent: () => import('./components/login/login.component').then(m => m.LoginComponent) },

  // Reporter routes
  { path: 'reporter/submit', loadComponent: () => import('./components/reporter/submit-report/submit-report.component').then(m => m.SubmitReportComponent) },
  { path: 'reporter/my-reports', loadComponent: () => import('./components/reporter/my-reports/my-reports.component').then(m => m.MyReportsComponent) },
  { path: 'reporter/report/:id', loadComponent: () => import('./components/reporter/view-report/view-report.component').then(m => m.ViewReportComponent) },

  // Admin routes
  { path: 'admin/dashboard', loadComponent: () => import('./components/admin/dashboard/dashboard.component').then(m => m.DashboardComponent) },
  { path: 'admin/ask-ai', loadComponent: () => import('./components/admin/ask-ai/ask-ai.component').then(m => m.AskAiComponent) },
  { path: 'admin/analytics', loadComponent: () => import('./components/admin/analytics/analytics.component').then(m => m.AnalyticsComponent) },
  { path: 'admin/monthly-report', loadComponent: () => import('./components/admin/monthly-report/monthly-report.component').then(m => m.MonthlyReportComponent) },
  { path: 'admin/report/:id', loadComponent: () => import('./components/reporter/view-report/view-report.component').then(m => m.ViewReportComponent) },
];
