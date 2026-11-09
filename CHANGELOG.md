# Changelog / Historial de cambios

## 4.23.1-2 — experimental

- Initialize Linux ingest profiles with the three Windows-only modules disabled; preserve existing preferences.
- Move Solr logs/PID files into the user profile and bind its HTTP listener to localhost.
- Restore execution permission for the bundled Linux artifact parser and account for its native dependencies.
- Handle the split PhotoRec package on newer distributions, including installs without Recommends.
- Add installation/lifecycle, RAW/NTFS/E01 recovery, GUI case/search/HTML-report tests for Ubuntu, Kali and Parrot.
- Document remaining redistribution review before binary publication.

### Español latinoamericano

- Perfiles nuevos con los tres módulos exclusivos de Windows desactivados; se conservan preferencias existentes.
- Registros y archivos de proceso de Solr en el perfil del usuario; acceso HTTP limitado a localhost.
- Permiso de ejecución del analizador auxiliar Linux y comprobación de sus dependencias.
- Dependencia de PhotoRec adaptada a distribuciones que lo separan de testdisk.
- Pruebas de instalación, actualización, recuperación e interfaz para Ubuntu, Kali y Parrot.
- Revisión de redistribución pendiente documentada antes de publicar binarios.

## 4.23.1-1 — experimental

### American English

- New independent Linux integration by Lupo-SysAdmin, based on the official Autopsy 4.23.1 ZIP.
- Native TSK/JNI 4.15.0 build, private Temurin 21 runtime, desktop entry and diagnostic launcher.
- Debian package assembly, pinned upstream hashes, source-release artifacts, and CI installation matrix.
- American English and Latin American Spanish documentation, upstream attribution, and explicit validation status.

### Español latinoamericano

- Nueva integración independiente de Linux por Lupo-SysAdmin, basada en el ZIP oficial de Autopsy 4.23.1.
- Compilación nativa de TSK/JNI 4.15.0, Java Temurin 21 privado, acceso al menú y lanzador con diagnóstico.
- Construcción del paquete Debian, hashes fijados, archivos de fuentes y matriz de instalación en CI.
- Documentación en inglés americano y español latinoamericano, créditos originales y estado explícito de las pruebas.
