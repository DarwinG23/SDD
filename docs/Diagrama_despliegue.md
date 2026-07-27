# Diagrama de Despliegue UML (PSM)

## 1. Nodos, Entornos de Ejecución y Artefactos

### Nodo: `<<divice>>` Navegador Web
* **Entorno de ejecución (`<<executionEnvironment>>`):** `Navegador`
  * **Artefacto (`<<artifact>>`):** `FrontEnd (React)`

---

### Nodo: `<<divice>>` Host Linux
Contiene el siguiente entorno de ejecución principal:
* **Entorno de ejecución (`<<executionEnvironment>>`):** `Docker Compose`

#### Contenedores (`<<container>>`) dentro de `Docker Compose`:

1. **`<<container>>` Servidor Ngix**
   * **Artefacto (`<<artifact>>`):** `Reverse proxy (Ngix)`

2. **`<<container>>` Backend**
   * **Módulos/Paquetes internos:**
     * `Presentación (Python, FastApi)`
     * `Negocio (Python)`
     * `Persistencia (Python, SQLAlchemy)`
     * `Servicios (Python)`
   * **Relaciones internas de dependencia:**
     * `Presentación (Python, FastApi)` $\rightarrow$ `Negocio (Python)`
     * `Negocio (Python)` $\rightarrow$ `Persistencia (Python, SQLAlchemy)`
     * `Negocio (Python)` $\rightarrow$ `Servicios (Python)`

3. **`<<container>>` Base de datos**
   * **Artefacto (`<<artifact>>`):** `PostgreSQL` (incluye símbolo de base de datos `BD`)

---

### Nodo: `<<divice>>` Proveedor Cloud
* **Entorno de ejecución (`<<executionEnvironment>>`):** `Servicio IA`
  * **Artefacto (`<<artifact>>`):** `Api QwenCoder`

---

## 2. Conexiones y Comunicaciones

* **`FrontEnd (React)`** $\leftrightarrow$ **`Reverse proxy (Ngix)`**
  * **Protocolo:** `HTTP (443)`

* **`Reverse proxy (Ngix)`** $\leftrightarrow$ **`Presentación (Python, FastApi)`**
  * **Protocolo:** `HTTP (80)`

* **`Persistencia (Python, SQLAlchemy)`** $\leftrightarrow$ **`PostgreSQL`**
  * **Protocolo:** `TCP (5432) Postgre SQL Protocol`

* **`Servicios (Python)`** $\leftrightarrow$ **`Api QwenCoder`**
  * **Protocolo:** `HTTP (11434)`