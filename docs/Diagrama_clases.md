# Diagrama de Clases UML (PSM)

## 1. Enumeraciones (`<<enumeration>>`)

### `Tipo`
* **Valores:**
  * `GENERACION : str = "GENERACION"`
  * `REFACTORIZACION : str = "REFACTORIZACION"`

---

### `Estado`
* **Valores:**
  * `GENERADA : str = "GENERADA"`
  * `EJECUTADA : str = "EJECUTADA"`
  * `EXITOSA : str = "EXITOSA"`
  * `FALLIDA : str = "FALLIDA"`

---

## 2. Clases

### `Plantilla`
* **Atributos:**
  * `- id_plantilla: int`
  * `- nombre: str`
  * `- tipo: Tipo`
  * `- lenguaje: str`
  * `- version: str`
  * `- objetivo: str`
  * `- salida: str`
  * `- frameworck: str`
  * `- promts: List[int]`
* **Relaciones:**
  * Usa la enumeración `Tipo` (relación de dependencia con flecha punteada).
  * **Asociación:** `Plantilla` (1) -- Tiene -- `Promt` (0..*)

---

### `Promt`
* **Atributos:**
  * `- id_promt: int`
  * `- contenido: str`
  * `- objetivo: str`
  * `- detalle: str`
  * `- id_plantilla: int`
* **Métodos:**
  * `+ validar_plantilla(id_plantilla: int): bool`
* **Relaciones:**
  * **Asociación:** `Plantilla` (1) -- Tiene -- `Promt` (0..*)
  * **Asociación:** `Promt` (1..*) -- Tiene -- `CodigoFuente` (1)

---

### `CodigoFuente`
* **Atributos:**
  * `- id_CodigoFuente: int`
  * `- nombre_archivo: str`
  * `- contenido: str`
  * `- lenguaje: str`
  * `- numero_lineas: int`
  * `- validado: bool`
  * `- evaluaciones: List[int]`
  * `- pruebas: List[int]`
* **Métodos:**
  * `+ validar_sintaxis_ast(): bool`
* **Relaciones:**
  * **Asociación:** `Promt` (1..*) -- Tiene -- `CodigoFuente` (1)
  * **Asociación:** `CodigoFuente` (1) -- Tiene -- `PruebaUnitaria` (1..*)
  * **Asociación:** `CodigoFuente` (1) -- Tiene -- `Evaluacion` (1..*)

---

### `PruebaUnitaria`
* **Atributos:**
  * `- id_PruebaUnitaria: int`
  * `- codigoPrueba : str`
  * `- estado : Estado`
  * `- detalle: str`
  * `- salidaEsperada: str`
  * `- id_CodigoFuente: int`
* **Relaciones:**
  * Usa la enumeración `Estado` (relación de dependencia con flecha punteada).
  * **Asociación:** `CodigoFuente` (1) -- Tiene -- `PruebaUnitaria` (1..*)

---

### `Evaluacion`
* **Atributos:**
  * `- id_Evaluacion: int`
  * `- resultado: bool`
  * `- detalle: str`
  * `- id_reporte: int`
* **Métodos:**
  * `+ ejecutar_evaluacion(id_prueba: str): bool`
  * `+ calcular_metricas(): float`
* **Relaciones:**
  * **Asociación:** `CodigoFuente` (1) -- Tiene -- `Evaluacion` (1..*)
  * **Asociación:** `Evaluacion` (1) -- Tiene -- `Medicion` (*)
  * **Asociación:** `Evaluacion` (1) -- Genera -- `Reporte` (1)

---

### `Reporte`
* **Atributos:**
  * `- id_Reporte: int`
  * `- formato: str`
  * `- fechaGeneracion: datetime.date`
  * `- detalle: str`
  * `- id_evaluacion: int`
* **Métodos:**
  * `+ generar_reporte_pdf(id_evaluacion: int): str`
  * `+ descargar_archivo(): bytes`
* **Relaciones:**
  * **Asociación:** `Evaluacion` (1) -- Genera -- `Reporte` (1)

---

### `Medicion`
* **Atributos:**
  * `- id_Medicion: int`
  * `- valor: float`
  * `- fecha: datetime`
  * `- id_TipoMetrica: int`
  * `- id_Evaluacion: int`
* **Relaciones:**
  * **Asociación:** `Evaluacion` (1) -- Tiene -- `Medicion` (*)
  * **Asociación:** `Medicion` (*) -- Tiene -- `TipoMetrica` (1)

---

### `TipoMetrica`
* **Atributos:**
  * `- id_TipoMetrica: int`
  * `- nombre: str`
  * `- descripcion: str`
  * `- unidad: str`
* **Relaciones:**
  * **Asociación:** `Medicion` (*) -- Tiene -- `TipoMetrica` (1)
  * **Asociación:** `TipoMetrica` (1) -- Tiene -- `Rango` (*)

---

### `Rango`
* **Atributos:**
  * `- id_Rango: int`
  * `- limiteInferior: float`
  * `- limiteSuperior: float`
  * `- id_TipoMetrica: int`
  * `- id_Fenomeno: int`
* **Relaciones:**
  * **Asociación:** `TipoMetrica` (1) -- Tiene -- `Rango` (*)
  * **Asociación:** `Rango` (*) -- Tiene -- `Fenomeno` (1)

---

### `Fenomeno`
* **Atributos:**
  * `- id_Fenomeno: int`
  * `- nombre: str`
  * `- descripcion: str`
  * `- estado: bool`
* **Relaciones:**
  * **Asociación:** `Rango` (*) -- Tiene -- `Fenomeno` (1)