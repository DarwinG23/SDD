# Diagrama de Casos de Uso UML

**Límite del Sistema (System Boundary):** `Sistema de eveluación de calidad  de pruebas unitarias con IA`

---

## 1. Actores

* **`Tester`**: Actor principal (humano) situado a la izquierda del sistema.
* **`QwenCoder`**: Actor secundario/externo (sistema IA) situado a la derecha del sistema.
* **`Pytest`**: Actor secundario/externo (herramienta de ejecución) situado a la derecha del sistema.

---

## 2. Casos de Uso

* **`Ingresar código fuente`**
* **`Ingresar prompt estructurado`**
* **`Generar promt de mejora`**
* **`Generar pruebas unitarias`**
* **`Ejecutar pruebas unitarias`**
* **`Generar reporte de resultados`**

---

## 3. Relaciones entre Actores y Casos de Uso

### Actor: `Tester`
* Interactúa con **`Ingresar código fuente`**.
* Interactúa con **`Ingresar prompt estructurado`**.
* Interactúa con **`Generar reporte de resultados`**.

### Actor: `QwenCoder`
* Interactúa con **`Generar promt de mejora`**.
* Interactúa con **`Generar pruebas unitarias`**.

### Actor: `Pytest`
* Interactúa con **`Ejecutar pruebas unitarias`**.

---

## 4. Relaciones entre Casos de Uso (Relaciones UML)

* **`Ingresar código fuente`** $\xrightarrow{\text{;\llInclude\gg>}}$ **`Ingresar prompt estructurado`**
  * Relación de inclusión desde `Ingresar código fuente` hacia `Ingresar prompt estructurado`.

* **`Generar promt de mejora`** $\xrightarrow{\text{;\llextend\gg>}}$ **`Generar reporte de resultados`**
  * Relación de extensión desde `Generar promt de mejora` hacia `Generar reporte de resultados`.

* **`Ejecutar pruebas unitarias`** $\xrightarrow{\text{;\llinclude\gg>}}$ **`Generar pruebas unitarias`**
  * Relación de inclusión desde `Ejecutar pruebas unitarias` hacia `Generar pruebas unitarias`.