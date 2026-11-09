# Redistribution review / Revisión de redistribución

## American English

**Open release gate.** This is a list of concrete unresolved checks, not a claim that redistribution is prohibited. Passing functional tests does not close this gate.

The official 4.23.1 ZIP contributes 1,064 JARs to the current package. Run `python3 scripts/inventory-jars.py build/package/opt/autopsy-gui build/jar-inventory.json` to record each JAR's SHA-256, embedded notices, Maven coordinates, and declared licenses. Metadata can be absent, incomplete, or describe a shaded dependency rather than the entire JAR. The output is evidence for review, not a full SBOM or license determination.

The two source archives currently shipped cover TSK and the private Temurin runtime. They do **not** cover all other bundled components. Before distributing the combined binary, resolve at least:

| Bundled component | Remaining check |
| --- | --- |
| JavaFX 17.0.14-ea2 | Identify exact corresponding OpenJFX sources and preserve GPLv2 + Classpath Exception notices, including native platform JARs. |
| JFreeChart 1.5.5 | Supply the LGPL-2.1-or-later license and matching corresponding source as required by the chosen redistribution method. |
| gst1-java-core 1.4.0 | Review LGPL-3.0 obligations and provide matching sources/notices. |
| SevenZipJBinding 9.20-2.00beta | Match the Java and bundled native components to sources and applicable LGPL/unRAR notices. |
| LICENSE4J runtime 4.7.3 | Record the applicable runtime redistribution terms; its presence in upstream's ZIP is not itself the license text. |
| Other bundled, nested, and shaded dependencies | Review the generated inventory, applicable license choices, notices and source requirements. |

Primary references: [Autopsy source](https://github.com/sleuthkit/autopsy/tree/autopsy-4.23.1), [OpenJFX](https://openjfx.io/), [JFreeChart](https://github.com/jfree/jfreechart), [LICENSE4J user guide](https://www.license4j.com/documents/LICENSE4J-License-Manager-User-Guide.pdf). Preserve upstream copyrights and distinguish integration authorship from original GUI authorship.

## Español latinoamericano

**Condición de publicación pendiente.** Esta lista identifica verificaciones concretas; no afirma que la redistribución esté prohibida. Aprobar las pruebas funcionales no resuelve estas condiciones.

El paquete contiene 1,064 JAR del ZIP oficial. `scripts/inventory-jars.py` registra hashes, avisos, coordenadas Maven y licencias declaradas. Los metadatos pueden faltar o referirse a dependencias incluidas dentro de otra biblioteca; el inventario no equivale a una auditoría completa.

Las fuentes entregadas de TSK y Temurin no cubren JavaFX, JFreeChart, gst1-java-core, SevenZipJBinding ni todos los componentes incluidos. Falta identificar y entregar las fuentes y avisos correspondientes según cada licencia, documentar los términos de redistribución de LICENSE4J y revisar las dependencias anidadas. La tabla anterior identifica las versiones encontradas. Conserva los créditos originales y atribuye a Jan Herrera la integración y el empaquetado Linux.
