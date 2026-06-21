## Documento de modelado técnico

##### Proyecto: SmartUnitTest: Sistema de evaluación de

##### pruebas unitarias generadas por IA mediante

##### métricas de calidad de software.

##### Revisión 1. 0

```
05/11/
```

```
Documento de modelado técnico
Pág. 2
```
# 1 Formulación del problema y solución

## 1.1 Contexto

```
En el desarrollo moderno de software, las pruebas unitarias constituyen una práctica
esencial para garantizar la calidad, confiabilidad y mantenibilidad del código. Estas
pruebas permiten validar el comportamiento de componentes individuales del sistema y
facilitan la detección temprana de errores durante el ciclo de desarrollo. Con la adopción
de metodologías ágiles y el incremento en la complejidad de los sistemas software, se
ha incrementado la necesidad de automatizar actividades relacionadas con el
aseguramiento de calidad. En este contexto, las herramientas basadas en Inteligencia
Artificial Generativa han comenzado a utilizarse para apoyar la generación automática
de pruebas unitarias, mejorando la eficiencia del proceso de desarrollo.
```
## 1.2 Problemática

```
A pesar del avance en herramientas de generación automática, la mayoría de estas
soluciones se centran únicamente en la creación de código de prueba, sin considerar
criterios de calidad que permitan evaluar su efectividad. Esto genera un problema
importante, ya que las pruebas generadas pueden presentar deficiencias en aspectos
como cobertura, mantenibilidad, redundancia o capacidad para detectar fallos reales.
Además, los desarrolladores no cuentan con mecanismos automáticos que les permitan
analizar la calidad de dichas pruebas de manera objetiva. Como resultado, se integran
pruebas unitarias que no siempre cumplen estándares adecuados de calidad, afectando
la confiabilidad del proceso de aseguramiento de software.
```
## 1.3 Solución

```
Consiste en el desarrollo de una plataforma que integra Inteligencia Artificial Generativa
para la creación automática de pruebas unitarias a partir de código fuente en Python,
utilizando una plantilla de entrada estructurada (prompt). Estas pruebas son ejecutadas
mediante el framework pytest, Posteriormente, el sistema aplica métricas de calidad de
software como cobertura de código, análisis de mutaciones y detección de fallos para
evaluar la efectividad de las pruebas generadas. Con base en estos resultados, la
plataforma genera recomendaciones de mejora y un reporte final en formato PDF,
integrando en un solo flujo la generación, ejecución y evaluación de pruebas unitarias.
```
## 1.4 justificación

```
La solución incorpora un módulo de evaluación que permite analizar su calidad mediante
indicadores como cobertura de código, análisis de mutaciones y detección de fallos. El
sistema genera recomendaciones de mejora basadas en los resultados obtenidos, lo
que facilita la iteración y optimización de las pruebas producidas. De esta manera, la
herramienta propuesta aporta valor tanto en contextos académicos como profesionales,
al reducir el esfuerzo manual requerido, incrementar la calidad de las pruebas unitarias y
fortalecer los procesos de aseguramiento de calidad en el desarrollo de software.
```

```
Documento de modelado técnico
Pág. 3
```
### 1.5 Alcance

El proyecto incluirá:

- Ingreso de código fuente (clases y funciones) en Python.
- Ingreso de prompt estructurado mediante una plantilla predefinida para la
- generación de pruebas unitarias
- Generación automática de pruebas unitarias mediante IA (GPT 4 ).
- Ejecución de pruebas con pytest.
- Evaluación mediante métricas de calidad (cobertura de código, puntaje de
- mutación y detección de fallos).
- Generación automática de prompt de mejora basados en los resultados
- obtenidos de la evaluación de calidad de las pruebas.
- Generación de reporte de resultados de la evaluación en formato PDF.
Fuera de alcance
- Soporte para múltiples lenguajes.
- Integración con varios modelos de IA.
- Pruebas de integración, rendimiento, seguridad u otras.
- Integración con CI/CD.
Limitaciones
- El sistema dependerá de la calidad del modelo de IA utilizado.
- La evaluación estará limitada a un conjunto específico de métricas.
- El rendimiento puede variar dependiendo del tamaño del código analizado.

### 1.6 Stakeholders

```
Tipo de usuario Tester
Tipo Humano
Descripción
Persona que ingresa el código fuente en el sistema y revisa
los resultados generados
Objetivos Mejorar la calidad de las pruebas unitarias
Actividades Descarga reporte, ingresar promt, subir código fuente
```
```
Tipo de usuario Sistema IA
Tipo Sistema externo
Descripción
Componente que genera automáticamente pruebas
unitarias a partir del código proporcionado.
Objetivos Proporcionar resultados automáticos
Actividades Generar pruebas unitarias
```
```
Tipo de usuario Framework de pruebas
Tipo Sistema externo
```
Descripción (^) Herramienta encargada de ejecutar las pruebas unitarias
generadas.
Objetivos Ejecutar pruebas unitarias generadas y devolver resultados
estructurados sobre su ejecución (éxito, fallo, errores o
excepciones).
Actividades - Ejecutar pruebas unitarias

