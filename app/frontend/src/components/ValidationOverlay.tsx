interface ValidationOverlayProps {
  visible: boolean;
  state: 'loading' | 'success' | 'error' | 'generating' | 'generated' | null;
  testCode?: string;
  errors?: string[];
  onGenerateTests?: () => void;
  onRetry?: () => void;
  onClose?: () => void;
  onCopyCode?: () => void;
}

export function ValidationOverlay({ visible, state, testCode, errors, onGenerateTests, onRetry, onClose, onCopyCode }: ValidationOverlayProps) {
  if (!visible) return null;

  return (
    <div className="overlay">
      <div className="overlay-backdrop" />
      <div className="overlay-content">
        {state === 'loading' && (
          <div className="overlay-state">
            <div className="spinner" />
            <p>Validando código fuente...</p>
          </div>
        )}

        {state === 'success' && (
          <div className="overlay-state">
            <div className="success-icon">&#10003;</div>
            <h3>Código válido</h3>
            <p>El archivo ha sido validado correctamente.</p>
            <button onClick={onGenerateTests} className="btn btn-primary">Generar pruebas unitarias</button>
          </div>
        )}

        {state === 'generating' && (
          <div className="overlay-state">
            <div className="spinner" />
            <p>Generando pruebas unitarias con IA...</p>
          </div>
        )}

        {state === 'generated' && (
          <div className="overlay-state">
            <div className="success-icon">&#10003;</div>
            <h3>Pruebas generadas</h3>
            <pre className="code-viewer"><code>{testCode}</code></pre>
            <div className="overlay-actions">
              <button onClick={onCopyCode} className="btn btn-secondary">Copiar código</button>
              <button onClick={onClose} className="btn btn-primary">Cerrar</button>
            </div>
          </div>
        )}

        {state === 'error' && (
          <div className="overlay-state">
            <div className="error-icon">&#10007;</div>
            <h3>Error</h3>
            <ul>{errors?.map((e, i) => <li key={i}>{e}</li>)}</ul>
            <button onClick={onRetry} className="btn btn-secondary">Volver a subir</button>
          </div>
        )}
      </div>
    </div>
  );
}
