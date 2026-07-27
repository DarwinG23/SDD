import { useState, useCallback, useRef } from 'react';

interface UploadPageProps {
  onUploadSuccess: (sessionId: string, sourcePath?: string) => void;
  sessionId: string | null;
}

export function UploadPage({ onUploadSuccess, sessionId: _sessionId }: UploadPageProps) {
  const [file, setFile] = useState<File | null>(null);
  const [projectName, setProjectName] = useState('');
  const [dragging, setDragging] = useState(false);
  const [uploading, setUploading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const handleFile = useCallback((f: File) => {
    setError(null);
    if (!f.name.endsWith('.py')) {
      setError('Solo se permiten archivos .py');
      return;
    }
    setFile(f);
    setProjectName(f.name.replace(/\.py$/i, ''));
  }, []);

  const handleDrop = useCallback((e: React.DragEvent) => {
    e.preventDefault();
    setDragging(false);
    if (e.dataTransfer.files.length > 0) handleFile(e.dataTransfer.files[0]);
  }, [handleFile]);

  const handleSubmit = useCallback(async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    setUploading(true);

    const formData = new FormData();
    formData.append('file', file);
    formData.append('project_name', projectName);
    formData.append('prompt', ''); // Prompt built on submit

    try {
      const res = await fetch('/api/v1/upload/source', { method: 'POST', body: formData });
      const data = await res.json();
      if (res.ok) {
        onUploadSuccess(data.sessionId, data.sourcePath);
      } else if (data.errors) {
        const msgs = data.errors.map((e: { line?: number; message: string }) =>
          `Línea ${e.line || '?'}: ${e.message}`
        );
        setError(msgs.join('\n'));
      } else if (Array.isArray(data.detail)) {
        setError(data.detail.map((d: { msg: string }) => d.msg).join('; '));
      } else {
        setError(data.detail || 'Error al subir archivo');
      }
    } catch (e) {
      console.error('Upload error:', e);
      setError('Error de conexión con el servidor');
    } finally {
      setUploading(false);
    }
  }, [file, projectName, onUploadSuccess]);

  return (
    <section className="upload-section">
      <h2>Subir código fuente</h2>
      <p>Arrastra tu archivo <code>.py</code> o haz clic para seleccionarlo.</p>

      <form onSubmit={handleSubmit}>
        <div
          className={`drop-zone ${dragging ? 'dragover' : ''}`}
          onDragOver={(e) => { e.preventDefault(); setDragging(true); }}
          onDragLeave={() => setDragging(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
        >
          {file ? (
            <div className="file-info">
              <span>{file.name}</span>
              <button type="button" onClick={(e) => { e.stopPropagation(); setFile(null); }}>&times;</button>
            </div>
          ) : (
            <p>Arrastra tu archivo .py aquí o haz clic para seleccionar</p>
          )}
          <input ref={fileInputRef} type="file" accept=".py" hidden onChange={(e) => e.target.files?.[0] && handleFile(e.target.files[0])} />
        </div>

        <div className="form-group">
          <label>Nombre del proyecto</label>
          <input type="text" value={projectName} onChange={(e) => setProjectName(e.target.value)} placeholder="Ej: MiProyecto" required />
        </div>

        {error && (
          <div style={{
            color: 'var(--error)',
            fontFamily: 'var(--mono)',
            fontSize: 13,
            padding: '8px 12px',
            background: 'var(--error-bg)',
            border: '1px solid rgba(255, 51, 85, 0.2)',
            borderRadius: 'var(--radius)',
            marginBottom: 16,
          }}>
            {error}
          </div>
        )}

        <button type="submit" disabled={!file || uploading} className="btn btn-primary">
          {uploading ? 'Subiendo...' : 'Subir y validar'}
        </button>
      </form>
    </section>
  );
}