- Registrar resultados de ejecución
- Reportar fallos o errores detectados


```
Documento de modelado técnico
Pág. 4
```
# 2 Especificación de requisitos estructurada

## 2.1 Requisitos Funcionales

## Número de requisito RF

## Nombre de requisito Ingresar código fuente

## Tipo Requerimiento funcional

## Fuente del requisito Desarrollador

```
Descripción
del
```
## requerimiento

```
Permite al usuario ingresar código fuente en Python
correspondiente a funciones o clases para su análisis y
```
## generación automática de pruebas unitarias.

## Prioridad del requisito Alta

## Número de requisito RF

## Nombre de requisito Validar código fuente

## Tipo Requerimiento funcional^

## Fuente del requisito Desarrollador

```
Descripción
del
```
## requerimiento

```
Permite verificar que el código fuente ingresado no contenga
```
## errores de sintaxis antes de generar las pruebas unitarias.

## Prioridad del requisito Alta

## Número de requisito RF

## Nombre de requisito Ingresar prompt estructurado

## Tipo Requerimiento funcional

## Fuente del requisito Desarrollador

```
Descripción
del
```
## requerimiento

```
Permite al usuario ingresar un prompt basado en una plantilla
predefinida con el fin de guiar correctamente la generación
automática de pruebas unitarias mediante inteligencia
```
## artificial.

## Prioridad del requisito Alta

## Número de requisito RF

## Nombre de requisito Validar prompt ingresado

## Tipo Requerimiento funcional^

## Fuente del requisito Desarrollador

```
Descripción
del
```
## requerimiento

```
Permite verificar que el prompt ingresado cumpla con la
estructura y parámetros definidos por la plantilla establecida
```
## antes de iniciar la generación de pruebas.

## Prioridad del requisito Alta


```
Documento de modelado técnico
Pág. 5
```
#### Número de requisito RF

#### Nombre de requisito Generar pruebas unitarias

#### Tipo Requerimiento funcional^

#### Fuente del requisito Desarrollador

Descripción
del

#### requerimiento

```
Permite generar automáticamente pruebas unitarias
utilizando inteligencia artificial a partir del código fuente y el
```
#### prompt proporcionado por el usuario.

#### Prioridad del requisito Alta

#### Número de requisito RF

#### Nombre de requisito Evaluar calidad de pruebas

#### Tipo Requerimiento funcional^

#### Fuente del requisito Desarrollador

Descripción
del

#### requerimiento

```
Permite ejecutar las pruebas unitarias generadas mediante el
framework pytest para obtener resultados de validación y
métricas de calidad(cobertura, mutación y detección de
```
#### fallos).

#### Prioridad del requisito Alta

#### Número de requisito RF

#### Nombre de requisito Evaluar calidad de pruebas

#### Tipo Requerimiento funcional^

#### Fuente del requisito Desarrollador

Descripción
del

#### requerimiento

```
Permite evaluar la calidad de las pruebas unitarias generadas
mediante métricas como cobertura de código, puntaje de
```
#### mutación y detección de fallos.

#### Prioridad del requisito Alta

#### Número de requisito RF

#### Nombre de requisito Generar prompts de mejora

#### Tipo Requerimiento funcional^

#### Fuente del requisito Desarrollador

Descripción
del

#### requerimiento

```
Permite generar automáticamente prompts de mejora si no se
cumplen los resultados mínimos de las métricas de calidad
durante la evaluación de las pruebas unitarias.(cobertura
```
#### 80%, puntaje de mutación 70% y detección de fallos 60%).

#### Prioridad del requisito Alta

#### Número de requisito RF

#### Nombre de requisito Regenerar pruebas unitarias

#### Tipo Requerimiento funcional

#### Fuente del requisito Desarrollador

Descripción
del

#### requerimiento

```
Permite generar nuevamente pruebas unitarias utilizando los
```
#### prompts de mejora generados por el sistema.

#### Prioridad del requisito Alta


```
Documento de modelado técnico
Pág. 6
```
#### Número de requisito RF

#### Nombre de requisito Generar reporte de resultados

#### Tipo Requerimiento funcional^

#### Fuente del requisito Desarrollador

```
Descripción
del
```
#### requerimiento

```
Permite generar un reporte con los resultados obtenidos de la
ejecución y evaluación de las pruebas unitarias y el promt de
```
#### mejora si es que es necesario.

