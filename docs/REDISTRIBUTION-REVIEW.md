# Redistribution record / Registro de redistribución

## American English

This record describes the redistribution materials assembled for revision 4.23.1-3. It is a component-specific engineering review, not a certification of upstream's entire dependency tree. The original notices remain in the application. Additional notices and evidence are installed in `/usr/share/doc/autopsy-gui/licensing`; embedded JAR notices are also collected in `embedded-notices.tar.gz`.

| Component | Sources, notices, and disposition |
| --- | --- |
| TSK 4.15.0 | Exact release source plus the missing, unchanged upstream LVM header; CPL/GPL/permissive notices retained. Linux JNI is rebuilt; the modification is recorded inside its JAR. |
| Temurin 21.0.13+9 | Publisher's corresponding source archive, GPLv2 + Classpath Exception, and private runtime `legal/` notices. |
| JavaFX 17.0.14-ea+2 | Complete OpenJFX 17.0.14+2 source at `dd3c3615967fff280a427ea4304fba9b6502b9be`, including native sources/build scripts and third-party notices. The differently spelled ZIP version is recorded in binary evidence. |
| JFreeChart 1.5.5; gst1-java-core 1.4.0 | Exact published binary matches; complete tagged source trees/build files, LGPL-2.1-or-later and LGPL-3.0-only respectively. |
| SevenZipJBinding | Sleuth Kit fork `f308cd8f663cc3c013bfb14ec9cfc3ecc75c23f3`, including p7zip sources/build system and LGPL/unRAR notices. All 76 rebuilt API classes match the official Autopsy JAR byte for byte. The packaged native JAR is rebuilt for Linux amd64; its filename remains `sevenzipjbinding-AllPlatforms.jar` for upstream classpath compatibility. It contains only Linux amd64. No upstream source changes are applied; GCC uses `-std=gnu++98`. |
| LICENSE4J 4.7.3 | Unmodified publisher runtime. Its POM identifies the runtime as a distributable library under the [publisher EULA](https://www.license4j.com/EULA.txt), reproduced in `licensing/license4j-eula.txt`. It is proprietary and is not relicensed under Apache-2.0. |
| JAI 1.1.3 / JAI ImageIO 1.1 | Original Sun binary redistribution terms and third-party notices. Complete publisher redistributables are included under `doc/autopsy-gui/vendor/`; `jai_codec` accompanies `jai_core`. These archives are part of this application, not separately licensed by this project. Optional native ImageIO binaries in the vendor archive are not activated by installation. |
| c3p0 0.12.0; mchange-commons-java 0.4.0; JXMapViewer2 2.8 | Complete tagged sources and original LGPL/EPL notices; LGPL library replacement remains possible. |
| NetBeans compiler, Jemmy, Equinox | Publisher source artifact for nb-javac 18.0.1+10 includes compiler/API sources and Ant build files. Jemmy 2.3.1.1 source ZIP and CDDL notice. Equinox source at `bfbb93ac8958a72b912beb586576eb3be96bf229`, plus NetBeans 15's patch and rebuild script. All four binary identities match the NetBeans external-artifact checksums. |
| JUnit 3.8.2 / 4.10 / 4.13.2 / 5.6.0 | Complete versioned source trees, build files, and original CPL/EPL notices. |
| Smaller CDDL/EPL/MPL/LGPL dependencies | Publisher source JARs and build POMs/parent POMs are included for Jakarta/Javax APIs, JHighlight, character detection, CORBA, and JNR POSIX. Jython 2.7.4's complete source/build tree supplies the shading instructions for embedded JNR; relocated classes do not have the standalone JAR's hash. |

`third-party-sources.lock.json` records every archive URL and SHA-256. `scripts/bundle-third-party.py` verifies downloads and builds `autopsy-third-party-sources-4.23.1.tar.gz`. Publish that archive **with** the binary, the TSK and Temurin sources, integration sources, and `SHA256SUMS`. A URL in this document alone is not a substitute for the release source assets.

For dependencies explicitly offered under alternative licenses, this distribution uses the permissive option where available (for example Apache-2.0 for JNA, Jetty and Jericho, and EDL for JTS). Original alternative-license notices are retained. Maven metadata is supporting evidence, not a blanket license: shaded libraries and components without Maven coordinates are also considered above. NetBeans notice files include upstream reference material for components that may not be installed; their presence does not imply that every such component is included.

The integration imposes no additional restriction on modifying/replacing LGPL libraries, relinking against modified versions, or reverse engineering to debug those modifications. Libraries remain separate JARs/shared objects. Third-party licenses govern their respective components, including the proprietary runtime libraries. No trademark endorsement is claimed.

## Español latinoamericano

Este registro describe los materiales de redistribución reunidos para la revisión 4.23.1-3. Es una revisión técnica por componente; no certifica todas las dependencias de upstream. Los avisos originales permanecen en la aplicación. Los avisos adicionales se instalan en `/usr/share/doc/autopsy-gui/licensing`; `embedded-notices.tar.gz` reúne también los avisos internos de los JAR.

Se incluyen las fuentes originales de TSK y Temurin; el árbol completo de OpenJFX; las fuentes y archivos de construcción de JFreeChart, GStreamer Java, c3p0, mchange, JXMapViewer, JUnit y Jython; las fuentes publicadas de las API CDDL/EPL/MPL/LGPL; y las fuentes de nb-javac, Jemmy y Equinox con el parche y procedimiento de NetBeans. Los hashes y las URLs exactas están en `third-party-sources.lock.json`. La tabla anterior identifica las versiones y el tratamiento aplicado a cada componente.

SevenZip se reconstruye desde el fork de Sleuth Kit `f308cd8`. Sus 76 clases Java coinciden byte por byte con las oficiales. El archivo nativo conserva el nombre `sevenzipjbinding-AllPlatforms.jar` por compatibilidad con el classpath, pero incluye solo Linux amd64. Se conservan las fuentes de p7zip y los avisos LGPL/unRAR. La compilación utiliza C++98 sin modificar esas fuentes.

LICENSE4J conserva su licencia propietaria: su POM remite al EULA del editor, reproducido íntegramente en `licensing/license4j-eula.txt`. JAI y JAI ImageIO conservan los términos binarios de Sun; se entregan los redistribuibles originales completos y `jai_codec` junto a `jai_core`. Los archivos del proveedor forman parte de esta aplicación y no cambian a Apache-2.0. Instalar el paquete no activa los binarios nativos opcionales del archivo de ImageIO.

Publica `autopsy-third-party-sources-4.23.1.tar.gz` junto con el `.deb`, las fuentes de TSK/Temurin, las fuentes de integración y `SHA256SUMS`. El script verifica cada descarga; los enlaces no sustituyen los archivos de fuentes de la publicación. En bibliotecas con alternativas expresas se utiliza la opción permisiva disponible, conservando también los avisos originales. El árbol de Jython proporciona las instrucciones de reubicación de sus clases JNR incorporadas; esas clases no tienen el mismo hash que el JAR independiente.

Esta integración no agrega restricciones a modificar o sustituir bibliotecas LGPL, reenlazar con versiones modificadas ni realizar ingeniería inversa para depurar esas modificaciones. Las bibliotecas se mantienen separadas. Cada componente conserva su licencia; no se otorga un aval de las marcas originales.
