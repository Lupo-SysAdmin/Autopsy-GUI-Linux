# Validation / Validación

## 4.23.1-3 — validated core workflow / Flujo principal validado

**American English.** All three disposable distributions passed the complete suite again on November 9, 2026 UTC, including the new ZIP, encrypted ZIP, and encrypted 7z tests under the private Java 21 runtime. SevenZip also passed all 17 upstream test groups, serially. [Results and candidate package hash](qa/2026-11-09-rev3.json), [logs and package inventories](qa/2026-11-09-rev3.logs.tar.gz), and the [tested runtime manifest](qa/4.23.1-3-tested-runtime.json) identify the evidence. The final packaging adds documentation/notices; application/runtime contents, permissions, and symlink targets are checked against that manifest. The TSK JAR is compared member by member because adding the JNI changes ZIP timestamps between builds; its classes, native code, notices and member list are identical. Only `build-info.json` build metadata is excluded. Source/notice materials are documented in the [redistribution record](REDISTRIBUTION-REVIEW.md).

Stable scope means the tested amd64 case/ingest/search/report and package lifecycle workflow. It does not mean every optional module or evidence format is supported. Container GUI tests use Xvfb; complete distro desktops, native Wayland, large cases, and upstream database-version migrations remain outside that matrix. Remote Actions and host installation are separate checks; consult the release notes for their final outcomes.

**Español latinoamericano.** Las tres distribuciones desechables aprobaron nuevamente toda la suite el 9 de noviembre de 2026 UTC, incluidas las nuevas pruebas ZIP, ZIP cifrado y 7z cifrado con Java 21 privado. SevenZip aprobó sus 17 grupos de pruebas ejecutados secuencialmente. Los enlaces anteriores identifican resultados, hash del paquete candidato, registros, paquetes y manifiesto de archivos probados. El empaquetado final agrega documentación y avisos; se verifican contenidos de ejecución, permisos y destinos de enlaces. El JAR de TSK se compara entrada por entrada: cambian las fechas del contenedor ZIP al agregar JNI, pero sus clases, código nativo, avisos y lista de entradas son idénticos. Solo se excluyen los metadatos de `build-info.json`.

El alcance estable es el flujo amd64 probado de casos, ingestión, búsqueda, informes y ciclo de instalación. No implica que todos los módulos o formatos funcionen. Las pruebas gráficas usan Xvfb; escritorios completos, Wayland nativo, casos grandes y migraciones entre versiones de la base de datos quedan fuera de esa matriz. Las notas de la release registran por separado los resultados finales de Actions y la instalación en el host.

## Earlier validation / Validación anterior

## American English

Test session: November 8, 2026 (America/New_York), November 9 UTC. The earlier revisions below were experimental; revision 3 results are recorded first.

Revision `4.23.1-1`, SHA-256 `a9f107bc7065519c3ff4d3c9bb45463a68f73f4584e7acda7393c67e128ac307`, passed clean APT installation, private JNI, exact EXT4/NTFS/E01 recovery, case reopening, GUI startup, legacy-command coexistence, a synthetic revision upgrade, removal, purge, reinstall, and case preservation on all three official container images:

| Platform | Image digest |
| --- | --- |
| Ubuntu 24.04.5 | `sha256:fe81560990fae86dc4743202b2cb4d3df98d0bcf949173cecef15ce1127ef852` |
| Kali Rolling 2026.3 | `sha256:6ec743d9fc5cd397451eeddeff3869bcfab5de9bd5dec5b1f34cbfbd80313073` |
| Parrot Security 7.4 | `sha256:2dcefa48d3c4ae6b1a1a1391ae2a0ae6115a3c194b3677b3f0487f0e3996c9cd` |

The deeper GUI tests then found four packaging issues addressed in revision `4.23.1-2`:

1. Windows-only aLEAPP, iLEAPP and YARA enabled by default cancelled ingest. New Linux profiles disable them; existing preferences are preserved.
2. Solr attempted to create logs/PID files below root-owned `/opt`. The launcher now uses writable per-user paths and binds HTTP to localhost.
3. The bundled Linux artifact parser lacked executable permission. Packaging restores it and includes its native dependency check.
4. Newer Debian/Kali packages split PhotoRec out of `testdisk`. The dependency now requires `photorec` or a pre-split `testdisk (<< 7.2-1~)`, including installations with Recommends disabled.

