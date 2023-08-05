import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.HashMap;
import java.util.Map;

public class VentanaConversor extends JFrame {

    private JTextField decimalField;
    private JComboBox<String> categoriaComboBox;
    private JComboBox<String> monedaComboBox;
    private JButton convertirButton;
    private JButton invertirButton; // Nuevo botón para inversión
    private JLabel resultadoLabel;

    private Map<String, Map<String, Double>> monedaValues;

    public VentanaConversor() {
        setTitle("Conversor de Monedas");
        setSize(800, 500);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setLocationRelativeTo(null);

        JPanel panel = new JPanel();
        panel.setBackground(Color.GRAY);
        panel.setLayout(new GridBagLayout());
        this.getContentPane().add(panel);

        GridBagConstraints gbc = new GridBagConstraints();
        gbc.insets = new Insets(5, 10, 5, 10);
        gbc.anchor = GridBagConstraints.WEST;

        JLabel bienvenidaLabel = new JLabel("Bienvenido al Conversor de Monedas");
        bienvenidaLabel.setFont(new Font("Arial", Font.BOLD, 24));
        gbc.gridx = 0;
        gbc.gridy = 0;
        gbc.gridwidth = 2;
        gbc.anchor = GridBagConstraints.CENTER;
        panel.add(bienvenidaLabel, gbc);

        decimalField = new JTextField(10);
        categoriaComboBox = new JComboBox<>();
        monedaComboBox = new JComboBox<>();
        convertirButton = new JButton("Convertir");
        invertirButton = new JButton("Invertir"); // Nuevo botón
        resultadoLabel = new JLabel("La conversión ha sido de: ");

        gbc.gridx = 0;
        gbc.gridy = 1;
        gbc.gridwidth = 1;
        panel.add(new JLabel("Dato Decimal:"), gbc);
        gbc.gridx = 1;
        panel.add(decimalField, gbc);

        gbc.gridy = 2;
        gbc.gridx = 0;
        panel.add(new JLabel("Seleccionar Categoría:"), gbc);
        gbc.gridx = 1;
        panel.add(categoriaComboBox, gbc);

        gbc.gridy = 3;
        gbc.gridx = 0;
        panel.add(new JLabel("Seleccionar Moneda:"), gbc);
        gbc.gridx = 1;
        panel.add(monedaComboBox, gbc);

        gbc.gridy = 4;
        gbc.gridx = 0;
        gbc.gridwidth = 1;
        panel.add(convertirButton, gbc);
        gbc.gridx = 1;
        panel.add(invertirButton, gbc); // Agregar el nuevo botón

        gbc.gridy = 5;
        gbc.gridx = 0;
        gbc.gridwidth = 2;
        panel.add(resultadoLabel, gbc);

        monedaValues = new HashMap<>();
        llenarOpciones();

        convertirButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                double datoDecimal = Double.parseDouble(decimalField.getText());
                String selectedCategoria = (String) categoriaComboBox.getSelectedItem();
                String selectedMoneda = (String) monedaComboBox.getSelectedItem();
                double conversionRate = monedaValues.get(selectedCategoria).get(selectedMoneda);
                double convertedValue = datoDecimal * conversionRate;
                String conversion = "La conversión ha sido de: " + convertedValue;
                resultadoLabel.setText(conversion);

                System.out.println("Categoría seleccionada: " + selectedCategoria);
                System.out.println("Moneda seleccionada: " + selectedMoneda);
                System.out.println("Valor de conversión: " + conversionRate);
            }
        });

        invertirButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                double datoDecimal = Double.parseDouble(decimalField.getText());
                String selectedCategoria = (String) categoriaComboBox.getSelectedItem();
                String selectedMoneda = (String) monedaComboBox.getSelectedItem();
                double conversionRate = monedaValues.get(selectedCategoria).get(selectedMoneda);
                double invertedValue = datoDecimal / conversionRate;
                String inversion = "La inversión ha sido de: " + invertedValue;
                resultadoLabel.setText(inversion);

                System.out.println("Categoría seleccionada: " + selectedCategoria);
                System.out.println("Moneda seleccionada: " + selectedMoneda);
                System.out.println("Valor de inversión: " + invertedValue);
            }
        });
    }

    private void llenarOpciones() {
        try {
            String url = "http://127.0.0.1:5000/data"; // Reemplaza con la URL correcta
            HttpURLConnection connection = (HttpURLConnection) new URL(url).openConnection();
            connection.setRequestMethod("GET");

            int responseCode = connection.getResponseCode();
            if (responseCode == HttpURLConnection.HTTP_OK) {
                BufferedReader reader = new BufferedReader(new InputStreamReader(connection.getInputStream()));
                StringBuilder response = new StringBuilder();
                String line;
                while ((line = reader.readLine()) != null) {
                    response.append(line);
                }
                reader.close();

                JSONObject jsonObject = new JSONObject(response.toString());
                JSONArray categoriasArray = jsonObject.names(); // Obtener los nombres de las categorías

                for (int i = 0; i < categoriasArray.length(); i++) {
                    String categoria = categoriasArray.getString(i);
                    categoriaComboBox.addItem(categoria); // Agregar las categorías a la JComboBox

                    JSONArray monedaArray = jsonObject.getJSONArray(categoria);
                    Map<String, Double> monedaMap = new HashMap<>();
                    for (int j = 0; j < monedaArray.length(); j++) {
                        JSONObject countryData = monedaArray.getJSONObject(j);
                        for (String country : countryData.keySet()) {
                            double value = countryData.getDouble(country); // Obtener el valor numérico del país
                            monedaMap.put(country, value); // Guardar el valor en el mapa
                            // Agregar las opciones de moneda a la JComboBox correspondiente
                            monedaComboBox.addItem(country);
                        }
                    }
                    monedaValues.put(categoria, monedaMap); // Guardar el mapa en monedaValues
                }
            } else {
                System.out.println("Error en la solicitud HTTP. Código de respuesta: " + responseCode);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(new Runnable() {
            @Override
            public void run() {
                VentanaConversor app = new VentanaConversor();
                app.setVisible(true);
            }
        });
    }
}
