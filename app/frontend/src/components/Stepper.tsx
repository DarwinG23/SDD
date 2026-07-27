export type StepId = 'upload' | 'configure' | 'generating' | 'results';

interface Step {
  id: StepId;
  label: string;
}

const steps: Step[] = [
  { id: 'upload', label: 'Subir código' },
  { id: 'configure', label: 'Configurar prompt' },
  { id: 'generating', label: 'Generar pruebas' },
  { id: 'results', label: 'Resultados' },
];

interface StepperProps {
  currentStep: StepId;
  onStepClick: (step: StepId) => void;
  completedSteps: Set<StepId>;
}

export function Stepper({ currentStep, onStepClick, completedSteps }: StepperProps) {
  return (
    <div style={{
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      gap: 0,
      marginBottom: 32,
      padding: '16px 24px',
      background: 'var(--bg-card)',
      backdropFilter: 'blur(12px)',
      WebkitBackdropFilter: 'blur(12px)',
      border: '1px solid var(--border-glow)',
      borderRadius: 'var(--radius-lg)',
    }}>
      {steps.map((step, i) => {
        const isActive = step.id === currentStep;
        const isCompleted = completedSteps.has(step.id);
        const isClickable = isCompleted || isActive;

        return (
          <div key={step.id} style={{ display: 'flex', alignItems: 'center' }}>
            <button
              onClick={() => isClickable && onStepClick(step.id)}
              disabled={!isClickable}
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: 8,
                background: 'none',
                border: 'none',
                cursor: isClickable ? 'pointer' : 'default',
                padding: '8px 12px',
                opacity: isActive || isCompleted ? 1 : 0.35,
                transition: 'opacity 0.3s',
                color: isActive ? 'var(--cyber)' : isCompleted ? 'var(--neon)' : 'var(--text-dim)',
                fontFamily: 'var(--mono)',
                fontSize: 12,
                fontWeight: isActive ? 700 : 500,
                textTransform: 'uppercase',
                letterSpacing: '1px',
              }}
            >
              <span style={{
                display: 'inline-flex',
                alignItems: 'center',
                justifyContent: 'center',
                width: 24,
                height: 24,
                borderRadius: '50%',
                background: isActive ? 'var(--cyber-dim)' : isCompleted ? 'var(--success-bg)' : 'transparent',
                border: `1px solid ${isActive ? 'var(--cyber)' : isCompleted ? 'var(--neon)' : 'var(--text-dim)'}`,
                color: isActive ? 'var(--cyber)' : isCompleted ? 'var(--neon)' : 'var(--text-dim)',
                fontSize: 11,
                fontWeight: 700,
              }}>
                {isCompleted ? '✓' : i + 1}
              </span>
              {step.label}
            </button>
            {i < steps.length - 1 && (
              <div style={{
                width: 40,
                height: 1,
                background: isCompleted
                  ? 'linear-gradient(90deg, var(--neon-dim), var(--border-glow))'
                  : 'var(--border-glow)',
                margin: '0 4px',
              }} />
            )}
          </div>
        );
      })}
    </div>
  );
}
