package auction;

import javax.swing.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class SellerGUI {
    private JTextField userIdField;
    private JTextField itemNameField;
    private JTextField itemDescField;
    private JTextField baseBidField;
    private JTextField bidTimeField;

    public SellerGUI() {
        JFrame frame = new JFrame("Auction Seller");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(400, 300);

        JPanel panel = new JPanel();
        panel.setLayout(new BoxLayout(panel, BoxLayout.Y_AXIS));

        userIdField = new JTextField(20);
        itemNameField = new JTextField(20);
        itemDescField = new JTextField(20);
        baseBidField = new JTextField(20);
        bidTimeField = new JTextField(20);

        JButton submitButton = new JButton("Submit");
        submitButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                // Handle submit button click event
                insertItemToDatabase();
            }
        });

        panel.add(new JLabel("Enter the user ID: "));
        panel.add(userIdField);
        panel.add(new JLabel("Enter the item name: "));
        panel.add(itemNameField);
        panel.add(new JLabel("Enter item description: "));
        panel.add(itemDescField);
        panel.add(new JLabel("Enter the base bid amount: "));
        panel.add(baseBidField);
        panel.add(new JLabel("Enter the time period of the bid (in days): "));
        panel.add(bidTimeField);
        panel.add(submitButton);

        frame.getContentPane().add(panel);
        frame.setVisible(true);
    }

    private void insertItemToDatabase() {
        try (Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/seller_details", "root", "123456789")) {
            String query = "INSERT INTO new_table (user_id, item_name, item_des, base_price, time_period) VALUES (?, ?, ?, ?, ?)";
            try (PreparedStatement pstm = con.prepareStatement(query)) {
                pstm.setString(1, userIdField.getText());
                pstm.setString(2, itemNameField.getText());
                pstm.setString(3, itemDescField.getText());
                pstm.setInt(4, Integer.parseInt(baseBidField.getText()));
                pstm.setLong(5, Long.parseLong(bidTimeField.getText()));
                pstm.executeUpdate();
                JOptionPane.showMessageDialog(null, "The item has been added to the database.");
            } catch (SQLException ex) {
                ex.printStackTrace();
                JOptionPane.showMessageDialog(null, "Error occurred while adding item to the database.");
            }
        } catch (SQLException ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(null, "Error occurred while connecting to the database.");
        }
    }

    public static void monitor(String userId) {
        try (Connection connection = DriverManager.getConnection("jdbc:mysql://localhost:3306/seller_details", "root", "123456789")) {
            String sql = "SELECT * FROM buyer_details WHERE item_id = ?";
            try (PreparedStatement preparedStatement = connection.prepareStatement(sql)) {
                preparedStatement.setString(1, userId);
                ResultSet resultSet = preparedStatement.executeQuery();

                if (resultSet.next()) {
                    // Item found, display its details
                    String itemId = resultSet.getString("item_id");
                    String buyerUserId = resultSet.getString("user_id");
                    String buyerName = resultSet.getString("buyer_name");
                    double bidAmount = resultSet.getDouble("bid_amount");

                    JOptionPane.showMessageDialog(null, "Item ID: " + itemId +
                            "\nBuyer User ID: " + buyerUserId +
                            "\nBuyer Name: " + buyerName +
                            "\nBid Amount: " + bidAmount);
                } else {
                    // Item not found
                    JOptionPane.showMessageDialog(null, "Item not found.");
                }
            }
        } catch (SQLException ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(null, "Error occurred while monitoring item.");
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            Object[] options = {"Add Item", "Monitor Items"};
            int choice = JOptionPane.showOptionDialog(null, "Select an option:", "Menu",
                    JOptionPane.YES_NO_OPTION, JOptionPane.QUESTION_MESSAGE, null, options, options[0]);

            if (choice == JOptionPane.YES_OPTION) {
                // User selected "Add Item"
                new SellerGUI(); // Open the SellerGUI when "Add Item" is selected
            } else if (choice == JOptionPane.NO_OPTION) {
                String userId = JOptionPane.showInputDialog("Enter User ID to monitor:");
                if (userId != null && !userId.isEmpty()) {
                    monitor(userId);
                } else {
                    JOptionPane.showMessageDialog(null, "Invalid User ID.");
                }
            } else {
                // User closed the dialog or clicked outside the options
                JOptionPane.showMessageDialog(null, "Invalid option or dialog closed.");
            }
        });
    }
}