#### Prioridad del requisito Alta

#### Número de requisito RF

#### Nombre de requisito Descargar reporte de resultados

#### Tipo Requerimiento funcional^

#### Fuente del requisito Desarrollador

```
Descripción
del
```
#### requerimiento

```
Permite descargar el reporte en formato PDF con los
resultados obtenidos de la ejecución y evaluación de las
```
#### pruebas unitarias.

#### Prioridad del requisito Alta

### 2.2 Requisitos No Funcionales

#### Número de requisito RNF

#### Nombre de requisito Interfaz intuitiva de usuario

#### Categoría Usabilidad

#### Tipo Requerimiento no funcional^

#### Fuente del requisito Desarrollador

```
Descripción
del
```
#### requerimiento

```
El sistema deberá presentar una interfaz simple e intuitiva
que facilite el ingreso de código fuente y la visualización de
```
#### resultados de evaluación.

#### Prioridad del requisito Media

#### Número de requisito RNF

#### Nombre de requisito Tiempo eficiente de procesamiento

#### Categoría Rendimiento

#### Tipo Requerimiento no funcional^

#### Fuente del requisito Desarrollador

```
Descripción
del
```
#### requerimiento

```
El sistema deberá procesar, ejecutar y evaluar pruebas
unitarias en un tiempo máximo de 60 segundos para códigos
```
#### fuente de hasta 500 líneas.

#### Prioridad del requisito Alta


```
Documento de modelado técnico
Pág. 7
```
## Número de requisito RNF

## Nombre de requisito Compatibilidad multiplataforma

## Categoría Compatibilidad

## Tipo Requerimiento no funcional

## Fuente del requisito Desarrollador

```
Descripción
del
```
## requerimiento

```
El sistema deberá funcionar correctamente en los
navegadores web Google Chrome, Microsoft Edge y Brave
```
## en sus versiones actuales.

## Prioridad del requisito Alta

## Número de requisito RNF

## Nombre de requisito Arquitectura mantenible

## Categoría Mantenibilidad

## Tipo Requerimiento no funcional^

## Fuente del requisito Desarrollador

```
Descripción
del
```
## requerimiento

```
El sistema deberá desarrollarse utilizando una arquitectura
```
## modular que facilite el mantenimiento y futuras mejoras.

## Prioridad del requisito Alta

## Número de requisito RNF

## Nombre de requisito Control seguro de ejecución de código

## Categoría Seguridad

## Tipo Requerimiento no funcional^

## Fuente del requisito Desarrollador

```
Descripción
del
```
## requerimiento

```
El sistema deberá validar y controlar el código fuente
ingresado para reducir riesgos asociados a ejecuciones
```
## maliciosas o inseguras.

## Prioridad del requisito Alta

# 3 Modelado de Casos de Uso

## 3.1 Catálogo de Actores

```
Actor Tipo Descripción
```
```
Tester Humano Persona que ingresa el código fuente en el
sistema y revisa los resultados generados.
```
```
Sistema de
generación de
pruebas con IA
```
```
Sistema
externo
```
```
Componente que genera automáticamente
pruebas unitarias a partir del código
proporcionado.
```
```
Framework de
pruebas
```
```
Sistema
externo
```
```
Herramienta encargada de ejecutar las pruebas
unitarias generadas.
```

```
Documento de modelado técnico
Pág. 8
```
### 3.2 Diagrama de Casos de Uso


```
Documento de modelado técnico
Pág. 9
```
### 3.3 Especificación de Casos Clave


```
Documento de modelado técnico
Pág. 10
```
# 4 Módelo conceptual del dominio


```
Documento de modelado técnico
Pág. 11
```
# 5 Arquitectura tentativa

## 5.1 Diagrama de componentes


```
Documento de modelado técnico
Pág. 12
```
### 5.2 Diagrama de despliegue

### 5.3 Justificación Arquitectónica

El diseño modular que separa estrictamente la lógica de generación de la de evaluación.
Al desacoplar el Módulo de IA (GPT-4) del entorno de ejecución de pytest, el sistema
garantiza que cualquier inconsistencia en el código generado no comprometa la
estabilidad de la plataforma. La elección de un modelo de despliegue que utiliza un
Servidor Web (Nginx) como Reverse Proxy permite gestionar la carga de peticiones de
manera estructurada, garantizando que el sistema cumpla con el requisito de procesar y
evaluar las pruebas en un tiempo máximo de 60 segundos. Esta disposición asegura la
compatibilidad multiplataforma y protege la integridad del Servidor de Aplicaciones,
delegando el tráfico inicial a una capa de red segura que facilita la visualización de
resultados en la interfaz de usuario.


```
Documento de modelado técnico
Pág. 13
```
# 6 Proceso de negocio en BPMN 2.

