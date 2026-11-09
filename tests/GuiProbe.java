import java.awt.*;
import java.awt.event.MouseEvent;
import java.lang.instrument.Instrumentation;
import java.nio.file.*;
import java.util.*;
import javax.swing.*;
import javax.swing.text.JTextComponent;

/** Test-only Swing driver. Never installed or injected by the production launcher. */
public final class GuiProbe {
    private static final Map<Integer, Component> controls = new HashMap<>();
    private static Path directory;
    public static void premain(String args, Instrumentation instrumentation) {
        directory = Path.of(args);
        Thread worker = new Thread(() -> {
            try {
                Files.createDirectories(directory);
                while (true) {
                    Path input = directory.resolve("command");
                    if (Files.exists(input)) {
                        String command = Files.readString(input);
                        Files.delete(input);
                        SwingUtilities.invokeLater(() -> { try { act(command); } catch (Throwable failure) { try { Files.writeString(directory.resolve("error"), failure.toString()); } catch (Exception ignored) { } } });
                    }
                    SwingUtilities.invokeAndWait(GuiProbe::dump);
                    Thread.sleep(1000);
                }
            } catch (Throwable failure) {
                try { Files.writeString(directory.resolve("error"), failure.toString()); }
                catch (Exception ignored) { }
            }
        }, "autopsy-qa-probe");
        worker.setDaemon(true);
        worker.start();
    }
    private static void act(String command) {
        String[] parts = command.replaceFirst("\\r?\\n$", "").split("\\t", 3);
        Component component = controls.get(Integer.parseInt(parts[1]));
        if (component == null || !component.isShowing()) throw new IllegalArgumentException("Control is not visible");
        switch (parts[0]) {
            case "click" -> {
                if (component instanceof AbstractButton button) button.doClick();
                else for (int event : new int[]{MouseEvent.MOUSE_PRESSED, MouseEvent.MOUSE_RELEASED, MouseEvent.MOUSE_CLICKED})
                    component.dispatchEvent(new MouseEvent(component, event, System.currentTimeMillis(), 0, component.getWidth()/2, component.getHeight()/2, 1, false, MouseEvent.BUTTON1));
            }
            case "mouse" -> { for (int event : new int[]{MouseEvent.MOUSE_PRESSED, MouseEvent.MOUSE_RELEASED, MouseEvent.MOUSE_CLICKED})
                component.dispatchEvent(new MouseEvent(component, event, System.currentTimeMillis(), 0, component.getWidth()/2, component.getHeight()/2, 1, false, MouseEvent.BUTTON1)); }
            case "text" -> ((JTextComponent) component).setText(new String(Base64.getDecoder().decode(parts[2]), java.nio.charset.StandardCharsets.UTF_8));
            case "combo" -> ((JComboBox<?>) component).setSelectedIndex(Integer.parseInt(parts[2]));
            case "list" -> ((JList<?>) component).setSelectedIndex(Integer.parseInt(parts[2]));
            case "table" -> { String[] cell = parts[2].split(","); ((JTable) component).setValueAt(Boolean.valueOf(cell[2]), Integer.parseInt(cell[0]), Integer.parseInt(cell[1])); }
            case "tree" -> ((JTree) component).setSelectionRow(Integer.parseInt(parts[2]));
            case "listclick" -> {
                JList<?> list = (JList<?>) component;
                Rectangle r = list.getCellBounds(Integer.parseInt(parts[2]), Integer.parseInt(parts[2]));
                for (int event : new int[]{MouseEvent.MOUSE_PRESSED, MouseEvent.MOUSE_RELEASED, MouseEvent.MOUSE_CLICKED})
                    list.dispatchEvent(new MouseEvent(list, event, System.currentTimeMillis(), 0, r.x + 8, r.y + r.height / 2, 1, false, MouseEvent.BUTTON1));
            }
            default -> throw new IllegalArgumentException("Unknown command");
        }
    }
    private static String quote(String value) {
        if (value == null) return "null";
        return "\"" + value.replace("\\", "\\\\").replace("\"", "\\\"").replace("\n", "\\n").replace("\r", "\\r").replace("\t", "\\t") + "\"";
    }
    private static void visit(Component c, int parent, java.util.List<String> output) {
        if (!c.isShowing()) return;
        int id = System.identityHashCode(c);
        controls.put(id, c);
        String text = c instanceof AbstractButton b ? b.getText() : c instanceof JLabel l ? l.getText()
            : c instanceof JTextComponent t ? t.getText() : c instanceof Frame f ? f.getTitle()
            : c instanceof Dialog d ? d.getTitle() : c.getName();
        String items = "[]";
        java.util.List<String> entries = new ArrayList<>();
        if (c instanceof JList<?> l) for (int i=0; i<l.getModel().getSize(); i++) entries.add(quote(String.valueOf(l.getModel().getElementAt(i))));
        if (c instanceof JComboBox<?> b) for (int i=0; i<b.getItemCount(); i++) entries.add(quote(String.valueOf(b.getItemAt(i))));
        if (c instanceof JTree t) for (int i=0; i<t.getRowCount(); i++) entries.add(quote(String.valueOf(t.getPathForRow(i))));
        if (c instanceof JTable t) for (int r=0; r<t.getRowCount(); r++) { java.util.List<String> cells = new ArrayList<>(); for (int col=0; col<t.getColumnCount(); col++) cells.add(String.valueOf(t.getValueAt(r,col))); entries.add(quote(String.join(" | ",cells))); }
        if (!entries.isEmpty()) items = "[" + String.join(",", entries) + "]";
        output.add("{\"id\":"+id+",\"parent\":"+parent+",\"class\":"+quote(c.getClass().getName())+",\"text\":"+quote(text)
            +",\"enabled\":"+c.isEnabled()+",\"selected\":"+(c instanceof AbstractButton b && b.isSelected())+",\"items\":"+items+"}");
        if (c instanceof Container container) for (Component child : container.getComponents()) visit(child, id, output);
    }
    private static void dump() {
        java.util.List<String> output = new ArrayList<>();
        controls.clear();
        for (Window window : Window.getWindows()) visit(window, 0, output);
        try {
            Path temp = directory.resolve("tree.tmp");
            Files.writeString(temp, "["+String.join(",", output)+"]\n");
            Files.move(temp, directory.resolve("tree.json"), StandardCopyOption.REPLACE_EXISTING);
        } catch (Exception failure) { throw new RuntimeException(failure); }
    }
}