The installed GUI regression checks creation of a case with spaces/accents, default ingest plus Keyword Search, the exact expected `evidence.txt` search hit and its contents in the generated HTML report. The final DEB `4.23.1-2` passed the entire suite on all three systems with exit code 0. Its SHA-256 is `440c828dc8d25773fbcdd7c9a07a4979bb3632c1149300b1dc78a2488f49bafe`. See the [machine-readable result](qa/2026-11-09.json) and [logs and package inventories](qa/2026-11-09.logs.tar.gz). See [reproduction instructions](TESTING.md).

These were real root-owned DEB installations, with the application run as an unprivileged account under Xvfb, in disposable containers inside a KVM Ubuntu VM. Host packages were not changed. This replaces the earlier rootless Ubuntu bootstrap attempt, which was not valid clean-install evidence. It does not certify complete distro desktops, Wayland, large cases, all modules, or forensic accuracy beyond the fixtures. The upgrade test changes the Debian revision, not the upstream database format. No production evidence was used.

Known upstream limitations include Windows-only modules, portions of Recent Activity, and missing OpenCV 2.4.13 native face detection. Optional multimedia/OCR modules have not been comprehensively tested. The startup log contains JavaFX/logging/GTK warnings; a successful main window alone is not evidence that every feature works. Remote CI results must be checked after upload; local tests do not imply a GitHub Actions run occurred.

## Español latinoamericano

Sesión del 8 de noviembre de 2026 (Nueva York), 9 de noviembre UTC. Las revisiones anteriores eran experimentales; los resultados de la revisión 3 aparecen al inicio.

La revisión `4.23.1-1`, identificada por el hash anterior, aprobó instalación APT real, JNI, recuperación exacta de EXT4/NTFS/E01, reapertura de casos, arranque gráfico, convivencia con Autopsy antiguo, actualización sintética, eliminación, purga, reinstalación y conservación de casos en Ubuntu 24.04.5, Kali 2026.3 y Parrot 7.4. La tabla identifica las imágenes exactas.

Las pruebas completas de interfaz encontraron cuatro problemas corregidos en `4.23.1-2`: módulos exclusivos de Windows activados inicialmente, rutas de Solr sin permiso de escritura, un auxiliar Linux sin permiso de ejecución y la separación de PhotoRec del paquete `testdisk` en distribuciones nuevas. Los perfiles nuevos desactivan los tres módulos incompatibles; los perfiles existentes no se sobrescriben.

La regresión gráfica crea un caso con espacios y acentos, ejecuta ingestión y búsqueda, exige encontrar `evidence.txt` y comprueba su presencia en el informe HTML. El DEB final `4.23.1-2` aprobó la suite completa en los tres sistemas, con código de salida 0. El hash SHA-256 aparece arriba. Se incluyen el [resultado verificable](qa/2026-11-09.json) y los [registros e inventarios](qa/2026-11-09.logs.tar.gz). Consulta [cómo reproducir las pruebas](TESTING.md).

Se utilizaron instalaciones del DEB propiedad de root y un usuario sin privilegios para la aplicación, con Xvfb, en contenedores desechables dentro de una VM KVM Ubuntu. No se cambiaron los paquetes del host. Esto reemplaza el intento anterior de Ubuntu mediante espacios de nombres, que no validaba una instalación limpia. No certifica escritorios completos, Wayland, casos grandes, todos los módulos ni exactitud forense más allá de las evidencias sintéticas. La actualización probada cambia la revisión Debian, no el formato de base de datos de Autopsy.

Persisten limitaciones de upstream: módulos Windows, partes de Recent Activity y detección de rostros sin OpenCV nativo. Los módulos multimedia/OCR no están validados exhaustivamente. Los avisos de JavaFX/logging/GTK no se interpretan como paridad funcional. Las pruebas locales tampoco equivalen a una ejecución de GitHub Actions.

## Screenshots / Capturas

| System / Sistema | Keyword search / Búsqueda | HTML report / Informe |
| --- | --- | --- |
| Ubuntu | [PNG](screenshots/ubuntu-4.23.1-2-keyword.png) | [PNG](screenshots/ubuntu-4.23.1-2-report.png) |
| Kali | [PNG](screenshots/kali-4.23.1-2-keyword.png) | [PNG](screenshots/kali-4.23.1-2-report.png) |
| Parrot | [PNG](screenshots/parrot-4.23.1-2-keyword.png) | [PNG](screenshots/parrot-4.23.1-2-report.png) |
