# Metodología del paquete

Este documento resume el método descrito en el manuscrito v6 y delimita lo que puede reproducirse con los archivos depositados. No añade nuevas búsquedas, decisiones humanas ni evaluaciones experimentales.

## Preguntas de investigación

| Código | Pregunta |
| --- | --- |
| RQ1 | ¿Qué recursos léxico-semánticos se han aplicado a la ingeniería de requisitos de software? |
| RQ2 | ¿Para qué tareas de ingeniería de requisitos se emplean? |
| RQ3 | ¿Qué proporción de los recursos identificados dispone de evidencia de soporte del español o de una adaptación, versión multilingüe o alternativa? |
| RQ4 | ¿Qué recursos y aplicaciones se han documentado específicamente para requisitos en español y qué cubren? |
| RQ5 | ¿Qué vacíos se observan en la intersección entre recursos léxico-semánticos, español y requisitos de software? |
| RQ6 | ¿Qué recursos y métodos son candidatos para transferirse al español y bajo qué condiciones? |

## Búsquedas declaradas

La fuente principal es OpenAlex. La documentación recibida sitúa la búsqueda principal el **15 de julio de 2026**. Esta fecha es una declaración de procedencia; el paquete no contiene una exportación original de la API que permita acreditar independientemente aquella ejecución. La búsqueda dirigida y el cierre de recuperación se documentan el **27 de septiembre de 2026**. La fecha de preparación del repositorio no debe confundirse con estas fechas.

Cadena principal declarada sobre `title_and_abstract.search`, punto de acceso `/works`:

```text
("requirements engineering" OR "software requirements" OR "requirements specification" OR "natural language requirements") AND ("WordNet" OR "word embedding" OR "semantic similarity" OR "ontology" OR "thesaurus" OR "lexical" OR "FrameNet" OR "knowledge graph" OR "word sense" OR "semantic role" OR "BERT" OR "language model" OR "semantic")
```

Ventana declarada: 2015-01-01 a 2026-12-31; tipos `article` o `book-chapter`; sin filtro de idioma, área ni acceso abierto en la recuperación. La fecha efectiva limita la cobertura de 2026. El tipo registrado por OpenAlex no acredita por sí solo revisión por pares.

Cadena dirigida declarada:

```text
("ingeniería de requisitos" OR "requisitos de software" OR "requisitos no funcionales" OR "especificación de requisitos" OR "Spanish requirements" OR "requirements in Spanish" OR "Spanish software requirements" OR "requisitos en español")
```

Los 11 registros adicionales de la ronda de kappa conforman un tercer flujo. No se suman al denominador principal de 533 estudios.

## Selección y extracción

Se requiere aplicación de NLP o aprendizaje automático a requisitos de software y uso o construcción de un recurso léxico-semántico. Las revisiones secundarias se usan como antecedentes, no como estudios primarios. Los motivos concretos se conservan por registro.

El archivo recibido registra decisiones asistidas por el procedimiento denominado `claude-sonnet-5`, con identificadores de consignas y pasadas. Se conservan esos nombres tal como fueron aportados, sin afirmar una verificación externa de la identidad del modelo. El paquete no incluye el texto íntegro de todas las consignas ni las respuestas originales de cada llamada, por lo que no reproduce la fase de extracción.

Los 539 incluidos tienen la siguiente base de decisión: 488 título y resumen, 36 solo título y 15 fragmentos o inicio del texto completo. Las comprobaciones de coincidencia textual son automáticas; la interpretación de la cita puede requerir revisión humana.

## Unidades y reglas de cómputo

1. **Estudio:** registro retenido tras la deduplicación; la posible relación residual entre publicaciones de un mismo estudio es una limitación.
2. **Recurso concreto:** modelo, producto o recurso léxico identificado; no se suman familias sin versión ni algoritmos genéricos a RQ3.
3. **Uso:** par único de estudio principal y recurso concreto aplicado, no solo mencionado.
4. **Familias:** un estudio puede emplear varias; se cuenta una vez por familia.
5. **Métricas y conjuntos:** se cuenta una vez por categoría canónica y estudio cuando existe la comprobación textual registrada.
6. **Español:** se utiliza la lengua de los datos; no se deduce del idioma del documento.

La «evidencia directa» de español incluye fuentes de fuerza distinta: recurso nativo, declaración del proveedor, resultado propio, evaluación agregada, evaluación de seguridad o presencia en entrenamiento. No equivale a eficacia demostrada en ingeniería de requisitos.

## Concordancia humana histórica

El manuscrito informa un ejercicio anterior de 18 pares: 16 inclusiones coincidentes, una exclusión coincidente y un desacuerdo, con acuerdo observado 17/18 y κ = 0,640. Este paquete de síntesis no incorpora las planillas originales de ese ejercicio y sus programas no recalculan κ. El resultado histórico no valida la selección global de 1.746 registros.
