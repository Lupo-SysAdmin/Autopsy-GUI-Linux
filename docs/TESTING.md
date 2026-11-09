# Test suite / Suite de pruebas

## American English

Run lifecycle tests **only in disposable containers**: they install and remove packages. On an amd64 Linux host with Docker, after building the DEB:

```bash
mkdir -p build/qa-results/ubuntu
docker run --name autopsy-qa-ubuntu --shm-size=1g \
  -v "$PWD:/src:ro" -v "$PWD/dist:/artifacts:ro" \
  -v "$PWD/build/qa-results/ubuntu:/results" \
  ubuntu:24.04 bash /src/tests/container-qa.sh
```

Repeat with distinct container/output names for `kalilinux/kali-rolling:latest` and `parrotsec/core:latest`. Save image digests, package hashes, `/results/lifecycle.log`, package inventories and GUI evidence. Containers use root for APT and a separate unprivileged account for Autopsy. Tests use only generated fixtures.

The suite validates clean install, legacy `/usr/bin/autopsy` coexistence, private JNI, exact recovery from RAW/ext4, RAW/NTFS and E01, persistent cases with spaces and accented characters, GUI case creation and ingest, keyword hit, HTML report contents, synthetic package upgrade, removal, purge, reinstall, and case preservation. The synthetic upgrade changes the Debian revision only; it does not prove migration between different upstream Autopsy database formats.

`GuiProbe.java` is a test-only Swing agent; it is never shipped in the application or loaded by the production launcher. It exercises UI controls and observes the component tree. Screenshots and actual report contents supplement its assertions. `gui-startup.sh` remains a smaller troubleshooting test.

Containers under Xvfb do not certify a complete distribution desktop, Wayland, GPU/video/face-detection modules, all evidence formats, large cases, or forensic correctness beyond the known fixtures. A passing GitHub Actions configuration is not evidence of a completed remote run. CI builds the DEB locally and uploads only QA evidence, not the binary, while the redistribution review is open. Public binary publication also requires closing [redistribution review](REDISTRIBUTION-REVIEW.md).

## Español latinoamericano

Ejecuta las pruebas **solo en contenedores desechables**: instalan y eliminan paquetes. El comando anterior usa Ubuntu; repítelo con nombres y carpetas diferentes para Kali y Parrot. Guarda los digests de imágenes, hashes del DEB, registros, inventario de paquetes y capturas. APT utiliza root; Autopsy se prueba con otro usuario sin privilegios y evidencias sintéticas.

La suite comprueba instalación, convivencia con Autopsy antiguo, JNI, recuperación exacta de EXT4/NTFS/E01, rutas con espacios y acentos, creación e ingestión desde la GUI, búsqueda, contenido del informe HTML, actualización sintética, eliminación, purga, reinstalación y conservación de casos. La actualización sintética cambia la revisión Debian: no demuestra migraciones entre versiones distintas de Autopsy.

El agente Swing se usa únicamente en pruebas. No se instala con la aplicación. Xvfb y contenedores no equivalen a validar escritorios completos, Wayland, GPU, módulos multimedia, todos los formatos ni casos grandes. Mientras la revisión está abierta, CI solo adjunta evidencias de pruebas, sin publicar el DEB. La publicación binaria también requiere cerrar la [revisión de redistribución](REDISTRIBUTION-REVIEW.md).
