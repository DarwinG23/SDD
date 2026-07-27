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
        <button onClick={onGenerate} disabled={generating} className="btn btn-secondary">
          {generating ? 'Generando...' : 'Generar reporte'}
        </button>
      )}
    </div>
  );
}
