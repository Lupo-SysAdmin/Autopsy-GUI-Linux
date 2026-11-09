import java.io.ByteArrayOutputStream;
import java.io.RandomAccessFile;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import net.sf.sevenzipjbinding.*;
import net.sf.sevenzipjbinding.impl.RandomAccessFileInStream;

/** Test the installed JNI under the packaged Java 21 runtime, without upstream test hooks. */
public class ArchiveSmoke {
    public static void main(String[] args) throws Exception {
        for (String path : args) {
            try (RandomAccessFile file = new RandomAccessFile(path, "r")) {
                IInArchive archive = SevenZip.openInArchive(null, new RandomAccessFileInStream(file));
                try {
                    if (archive.getNumberOfItems() != 1) throw new AssertionError(path);
                    // This Sleuth Kit fork exposes original name bytes for charset detection.
                    Object raw = archive.getProperty(0, PropID.PATH);
                    String name = raw instanceof byte[] ? new String((byte[]) raw, StandardCharsets.UTF_8) : raw.toString();
                    if (!name.equals("evidencia á.txt")) throw new AssertionError("Filename: " + name);
                    ByteArrayOutputStream data = new ByteArrayOutputStream();
                    ExtractOperationResult result = archive.extractSlow(0, bytes -> {
                        data.write(bytes, 0, bytes.length);
                        return bytes.length;
                    }, "test-password");
                    if (result != ExtractOperationResult.OK || !Arrays.equals(data.toByteArray(),
                            "Autopsy archive fixture á\n".getBytes(StandardCharsets.UTF_8))) {
                        throw new AssertionError("Extraction mismatch: " + path + " / " + result);
                    }
                    System.out.println("PASS archive: " + path);
                } finally { archive.close(); }
            }
        }
    }
}
