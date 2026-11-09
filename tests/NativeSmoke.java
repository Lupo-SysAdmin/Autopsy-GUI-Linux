package org.sleuthkit.datamodel;

import java.nio.file.Files;
import java.nio.file.Path;

/** Exercises the real JNI ABI and SQLite case creation, not a mock. */
public final class NativeSmoke {
    public static void main(String[] args) throws Exception {
        String version = SleuthkitJNI.getVersion();
        if (!version.startsWith("4.15.0")) {
            throw new AssertionError("Unexpected TSK: " + version);
        }
        Path dir = Files.createTempDirectory("autopsy-native-smoke-");
        Path db = dir.resolve("case.db");
        try {
            SleuthkitCase created = SleuthkitCase.newCase(db.toString());
            if (args.length > 0) {
                var process = created.makeAddImageProcess("UTC", false, false, "");
                process.run("autopsy-gui-fixture", new String[]{args[0]});
                process.commit();
            }
            created.close();
            if (Files.size(db) == 0) throw new AssertionError("Empty case database");
            SleuthkitCase reopened = SleuthkitCase.openCase(db.toString());
            if (args.length > 0) {
                var matches = reopened.findFiles(reopened.getRootObjects().get(0), "evidence.txt");
                if (matches.size() != 1) throw new AssertionError("Expected one evidence.txt");
                byte[] expected = "Autopsy Linux fixture / Evidencia de prueba\n".getBytes(java.nio.charset.StandardCharsets.UTF_8);
                byte[] actual = new byte[expected.length];
                int read = matches.get(0).read(actual, 0, actual.length);
                if (read != expected.length || !java.util.Arrays.equals(actual, expected)) {
                    throw new AssertionError("Recovered evidence differs from fixture");
                }
                System.out.println("PASS: RAW/ext4 ingest and exact recovered file content");
            }
            reopened.close();
            System.out.println("PASS: TSK " + version + "; JNI create/reopen SQLite case");
        } finally {
            try (var paths = Files.list(dir)) {
                for (Path path : paths.toList()) Files.deleteIfExists(path);
            }
            Files.deleteIfExists(dir);
        }
    }
}
