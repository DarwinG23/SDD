## Context

Actualmente el resultado de la validación se muestra como un div inline debajo del formulario, sin separación visual del flujo de trabajo. No hay indicador de carga durante el proceso ni acciones claras después del resultado. El usuario debe interpretar el mensaje y decidir qué hacer sin guía visual.

## Goals / Non-Goals

**Goals:**
- Overlay a pantalla completa con spinner durante la validación
- Resultado visual diferenciado: verde (éxito) con botón "Generar pruebas unitarias", rojo (error) con botón "Volver a subir"
- Mantener compatibilidad con el backend existente y el formulario estructurado actual

**Non-Goals:**
- No se implementa la generación de pruebas
- No se modifican endpoints del backend
- No se cambia la lógica de almacenamiento o validación

## Decisions

### D1: Overlay DOM en lugar de modal externo

Se agrega un div fijo (`#validation-overlay`) directamente en `upload.html` con tres estados internos (cargando, éxito, error) controlados por clases CSS. No se requiere librería externa.

**Alternativa considerada:** Usar `dialog` HTML nativo o librería JS. Se descartó por simplicidad y control total de estilos.

### D2: Control de estado con clases CSS

El overlay usa tres clases: `.loading`, `.success`, `.error` para mostrar/ocultar secciones internas. El JS solo cambia clases, no manipula innerHTML para los estados.

**Alternativa considerada:** Renderizado condicional con JS. Se descartó por ser más frágil y difícil de mantener.

### D3: Reutilización del overlay existente

El overlay y sus secciones internas (spinner, resultado éxito, resultado error) están siempre en el DOM. El JS los muestra/oculta según el estado, evitando crear/destruir elementos.

### D4: Botón "Generar pruebas" como placeholder

El botón muestra un `alert()` o `toast` con "Funcionalidad próximamente" — sin llamada API ni navegación. Fácil de conectar cuando se implemente el endpoint.

## Risks / Trade-offs

- **[Riesgo] Overlay puede no renderizarse bien en pantallas muy pequeñas**: mitigado con estilos responsive y viewport units.
- **[Riesgo] El botón "Generar pruebas" actualmente no hace nada relevante**: aceptado por diseño — es un placeholder para el próximo cambio.
- **[Trade-off] Mantener tres estados en el DOM** aumenta el HTML pero simplifica el JS y la depuración.
