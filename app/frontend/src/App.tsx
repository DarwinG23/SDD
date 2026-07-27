import { useState, useCallback } from 'react';
import { UploadPage } from './components/UploadPage';
import { StructuredPromptForm } from './components/StructuredPromptForm';
import { Stepper } from './components/Stepper';
import { MatrixRain } from './components/MatrixRain';
import { GeneratingOverlay } from './components/GeneratingOverlay';
import { TestResultsViewer } from './components/TestResultsViewer';
import { EvaluationMetrics } from './components/EvaluationMetrics';
import { ReportDownload } from './components/ReportDownload';
import { generateTests, executeTests, runEvaluation, generateReport } from './api/client';
import type { StepId } from './components/Stepper';
import type { TestResult, EvaluationResult } from './api/client';

export default function App() {
  const [currentStep, setCurrentStep] = useState<StepId>('upload');
  const [completedSteps, setCompletedSteps] = useState<Set<StepId>>(new Set());
  const [sessionId, setSessionId] = useState<string | null>(null);
  const [sourcePath, setSourcePath] = useState<string>('');
  const [testCode, setTestCode] = useState('');
  const [genError, setGenError] = useState<string | null>(null);
  const [testResult, setTestResult] = useState<TestResult | null>(null);
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null);
  const [reportId, setReportId] = useState<string | null>(null);
  const [generating, setGenerating] = useState(false);

  const completeStep = useCallback((step: StepId) => {
    setCompletedSteps(prev => new Set(prev).add(step));
  }, []);

  const handleUploadSuccess = useCallback((sid: string, sp?: string) => {
    setSessionId(sid);
    setSourcePath(sp || '');
    completeStep('upload');
    setCurrentStep('configure');
  }, [completeStep]);

  const handlePromptSubmit = useCallback(async (prompt: string) => {
    if (!sessionId) return;
    setCurrentStep('generating');
    setGenError(null);
    completeStep('configure');
    setGenerating(true);
    try {
      const result = await generateTests(sessionId, prompt, '');
      if (result.success && result.test_code) {
        setTestCode(result.test_code);
        const execResult = await executeTests(sessionId, result.test_code);
        setTestResult(execResult);
        const evalResult = await runEvaluation(sourcePath, result.test_code);
        setEvaluation(evalResult);
      } else {
        setGenError(result.error || 'Error al generar pruebas');
      }
    } catch {
      setGenError('Error de conexión con el servidor');
    } finally {
      setGenerating(false);
    }
  }, [sessionId, sourcePath, completeStep]);

  const handleNextToResults = useCallback(() => {
    completeStep('generating');
    setCurrentStep('results');
  }, [completeStep]);

  const handleCopyCode = useCallback(() => {
    navigator.clipboard.writeText(testCode);
  }, [testCode]);

  const handleRetry = useCallback(() => {
    setGenError(null);
    setTestCode('');
    setCurrentStep('configure');
  }, []);

  const handleGenerateReport = useCallback(async () => {
    if (!evaluation) return;
    try {
      const result = await generateReport(evaluation as unknown as Record<string, unknown>, testCode);
      setReportId(result.report_id);
    } catch {
      alert('Error al generar reporte');
    }
  }, [evaluation, testCode]);

  const handleStepClick = useCallback((step: StepId) => {
    setCurrentStep(step);
  }, []);

  return (
    <>
      <MatrixRain />
      <div className="app">
        <header>
          <h1>SmartUnitTest</h1>
          <p>Sistema de evaluación de pruebas unitarias generadas por IA</p>
        </header>

        <Stepper
          currentStep={currentStep}
          onStepClick={handleStepClick}
          completedSteps={completedSteps}
        />

        <main>
          {currentStep === 'upload' && (
            <UploadPage onUploadSuccess={handleUploadSuccess} sessionId={sessionId} />
          )}

          {currentStep === 'configure' && sessionId && (
            <section>
              <h2>Configurar prompt</h2>
              <StructuredPromptForm onSubmit={handlePromptSubmit} disabled={generating} />
            </section>
          )}

          {currentStep === 'generating' && (
            <GeneratingOverlay
              testCode={testCode}
              onCopyCode={handleCopyCode}
              onNext={handleNextToResults}
              onRetry={handleRetry}
              error={genError}
            />
          )}

          {currentStep === 'results' && (
            <>
              <section>
                <TestResultsViewer result={testResult} />
              </section>
              <section>
                <EvaluationMetrics evaluation={evaluation} />
              </section>
              <section>
                <ReportDownload reportId={reportId} onGenerate={handleGenerateReport} generating={generating} />
              </section>
            </>
          )}
        </main>
      </div>
    </>
  );
}
