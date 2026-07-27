import { getReportDownloadUrl } from '../api/client';

interface ReportDownloadProps {
  reportId: string | null;
  onGenerate: () => void;
  generating?: boolean;
}

export function ReportDownload({ reportId, onGenerate, generating }: ReportDownloadProps) {
  return (
    <div className="report-download">
      <h3>Reporte de resultados</h3>
      {reportId ? (
        <a href={getReportDownloadUrl(reportId)} className="btn btn-primary" download>
          Descargar PDF
        </a>
      ) : (
        <button onClick={onGenerate} disabled={generating} className="btn btn-secondary" style={{ position: 'relative' }}>
          {generating ? 'Generando...' : 'Generar reporte'}
          {generating && (
            <div style={{
              position: 'absolute', bottom: 0, left: 0, height: 3,
              width: '100%', background: 'rgba(255,255,255,0.2)', borderRadius: 2, overflow: 'hidden',
            }}>
              <div className="loading-bar" />
            </div>
          )}
        </button>
      )}
    </div>
  );
}
