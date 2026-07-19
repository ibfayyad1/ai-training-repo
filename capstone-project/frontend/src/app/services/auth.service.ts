import { Injectable } from '@angular/core';

@Injectable({ providedIn: 'root' })
export class AuthService {
  private currentUser: { username: string; role: string } | null = null;

  login(username: string, role: string): void {
    this.currentUser = { username, role };
    localStorage.setItem('user', JSON.stringify(this.currentUser));
  }

  logout(): void {
    this.currentUser = null;
    localStorage.removeItem('user');
  }

  getUser(): { username: string; role: string } | null {
    if (!this.currentUser) {
      const stored = localStorage.getItem('user');
      if (stored) this.currentUser = JSON.parse(stored);
    }
    return this.currentUser;
  }

  isLoggedIn(): boolean {
    return this.getUser() !== null;
  }

  isAdmin(): boolean {
    return this.getUser()?.role === 'admin';
  }

  getUsername(): string {
    return this.getUser()?.username || '';
  }
}
