# Third-party software / Software de terceros

## American English

The repository's Apache-2.0 license applies to original Linux integration code, scripts, and documentation by Jan Herrera (Lupo-SysAdmin). It does not relicense bundled software or grant trademark rights.

| Component | Origin and licensing |
| --- | --- |
| Autopsy and its original GUI | [sleuthkit/autopsy](https://github.com/sleuthkit/autopsy), Apache-2.0; bundled libraries have their own licenses |
| The Sleuth Kit 4.15.0 | [Official source](https://github.com/sleuthkit/sleuthkit/releases/tag/sleuthkit-4.15.0); mixed licenses, including CPL/IBM, GPL and permissive notices; preserve the upstream `licenses/` directory |
| Eclipse Temurin 21 | [Official release](https://github.com/adoptium/temurin21-binaries/releases/tag/jdk-21.0.13%2B9); GPLv2 with Classpath Exception and third-party notices in `runtime/legal/` |
| NetBeans, JavaFX, Solr and other ZIP contents | Upstream licenses/notices and JAR metadata remain in the application payload; Apache-2.0 is not a blanket license for these contents |
| System libraries | Installed by APT; their distribution packages supply licensing and source information |

The build ships the TSK, Temurin, and additional third-party source archives beside the binary. Publish them with the integration source and SHA256SUMS. The redistribution record documents the review and evidence; it is not a legal certification of upstream's entire dependency tree.

No endorsement by Autopsy, Sleuth Kit Labs, Eclipse, Debian, Kali, Parrot or Ubuntu is implied. Do not describe Lupo-SysAdmin as the author of Autopsy's original interface or Linux support.

## Español latinoamericano

Apache-2.0 cubre el código original de integración, scripts y documentación de Jan Herrera (Lupo-SysAdmin). No cambia las licencias del software incluido ni concede derechos sobre marcas.

Autopsy utiliza Apache-2.0, pero sus bibliotecas conservan licencias propias. TSK incluye licencias mixtas: se conserva su directorio `licenses/`. Temurin/OpenJDK utiliza GPLv2 con Classpath Exception y avisos de terceros en `runtime/legal/`. NetBeans, JavaFX, Solr y los demás componentes conservan avisos y metadatos originales. APT administra las licencias y fuentes de las bibliotecas del sistema.

La construcción entrega las fuentes de TSK, Temurin y las bibliotecas adicionales junto al binario. Publica también las fuentes de integración y SHA256SUMS. El registro de redistribución documenta la revisión y sus evidencias; no constituye una certificación jurídica de todas las dependencias de upstream.

No se implica un aval de los proyectos originales ni de las distribuciones. Los créditos de Lupo-SysAdmin corresponden a la adaptación, integración y empaquetado Linux; la interfaz original conserva su autoría.

## Revision 4.23.1-3 / Revisión 4.23.1-3

Additional corresponding sources and notices are now supplied through `third-party-sources.lock.json` and the release's `autopsy-third-party-sources-4.23.1.tar.gz`. See the [component redistribution record](docs/REDISTRIBUTION-REVIEW.md) for exact versions, binary correspondence, license choices, and proprietary JAI/LICENSE4J terms. The original notices are retained; Apache-2.0 applies only to this project's original work. Never distribute the DEB release without its accompanying source assets.

Se entregan fuentes y avisos adicionales mediante `third-party-sources.lock.json` y el archivo `autopsy-third-party-sources-4.23.1.tar.gz` de la publicación. El [registro por componente](docs/REDISTRIBUTION-REVIEW.md) identifica versiones, correspondencia de binarios, opciones de licencia y términos propietarios de JAI/LICENSE4J. Apache-2.0 cubre únicamente el trabajo original de este proyecto. Publica siempre el DEB acompañado de sus archivos de fuentes.

The desktop icon uses the original Autopsy artwork from the official ZIP. PNG frames preserve its pixels and dimensions; see `licensing/autopsy-icon.json`. Original copyrights and trademark ownership remain with their owners.

El icono de escritorio utiliza el arte original de Autopsy del ZIP oficial. Los PNG conservan sus píxeles y dimensiones; consulta `licensing/autopsy-icon.json`. Se mantienen los derechos y las marcas de sus respectivos titulares.
