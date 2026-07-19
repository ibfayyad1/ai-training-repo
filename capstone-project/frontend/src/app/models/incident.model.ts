export interface Incident {
  id: number;
  report_number: string;
  reporter_username: string;
  description: string;
  category: string;
  severity: string;
  location: string;
  timestamp_extracted: string;
  image_path: string | null;
  image_analysis: string | null;
  ai_report: string | null;
  ai_reasoning: string | null;
  confidence: number;
  status: 'open' | 'reviewing' | 'resolved' | 'closed';
  pdf_path: string | null;
  created_at: string;
  updated_at: string;
}

export interface Stats {
  total: number;
  by_category: { [key: string]: number };
  by_severity: { [key: string]: number };
  by_status: { [key: string]: number };
  this_week: number;
  this_month: number;
}

export interface User {
  username: string;
  role: 'reporter' | 'admin';
}

export interface AskAIResponse {
  question: string;
  answer: string;
  sources: string[];
  documents_searched: number;
}
