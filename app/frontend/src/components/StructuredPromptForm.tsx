import { useState } from 'react';

interface PromptFormData {
  context: string;
  code: string;
  tests: string;
}

interface StructuredPromptFormProps {
  onSubmit: (prompt: string) => void;
  disabled?: boolean;
}

export function StructuredPromptForm({ onSubmit, disabled }: StructuredPromptFormProps) {
  const [form, setForm] = useState<PromptFormData>({ context: '', code: '', tests: '' });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    if (!form.context.trim() || !form.code.trim() || !form.tests.trim()) {
      alert('Todos los campos son requeridos');
      return;
    }
    const combined = `Contexto:\n${form.context}\n\nCódigo:\n${form.code}\n\nPruebas:\n${form.tests}`;
    onSubmit(combined);
  };

  const set = (field: keyof PromptFormData) => (e: React.ChangeEvent<HTMLTextAreaElement>) =>
    setForm((prev) => ({ ...prev, [field]: e.target.value }));

  return (
    <form onSubmit={handleSubmit}>
      <div className="form-group">
        <label>Contexto</label>
        <textarea value={form.context} onChange={set('context')} rows={3} placeholder="Describe el contexto del código a probar..." required />
      </div>
      <div className="form-group">
        <label>Código</label>
        <textarea value={form.code} onChange={set('code')} rows={3} placeholder="Describe la funcionalidad específica..." required />
      </div>
      <div className="form-group">
        <label>Pruebas</label>
        <textarea value={form.tests} onChange={set('tests')} rows={3} placeholder="Especifica los casos de prueba esperados..." required />
      </div>
      <button type="submit" disabled={disabled} className="btn btn-primary">
        Generar pruebas
      </button>
    </form>
  );
}
