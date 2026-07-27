const API_BASE = '/api/v1';

async function request<T>(method: string, path: string, body?: unknown): Promise<T> {
  const opts: RequestInit = {
    method,
    headers: body ? { 'Content-Type': 'application/json' } : undefined,
    body: body ? JSON.stringify(body) : undefined,
  };
  const res = await fetch(`${API_BASE}${path}`, opts);
  if (!res.ok) {
    const err = await res.json().catch(() => ({ detail: 'Request failed' }));
    throw new Error(err.detail || err.message || 'Request failed');
  }
  return res.json();
}

export interface UploadResult {
  valid: boolean;
  uploadId: string | null;
  sessionId: string;
  projectName?: string;
  prompt?: string;
  errors?: Array<{ line?: number; message: string }>;
}

export interface AiGenerateResult {
  success: boolean;
  test_code?: string;
  error?: string;
}

export interface TestResult {
  success: boolean;
  passed: number;
  failed: number;
  stdout: string;
  stderr: string;
  exit_code: number;
}

export interface EvaluationResult {
  evaluation_id: string;
  coverage: number;
  mutation_score: number;
  failure_detection: number;
  all_passed: boolean;
  details: Record<string, unknown>;
}

export async function uploadSource(formData: FormData): Promise<UploadResult> {
  const res = await fetch(`${API_BASE}/upload/source`, { method: 'POST', body: formData });
  const data = await res.json();
  if (!res.ok) throw data;
  return data;
}

export async function generateTests(sessionId: string, prompt: string, code: string): Promise<AiGenerateResult> {
  return request<AiGenerateResult>('POST', '/ai/generate-tests', { session_id: sessionId, prompt, code });
}

export async function regenerateTests(sessionId: string, prompt: string, code: string): Promise<AiGenerateResult> {
  return request<AiGenerateResult>('POST', '/ai/regenerate-tests', { session_id: sessionId, prompt, code });
}

export async function executeTests(sourceCode: string, testCode: string): Promise<TestResult> {
  return request<TestResult>('POST', '/tests/execute', { session_id: '', source_code: sourceCode, test_code: testCode });
}

export async function runEvaluation(sourcePath: string, testCode: string): Promise<EvaluationResult> {
  return request<EvaluationResult>('POST', '/evaluation/run', { source_path: sourcePath, test_code: testCode });
}

export async function getEvaluation(evaluationId: string): Promise<EvaluationResult> {
  return request<EvaluationResult>('GET', `/evaluation/${evaluationId}`);
}

export async function generateReport(evaluationResults: Record<string, unknown>, testCode: string): Promise<{ report_id: string; status: string }> {
  return request('POST', '/reports/generate', { evaluation_results: evaluationResults, test_code: testCode });
}

export function getReportDownloadUrl(reportId: string): string {
  return `${API_BASE}/reports/${reportId}/download`;
}
