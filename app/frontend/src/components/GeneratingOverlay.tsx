import { useState, useEffect } from 'react';

interface GeneratingOverlayProps {
  testCode: string;
  onCopyCode: () => void;
  onNext: () => void;
  onRetry: () => void;
  error: string | null;
}

const particles = ['{', '}', '[', ']', '(', ')'];

export function GeneratingOverlay({ testCode, onCopyCode, onNext, onRetry, error }: GeneratingOverlayProps) {
  const [showCode, setShowCode] = useState(false);
  const [displayedText, setDisplayedText] = useState('');
  const [typing, setTyping] = useState(false);

  useEffect(() => {
    if (testCode) {
      setShowCode(true);
      setTyping(true);
      let i = 0;
      const interval = setInterval(() => {
        if (i < testCode.length) {
          setDisplayedText(testCode.slice(0, i + 50));
          i += 50;
        } else {
          clearInterval(interval);
          setTyping(false);
        }
      }, 30);
      return () => clearInterval(interval);
    }
  }, [testCode]);

  if (error) {
    return (
      <section className="glass-card" style={{ textAlign: 'center', padding: 48 }}>
        <div className="error-icon">&#10007;</div>
        <h3 style={{ margin: '16px 0 8px', color: 'var(--error)' }}>Error al generar pruebas</h3>
        <p style={{ color: 'var(--text-dim)', fontFamily: 'var(--mono)', fontSize: 13 }}>{error}</p>
        <div style={{ marginTop: 24, display: 'flex', gap: 12, justifyContent: 'center' }}>
          <button onClick={onRetry} className="btn btn-secondary">Reintentar</button>
        </div>
      </section>
    );
  }

  if (!showCode) {
    return (
      <section className="glass-card hologram" style={{ textAlign: 'center', padding: 48 }}>
        <div className="spinner" style={{ margin: '0 auto 24px' }} />
        <div className="loader-text">
          <span style={{ color: 'var(--text-dim)', fontFamily: 'var(--mono)', fontSize: 14 }}>
            Generando pruebas unitarias con IA...
          </span>
          <span className="cursor-blink" style={{ color: 'var(--neon)' }}>|</span>
        </div>
        <div style={{ marginTop: 32, position: 'relative', height: 60 }}>
          {particles.map((p, i) => (
            <span
              key={i}
              style={{
                position: 'absolute',
                left: '50%',
                top: '50%',
                fontSize: 20,
                color: `var(--${i % 3 === 0 ? 'neon' : i % 3 === 1 ? 'cyber' : 'purple'})`,
                opacity: 0.5,
                animation: `float 2s ease-in-out ${i * 0.3}s infinite`,
                transform: `translate(calc(-50% + ${[-80, 80, -60, 90, 0, -100][i]}px), calc(-50% + ${[-60, -40, 70, 50, -80, 20][i]}px))`,
              }}
            >
              {p}
            </span>
          ))}
        </div>
      </section>
    );
  }

  return (
    <section className="glass-card">
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 16 }}>
        <div className="success-icon" style={{ width: 32, height: 32, fontSize: 16, margin: 0 }}>
          &#10003;
        </div>
        <h3 style={{ margin: 0, color: 'var(--neon)' }}>Pruebas generadas</h3>
      </div>
      <div className="code-viewer" style={{ maxHeight: 400 }}>
        <div style={{
          display: 'flex',
          alignItems: 'center',
          gap: 8,
          padding: '8px 16px',
          background: 'rgba(0,255,65,0.03)',
          borderBottom: '1px solid rgba(0,255,65,0.05)',
          borderRadius: 'var(--radius) var(--radius) 0 0',
          margin: '-20px -20px 16px',
        }}>
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#ff5f57' }} />
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#ffbd2e' }} />
          <span style={{ width: 10, height: 10, borderRadius: '50%', background: '#28c840' }} />
          <span style={{ marginLeft: 12, color: 'var(--text-dim)', fontSize: 12, fontFamily: 'var(--mono)' }}>
            test_generated.py
          </span>
        </div>
        <pre style={{ margin: 0 }}>
          <code>{typing ? displayedText : testCode}</code>
          {typing && <span className="cursor-blink" style={{ color: 'var(--neon)' }}>|</span>}
        </pre>
      </div>
      <div style={{ marginTop: 20, display: 'flex', gap: 12, justifyContent: 'center' }}>
        <button onClick={onCopyCode} className="btn btn-secondary">Copiar código</button>
        <button onClick={onNext} className="btn btn-primary" disabled={typing}>Ver resultados</button>
      </div>
    </section>
  );
}
