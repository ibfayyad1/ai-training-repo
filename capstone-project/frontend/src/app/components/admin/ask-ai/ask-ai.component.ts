import { Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SidebarComponent } from '../../sidebar/sidebar.component';
import { ApiService } from '../../../services/api.service';

@Component({
  selector: 'app-ask-ai',
  standalone: true,
  imports: [CommonModule, FormsModule, SidebarComponent],
  template: `
    <div class="layout">
      <app-sidebar></app-sidebar>
      <main class="main-content">
        <div class="page-header">
          <h1>Ask AI</h1>
          <p>Ask any question about your incidents. AI answers from REAL data using RAG (Module 03).</p>
        </div>

        <div class="chat-container">
          <!-- Messages -->
          <div class="messages">
            <div *ngFor="let msg of messages" class="message" [class.user-msg]="msg.role === 'user'" [class.ai-msg]="msg.role === 'ai'">
              <div class="msg-avatar">{{ msg.role === 'user' ? 'You' : 'AI' }}</div>
              <div class="msg-content">
                <p>{{ msg.text }}</p>
                <div class="msg-sources" *ngIf="msg.sources && msg.sources.length">
                  <strong>Sources:</strong> {{ msg.sources.join(', ') }}
                </div>
                <div class="msg-technique" *ngIf="msg.technique">
                  <em>{{ msg.technique }}</em>
                </div>
              </div>
            </div>
            <div *ngIf="loading" class="message ai-msg">
              <div class="msg-avatar">AI</div>
              <div class="msg-content"><p>Searching incident database...</p></div>
            </div>
          </div>

          <!-- Input -->
          <div class="chat-input">
            <input [(ngModel)]="question" (keyup.enter)="ask()"
              placeholder="Ask anything: 'How many fires this week?', 'Busiest area?', etc."
              [disabled]="loading">
            <button (click)="ask()" [disabled]="loading || !question">Ask</button>
          </div>

          <!-- Example Questions -->
          <div class="examples" *ngIf="messages.length === 0">
            <p>Try asking:</p>
            <button *ngFor="let ex of examples" (click)="question = ex; ask()">{{ ex }}</button>
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
    .chat-container { background: #fff; border-radius: 12px; margin-top: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.06); overflow: hidden; }
    .messages { padding: 24px; min-height: 400px; max-height: 500px; overflow-y: auto; }
    .message { display: flex; gap: 12px; margin-bottom: 20px; }
    .msg-avatar { width: 36px; height: 36px; border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 11px; font-weight: 600; flex-shrink: 0; }
    .user-msg .msg-avatar { background: #e3f2fd; color: #1565c0; }
    .ai-msg .msg-avatar { background: #e0f7fa; color: #00838f; }
    .msg-content { flex: 1; }
    .msg-content p { margin: 0; font-size: 14px; line-height: 1.6; color: #333; white-space: pre-wrap; }
    .user-msg .msg-content p { font-weight: 500; }
    .ai-msg .msg-content { background: #f8f9fa; padding: 16px; border-radius: 0 12px 12px 12px; }
    .msg-sources { margin-top: 8px; font-size: 11px; color: #6c757d; }
    .msg-technique { margin-top: 4px; font-size: 10px; color: #00b4d8; }
    .chat-input { display: flex; gap: 8px; padding: 16px 24px; border-top: 1px solid #f0f0f0; background: #fafafa; }
    .chat-input input { flex: 1; padding: 14px; border: 1px solid #dee2e6; border-radius: 8px; font-size: 14px; }
    .chat-input input:focus { outline: none; border-color: #00b4d8; }
    .chat-input button { padding: 14px 28px; background: #00b4d8; color: #fff; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; }
    .chat-input button:disabled { opacity: 0.5; }
    .examples { padding: 16px 24px; border-top: 1px solid #f0f0f0; }
    .examples p { font-size: 12px; color: #6c757d; margin: 0 0 8px; }
    .examples button { padding: 8px 14px; border: 1px solid #dee2e6; border-radius: 20px; background: #fff; font-size: 12px; cursor: pointer; margin-right: 8px; margin-bottom: 8px; }
    .examples button:hover { border-color: #00b4d8; color: #00b4d8; }
  `]
})
export class AskAiComponent {
  question = '';
  messages: { role: string; text: string; sources?: string[]; technique?: string }[] = [];
  loading = false;
  examples = [
    'How many traffic accidents this week?',
    'What is the most common incident type?',
    'Any high severity incidents recently?',
    'Compare different areas by incident count'
  ];

  constructor(private api: ApiService) {}

  ask() {
    if (!this.question || this.loading) return;
    const q = this.question;
    this.messages.push({ role: 'user', text: q });
    this.question = '';
    this.loading = true;

    this.api.askAI(q).subscribe({
      next: (res) => {
        this.messages.push({
          role: 'ai',
          text: res.answer,
          sources: res.sources,
          technique: `RAG: ${res.documents_searched} documents searched`
        });
        this.loading = false;
      },
      error: () => {
        this.messages.push({ role: 'ai', text: 'Error: Could not process your question.' });
        this.loading = false;
      }
    });
  }
}
