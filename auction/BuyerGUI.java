package auction;

import javax.swing.*;
import javax.swing.table.DefaultTableModel;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.PreparedStatement;
import java.sql.ResultSet;
import java.sql.SQLException;

public class BuyerGUI {
    public static void main(String[] args) {
        JFrame frame = new JFrame("Auction Buyer");
        frame.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        frame.setSize(600, 400);

        JPanel formPanel = new JPanel();
        frame.add(formPanel);
        createForm(formPanel);

        // Create a table model and set column names
        DefaultTableModel tableModel = new DefaultTableModel();
        JTable table = new JTable(tableModel);
   //     tableModel.addColumn("Item ID");
        tableModel.addColumn("User ID");
        tableModel.addColumn("Item Name");
        tableModel.addColumn("Item Description");
        tableModel.addColumn("Base Price");
        tableModel.addColumn("Time Period");

        // Fetch items from the database and populate the table
        fetchItemsFromDatabase(tableModel);

        // Add the table to a scroll pane
        JScrollPane scrollPane = new JScrollPane(table);
        frame.add(scrollPane);

        frame.setLayout(new BoxLayout(frame.getContentPane(), BoxLayout.Y_AXIS));
        frame.setVisible(true);
    }
    private static double getBasePriceFromDatabase(Connection con, String userId) throws SQLException {
        String query = "SELECT base_price FROM new_table WHERE user_id = ?";
        try (PreparedStatement pstm = con.prepareStatement(query)) {
            pstm.setString(1, userId);
            ResultSet rs = pstm.executeQuery();
            if (rs.next()) {
                return rs.getDouble("base_price");
            } else {
                throw new SQLException("Item not found in the database.");
            }
        }
    }
    
    private static void updateBasePriceInDatabase(Connection con, String userId, double newPrice) throws SQLException {
        String query = "UPDATE new_table SET base_price = ? WHERE user_id = ?";
        try (PreparedStatement pstm = con.prepareStatement(query)) {
            pstm.setDouble(1, newPrice);
            pstm.setString(2, userId);
            int rowsAffected = pstm.executeUpdate();
            if (rowsAffected == 0) {
                throw new SQLException("Failed to update base price.");
            }
        }
    }
    
    
    
    private static void createForm(JPanel panel) {
        panel.setLayout(null);

        JLabel itemIdLabel = new JLabel("seller ID:");
        itemIdLabel.setBounds(20, 20, 80, 25);
        panel.add(itemIdLabel);

        JTextField itemIdField = new JTextField(20);
        itemIdField.setBounds(120, 20, 200, 25);
        panel.add(itemIdField);

        JLabel buyerIdLabel = new JLabel("Your ID:");
        buyerIdLabel.setBounds(20, 50, 80, 25);
        panel.add(buyerIdLabel);

        JTextField buyerIdField = new JTextField(20);
        buyerIdField.setBounds(120, 50, 200, 25);
        panel.add(buyerIdField);

        JLabel buyerNameLabel = new JLabel("Your Name:");
        buyerNameLabel.setBounds(20, 80, 80, 25);
        panel.add(buyerNameLabel);

        JTextField buyerNameField = new JTextField(20);
        buyerNameField.setBounds(120, 80, 200, 25);
        panel.add(buyerNameField);

        JLabel bidAmountLabel = new JLabel("Bid Amount:");
        bidAmountLabel.setBounds(20, 110, 80, 25);
        panel.add(bidAmountLabel);

        JTextField bidAmountField = new JTextField(20);
        bidAmountField.setBounds(120, 110, 200, 25);
        panel.add(bidAmountField);

        JButton placeBidButton = new JButton("Place Bid");
        placeBidButton.setBounds(150, 140, 100, 25);
        panel.add(placeBidButton);

        placeBidButton.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                String itemId = itemIdField.getText();
                String buyerId = buyerIdField.getText();
                String buyerName = buyerNameField.getText();
                double bidAmount = Double.parseDouble(bidAmountField.getText());
        
                try (Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/seller_details", "root", "123456789")) {
                    double basePrice = getBasePriceFromDatabase(con, itemId);
                    if (bidAmount > basePrice) {
                        Buyer.placeBid(con, itemId, buyerId, buyerName, bidAmount);
                        updateBasePriceInDatabase(con, itemId, bidAmount);
                        JOptionPane.showMessageDialog(null, "Bid placed successfully!");
                    } else {
                        JOptionPane.showMessageDialog(null, "Bid amount should be greater than the base price.");
                    }
                } catch (SQLException ex) {
                    ex.printStackTrace();
                    JOptionPane.showMessageDialog(null, "Bid placed successfully!");
                }
            }
        });
    }

    private static void fetchItemsFromDatabase(DefaultTableModel tableModel) {
        try (Connection con = DriverManager.getConnection("jdbc:mysql://localhost:3306/seller_details", "root", "123456789")) {
            String query = "SELECT user_id, item_name, item_des, base_price, time_period FROM new_table";
            PreparedStatement pstm = con.prepareStatement(query);
            ResultSet rs = pstm.executeQuery();
    
            while (rs.next()) {
                Object[] rowData = {
                        rs.getString("user_id"),
                        rs.getString("item_name"),
                        rs.getString("item_des"),
                        rs.getDouble("base_price"),
                        rs.getInt("time_period")
                };
                tableModel.addRow(rowData);
            }
    
            rs.close();
            pstm.close();
        } catch (SQLException ex) {
            ex.printStackTrace();
            JOptionPane.showMessageDialog(null, "Error occurred while fetching items from the database.");
        }
    }
}
