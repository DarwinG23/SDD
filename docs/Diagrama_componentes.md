# Diagrama de Componentes UML

## 1. Componentes Principales y Subsistemas

### Componente: `FrontEnd`
* **Componentes internos:**
  * `«component» Navegador`
* **Interfaces y Conexiones:**
  * Consume la interfaz provista por el componente `Endpoints` dentro de la capa de **Presentación** del **BackEnd** (conexión mediante interfaz puerto/socket de tipo requiere-provee).

---

### Componente Principal: `BackEnd`
Se organiza internamente en 4 paquetes/capas de arquitectura:

#### A. Paquete `Presentación`
* **Componentes internos:**
  * `«component» Endpoints`
* **Relaciones internas:**
  * Posee una relación de dependencia (`-->`) hacia el paquete/componentes de **Negocio**.

#### B. Paquete `Negocio`
* **Componentes internos:**
  * `«component» Validación código`
  * `«component» Validación prompt`
  * `«component» Promt de mejora`
  * `«component» Evaluación`
  * `«component» Reportes`
* **Relaciones internas:**
  * Posee una relación de dependencia (`-->`) hacia el paquete/componentes de **Servicios**.
  * Posee una relación de dependencia (`-->`) hacia el paquete/componentes de **Persistencia** (específicamente señalando hacia `Modelos`).

#### C. Paquete `Servicios`
* **Componentes internos:**
  * `«component» Ejecución de Pruebas`
  * `«component» Servicio de IA`

#### D. Paquete `Persistencia`
* **Componentes internos:**
  * `«component» Modelos`
  * `«component» Repositorio`
* **Relaciones internas:**
  * `Modelos` tiene una relación de asociación/conexión punteada con `Repositorio`.

---

### Componente: `Base de datos`
* **Elementos internos:**
  * Representación física/lógica de la base de datos `BD`.
* **Interfaces y Conexiones:**
  * Provee/requiere una interfaz mediante la cual se conecta directamente con el componente `Repositorio` de la capa de **Persistencia**.

---

## 2. Flujo de Dependencias e Interacciones Generales

1. **`FrontEnd` (`Navegador`)** $\rightarrow$ Interactúa mediante interfaz con **`BackEnd` (`Presentación` / `Endpoints`)**.
2. **`Presentación` (`Endpoints`)** $\rightarrow$ Depende de la capa de **`Negocio`**.
3. **`Negocio`** $\rightarrow$ Depende de la capa de **`Servicios`** y de la capa de **`Persistencia` (`Modelos`)**.
4. **`Persistencia` (`Repositorio`)** $\rightarrow$ Interactúa mediante interfaz con la **`Base de datos` (`BD`)**.