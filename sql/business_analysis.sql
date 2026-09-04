SELECT
    (SELECT COUNT(*) FROM Suppliers) AS Total_Suppliers,
    (SELECT COUNT(*) FROM Products) AS Total_Products,
    (SELECT COUNT(*) FROM Purchase_Orders) AS Total_Orders,
    (SELECT COUNT(*) FROM Countries) AS Total_Countries;

