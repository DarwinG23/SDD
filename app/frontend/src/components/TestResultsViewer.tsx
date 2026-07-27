import type { TestResult } from '../api/client';

interface TestResultsViewerProps {
  result: TestResult | null;
}

export function TestResultsViewer({ result }: TestResultsViewerProps) {
  if (!result) return null;

  return (
    <div className="test-results">
      <h3>Resultados de ejecución</h3>
      <div className={`result-badge ${result.success ? 'success' : 'failure'}`}>
        {result.success ? 'Pruebas pasaron' : 'Pruebas fallaron'}
      </div>
      <p>Pasaron: {result.passed} | Fallaron: {result.failed}</p>
      {result.stdout && (
        <div className="output-section">
          <h4>Salida estándar</h4>
          <pre>{result.stdout}</pre>
        </div>
      )}
      {result.stderr && (
        <div className="output-section">
          <h4>Errores</h4>
          <pre className="error-output">{result.stderr}</pre>
        </div>
      )}
    </div>
  );
}
