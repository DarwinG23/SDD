import type { EvaluationResult } from '../api/client';

interface EvaluationMetricsProps {
  evaluation: EvaluationResult | null;
}

export function EvaluationMetrics({ evaluation }: EvaluationMetricsProps) {
  if (!evaluation) return null;

  const metrics = [
    { name: 'Cobertura de código', value: evaluation.coverage, threshold: 80 },
    { name: 'Mutation Score', value: evaluation.mutation_score, threshold: 70 },
    { name: 'Detección de fallos', value: evaluation.failure_detection, threshold: 60 },
  ];

  return (
    <div className="evaluation-metrics">
      <h3>Métricas de Calidad</h3>
      <div className={`overall-badge ${evaluation.all_passed ? 'success' : 'failure'}`}>
        {evaluation.all_passed ? 'TODAS LAS MÉTRICAS CUMPLEN' : 'ALGUNAS MÉTRICAS NO CUMPLEN'}
      </div>
      <table className="metrics-table">
        <thead>
          <tr>
            <th>Métrica</th>
            <th>Valor</th>
            <th>Umbral</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {metrics.map((m) => {
            const passed = m.value >= m.threshold;
            return (
              <tr key={m.name} className={passed ? 'passed' : 'failed'}>
                <td>{m.name}</td>
                <td>{m.value.toFixed(1)}%</td>
                <td>{m.threshold}%</td>
                <td>{passed ? '✓ Cumple' : '✗ No cumple'}</td>
              </tr>
            );
          })}
        </tbody>
      </table>
    </div>
  );
}
