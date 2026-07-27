# Diagrama de Paquetes UML

## 1. Paquetes y Subpaquetes

### Paquete: `FrontEnd`
* **Subpaquetes internos:**
  * `ui`
  * `api_client`
* **Relaciones:**
  * Posee una relación de dependencia con estereotipo `«use»` dirigida hacia el paquete **`Presentacion`** dentro de **`BackEnd`**.

---

### Paquete Contenedor: `BackEnd`
Agrupa los siguientes paquetes internos:

#### A. Paquete `Presentacion`
* **Subpaquetes internos:**
  * `controllers`
  * `dto`
* **Relaciones:**
  * Recibe una dependencia `«use»` desde **`FrontEnd`**.
  * Posee una relación de dependencia con estereotipo `«use»` que sale del subpaquete `controllers` dirigida hacia el paquete **`Negocio`**.

#### B. Paquete `Negocio`
* **Subpaquetes internos:**
  * `validation`
  * `evaluation`
  * `prompts`
  * `reports`
* **Relaciones:**
  * Recibe una dependencia `«use»` desde `Presentacion.controllers`.
  * Posee una relación de dependencia con estereotipo `«use»` dirigida hacia el paquete **`Servicios`**.
  * Posee una relación de dependencia con estereotipo `«use»` dirigida hacia el paquete **`Persistencia`**.

#### C. Paquete `Servicios`
* **Subpaquetes internos:**
  * `ai_service`
  * `test_runner`
* **Relaciones:**
  * Recibe una dependencia `«use»` desde el paquete **`Negocio`**.

#### D. Paquete `Persistencia`
* **Subpaquetes internos:**
  * `models`
  * `repositories`
* **Relaciones:**
  * Recibe una dependencia `«use»` desde el paquete **`Negocio`**.

---

## 2. Flujo de Dependencias Resumido

1. **`FrontEnd`** $\xrightarrow{\text{«use»}}$ **`BackEnd.Presentacion`**
2. **`Presentacion.controllers`** $\xrightarrow{\text{«use»}}$ **`Negocio`**
3. **`Negocio`** $\xrightarrow{\text{«use»}}$ **`Servicios`**
4. **`Negocio`** $\xrightarrow{\text{«use»}}$ **`Persistencia`**