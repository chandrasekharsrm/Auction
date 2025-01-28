package auction;

import java.sql.Connection;
import java.sql.PreparedStatement;
import java.sql.SQLException;

public class Buyer {

    public static void placeBid(Connection con, String itemId, String buyerId, String buyerName, double bidAmount) throws SQLException {
        double basePrice = getBasePriceFromDatabase(con, itemId);
        if (bidAmount > basePrice) {
            updateBasePriceInDatabase(con, itemId, bidAmount);
            storeBuyerDetails(con, itemId, buyerId, buyerName, bidAmount);
        } else {
            throw new IllegalArgumentException("Bid amount should be greater than the base price.");
        }
    }

    private static double getBasePriceFromDatabase(Connection con, String itemId) throws SQLException {
        String query = "SELECT base_price FROM new_table WHERE user_id = ?";
        try (PreparedStatement pstm = con.prepareStatement(query)) {
            pstm.setString(1, itemId);
            try (var rs = pstm.executeQuery()) {
                if (rs.next()) {
                    return rs.getDouble("base_price");
                } else {
                    throw new SQLException("Item not found in the database.");
                }
            }
        }
    }

    private static void updateBasePriceInDatabase(Connection con, String itemId, double newPrice) throws SQLException {
        String query = "UPDATE new_table SET base_price = ? WHERE user_id = ?";
        try (PreparedStatement pstm = con.prepareStatement(query)) {
            pstm.setDouble(1, newPrice);
            pstm.setString(2, itemId);
            int rowsAffected = pstm.executeUpdate();
            if (rowsAffected == 0) {
                throw new SQLException("Failed to update base price.");
            }
        }
    }

    private static void storeBuyerDetails(Connection con, String itemId, String buyerId, String buyerName, double bidAmount) throws SQLException {
        String query = "INSERT INTO buyer_details (item_id, user_id, buyer_name, bid_amount) VALUES (?, ?, ?, ?)";
        try (PreparedStatement pstm = con.prepareStatement(query)) {
            pstm.setString(1, itemId);
            pstm.setString(2, buyerId);
            pstm.setString(3, buyerName);
            pstm.setDouble(4, bidAmount);
            pstm.executeUpdate();
        }
    }
}
