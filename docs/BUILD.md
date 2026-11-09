# Build and release / Construcción y publicación

## American English

Release-specific fixes: the 4.23.1 ZIP contains TSK classes with class-file major version 65 (Java 21), even though the upstream installation script says Java 17. This integration therefore bundles Java 21. The TSK 4.15.0 source tarball also omits `tsk/pool/tsk_lvm.hpp`; the unchanged header from the same official tag is provided in `packaging/upstream/` under its original CPL-1.0 license.

The TSK JAR is modified by adding `NATIVELIBS/amd64/linux/libtsk_jni.so` and a modification notice; upstream Java classes are retained. Its loader requires this embedded location. `LD_LIBRARY_PATH` resolves the private `libtsk.so` dependency. The launcher gives JNI a private cache directory. `etc/autopsy.conf` is adjusted to remove the Windows-relative JRE location and development profile name.

1. Review `versions.lock.json`. Upstream ZIP/source/runtime checksums are pinned from official release metadata. Update all compatible components together; never silently resolve `latest` during a build.
2. Build in `packaging/Dockerfile` (Ubuntu 24.04 amd64). `build-native.sh` compiles TSK and JNI; it uses the official ZIP's matching Java JAR to avoid an uncontrolled Maven dependency resolution.
3. `package.py` extracts the ZIP, removes standalone Windows binary extensions, installs private native libraries/runtime under `/opt/autopsy-gui`, and writes the desktop launcher. It retains upstream notices. Native dependencies are calculated with `dpkg-shlibdeps`. Inspect `build/shlibdeps.log`; private TSK/JVM libraries may lack distro metadata, but unresolved external libraries must be fixed.
4. Run package checks and the native test in `tests/NativeSmoke.java`. Test GUI startup and real ingest separately. There are no post-install downloads or package-manager calls from maintainer scripts.
5. Test clean installation, upgrade, removal, and coexistence with legacy Autopsy on each target distribution. Dependency ABI differences may require separate builds. Do not label an untested OS supported.
6. Publish a prerelease only after reviewing validation and third-party redistribution obligations. Upload all `dist/` files, including sources. Attach build logs, dependency inventory, checksums, and the release commit. Signing releases is recommended; hashes alone are not signatures.

GitHub Actions builds on manual dispatch and pushes to `main`; it uploads workflow artifacts and does not publish a release or push changes. Native dependencies come from the builder's distro. Build source is repeatable, but OS dependencies/container tags are not immutable snapshots.

## Español latinoamericano

Correcciones específicas: el ZIP 4.23.1 contiene clases TSK con versión de bytecode 65 (Java 21), aunque el instalador de upstream indica Java 17. Por eso esta integración incluye Java 21. Las fuentes comprimidas de TSK 4.15.0 también omiten `tsk/pool/tsk_lvm.hpp`; se incluye el encabezado sin cambios del mismo tag oficial en `packaging/upstream/`, con su licencia CPL-1.0 original.

Se agrega `NATIVELIBS/amd64/linux/libtsk_jni.so` al JAR de TSK junto con un aviso de modificación, conservando las clases Java originales. Su cargador exige esa ubicación interna. `LD_LIBRARY_PATH` resuelve `libtsk.so` privado y el lanzador asigna una caché privada para JNI. También se ajusta `etc/autopsy.conf` para retirar la ruta relativa del Java de Windows y el nombre del perfil de desarrollo.

1. Revisa `versions.lock.json`. Los hashes provienen de metadatos oficiales. Actualiza Autopsy, TSK y Java de manera coordinada; no resuelvas `latest` durante la construcción.
2. Construye con `packaging/Dockerfile`, basado en Ubuntu 24.04 amd64. Se compilan TSK/JNI y se utiliza el JAR correspondiente del ZIP, evitando descargar dependencias Maven sin control.
3. `package.py` retira binarios Windows independientes, coloca bibliotecas y Java privados en `/opt/autopsy-gui`, conserva avisos e instala el lanzador. Calcula dependencias con `dpkg-shlibdeps`. Revisa `build/shlibdeps.log`: las bibliotecas privadas pueden carecer de metadatos Debian, pero las dependencias externas faltantes deben resolverse.
4. Ejecuta los controles del paquete y `tests/NativeSmoke.java`. Prueba apertura gráfica e ingestión por separado. No se descarga ni compila software durante la instalación del paquete.
5. Verifica instalación limpia, actualización, desinstalación y convivencia con Autopsy antiguo en cada distribución. Diferencias de ABI pueden requerir compilaciones separadas. No declares compatible un sistema sin probarlo.
6. Publica una versión preliminar solo después de revisar las pruebas y obligaciones de redistribución. Adjunta todos los archivos de `dist/`, fuentes incluidas, además de logs, inventario de dependencias, hashes y commit. Los hashes no sustituyen una firma.

GitHub Actions construye manualmente o al hacer push a `main`. Entrega artefactos, sin publicar releases ni modificar el repositorio. Los repositorios del sistema y la etiqueta del contenedor no son snapshots inmutables.
