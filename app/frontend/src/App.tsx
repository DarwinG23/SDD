import { useState, useCallback } from 'react';
import { UploadPage } from './components/UploadPage';
import { StructuredPromptForm } from './components/StructuredPromptForm';
import { ValidationOverlay } from './components/ValidationOverlay';
import { TestResultsViewer } from './components/TestResultsViewer';
import { EvaluationMetrics } from './components/EvaluationMetrics';
import { ReportDownload } from './components/ReportDownload';
import { generateTests, executeTests, runEvaluation, generateReport } from './api/client';
import type { TestResult, EvaluationResult } from './api/client';

type OverlayState = 'loading' | 'success' | 'error' | 'generating' | 'generated' | null;

export default function App() {
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [overlayState, setOverlayState] = useState<OverlayState>(null);
  const [testCode, setTestCode] = useState('');
  const [overlayErrors, setOverlayErrors] = useState<string[]>([]);
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null);
  const [reportId, setReportId] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);

  const handleUploadSuccess = useCallback((sid: string) => {
    setSessionId(sid);
    setOverlayState('success');
  }, []);

  const handleGenerateTests = useCallback(async () => {
    if (!sessionId) return;
    setOverlayState('generating');
    try {
      const result = await generateTests(sessionId, '', '');
      if (result.success && result.test_code) {
        setTestCode(result.test_code);
        setOverlayState('generated');
      } else {
        setOverlayErrors([result.error || 'Error al generar pruebas']);
        setOverlayState('error');
      }
    } catch {
      setOverlayErrors(['Error de conexión con el servidor']);
      setOverlayState('error');
    }
  }, [sessionId]);

  const handlePromptSubmit = useCallback(async (prompt: string) => {
    if (!sessionId) return;
    setGenerating(true);
    try {
      const result = await generateTests(sessionId, prompt, '');
      if (result.success && result.test_code) {
        setTestCode(result.test_code);
        const execResult = await executeTests('', result.test_code);
        setTestResult(execResult);
        const evalResult = await runEvaluation('', result.test_code);
        setEvaluation(evalResult);
      }
    } catch {
      setOverlayErrors(['Error en la generación']);
    } finally {
      setGenerating(false);
    }
  }, [sessionId]);

  const handleGenerateReport = useCallback(async () => {
    if (!evaluation) return;
    try {
      const result = await generateReport(evaluation as unknown as Record<string, unknown>, testCode);
      setReportId(result.report_id);
    } catch {
      alert('Error al generar reporte');
    }
  }, [evaluation, testCode]);

  const handleCopyCode = useCallback(() => {
    navigator.clipboard.writeText(testCode);
  }, [testCode]);

  return (
    <div className="app">
      <header>
        <h1>SmartUnitTest</h1>
        <p>Sistema de evaluación de pruebas unitarias generadas por IA</p>
      </header>

      <main>
        <UploadPage onUploadSuccess={handleUploadSuccess} sessionId={sessionId} />

        {sessionId && (
          <section className="prompt-section">
            <h2>Prompt estructurado</h2>
            <StructuredPromptForm onSubmit={handlePromptSubmit} disabled={generating} />
          </section>
        )}

        <ValidationOverlay
          visible={overlayState !== null}
          state={overlayState}
          testCode={testCode}
          errors={overlayErrors}
          onGenerateTests={handleGenerateTests}
          onRetry={() => { setOverlayState(null); setSessionId(null); }}
          onClose={() => setOverlayState(null)}
          onCopyCode={handleCopyCode}
        />

        <TestResultsViewer result={testResult} />
        <EvaluationMetrics evaluation={evaluation} />
        <ReportDownload reportId={reportId} onGenerate={handleGenerateReport} generating={generating} />
      </main>
    </div>
  );
}
