# Third-party software / Software de terceros

## American English

The repository's Apache-2.0 license applies to original Linux integration code, scripts, icon, and documentation by Jan Herrera (Lupo-SysAdmin). It does not relicense bundled software or grant trademark rights.

| Component | Origin and licensing |
| --- | --- |
| Autopsy and its original GUI | [sleuthkit/autopsy](https://github.com/sleuthkit/autopsy), Apache-2.0; bundled libraries have their own licenses |
| The Sleuth Kit 4.15.0 | [Official source](https://github.com/sleuthkit/sleuthkit/releases/tag/sleuthkit-4.15.0); mixed licenses, including CPL/IBM, GPL and permissive notices; preserve the upstream `licenses/` directory |
| Eclipse Temurin 21 | [Official release](https://github.com/adoptium/temurin21-binaries/releases/tag/jdk-21.0.13%2B9); GPLv2 with Classpath Exception and third-party notices in `runtime/legal/` |
| NetBeans, JavaFX, Solr and other ZIP contents | Upstream licenses/notices and JAR metadata remain in the application payload; Apache-2.0 is not a blanket license for these contents |
| System libraries | Installed by APT; their distribution packages supply licensing and source information |

The build ships the exact downloaded TSK source archive and Temurin source archive beside the binary. Publish these files, the integration source at the release tag, and SHA256SUMS together. Keep upstream notices intact. Before public redistribution, review the full bundled-component inventory and any corresponding-source obligations, including components inherited from the Autopsy ZIP; the two source archives are not a complete source inventory for every bundled JAR. This initial project is not a completed legal audit of upstream's entire dependency tree.

No endorsement by Autopsy, Sleuth Kit Labs, Eclipse, Debian, Kali, Parrot or Ubuntu is implied. Do not describe Lupo-SysAdmin as the author of Autopsy's original interface or Linux support.

## Español latinoamericano

Apache-2.0 cubre el código original de integración, scripts, icono y documentación de Jan Herrera (Lupo-SysAdmin). No cambia las licencias del software incluido ni concede derechos sobre marcas.

Autopsy utiliza Apache-2.0, pero sus bibliotecas conservan licencias propias. TSK incluye licencias mixtas: se conserva su directorio `licenses/`. Temurin/OpenJDK utiliza GPLv2 con Classpath Exception y avisos de terceros en `runtime/legal/`. NetBeans, JavaFX, Solr y los demás componentes conservan avisos y metadatos originales. APT administra las licencias y fuentes de las bibliotecas del sistema.

La construcción entrega los archivos exactos de código fuente de TSK y Temurin junto al binario. Publica también el código de integración correspondiente al tag y SHA256SUMS. Antes de redistribuir públicamente, revisa el inventario completo y las obligaciones de proporcionar fuentes, incluidos los componentes heredados del ZIP. Los dos archivos de fuentes no representan todas las fuentes de cada JAR. Esta primera versión no constituye una auditoría legal completa de todas las dependencias de upstream.

No se implica un aval de los proyectos originales ni de las distribuciones. Los créditos de Lupo-SysAdmin corresponden a la adaptación, integración y empaquetado Linux; la interfaz original conserva su autoría.
