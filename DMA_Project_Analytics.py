import mysql.connector
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root",  
    password="2001",
    database="optics"
)

cursor = connection.cursor()

print('1. Query: Total number of orders per customer:')
query1 = """
SELECT CustomerID, COUNT(OrderID) AS TotalOrders
FROM `Order`
GROUP BY CustomerID
ORDER BY TotalOrders DESC;
"""
cursor.execute(query1)
orders_per_customer = cursor.fetchall()
df_orders = pd.DataFrame(orders_per_customer, columns=["CustomerID", "TotalOrders"])
print(df_orders.head())

# Visualization: Total number of orders per customer
plt.figure(figsize=(10, 6))
sns.barplot(x="CustomerID", y="TotalOrders", data=df_orders, palette="viridis")
plt.title("Total Number of Orders Per Customer", fontsize=16)
plt.xlabel("Customer ID", fontsize=12)
plt.ylabel("Total Orders", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print('2. Query: Average product rating per product:')
query2 = """
SELECT ProductID, AVG(Rating) AS AverageRating
FROM CustomerReview
GROUP BY ProductID
ORDER BY AverageRating DESC;
"""
cursor.execute(query2)
average_ratings = cursor.fetchall()
df_ratings = pd.DataFrame(average_ratings, columns=["ProductID", "AverageRating"])
print(df_ratings.head())

# Visualization: Average product rating per product
plt.figure(figsize=(10, 6))
sns.barplot(x="ProductID", y="AverageRating", data=df_ratings, palette="coolwarm")
plt.title("Average Product Rating Per Product", fontsize=16)
plt.xlabel("Product ID", fontsize=12)
plt.ylabel("Average Rating", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("Query: Total revenue generated per product:")
query3 = """
SELECT P.ProductID, P.ProductName, COUNT(C.OrderID) * P.Price AS TotalRevenue
FROM Product P
JOIN Contains C ON P.ProductID = C.ProductID
GROUP BY P.ProductID, P.ProductName
ORDER BY TotalRevenue DESC;
"""
cursor.execute(query3)
revenue_per_product = cursor.fetchall()
df_revenue = pd.DataFrame(revenue_per_product, columns=["ProductID", "ProductName", "TotalRevenue"])
print(df_revenue.head())

# Visualization: Total revenue generated per product
plt.figure(figsize=(12, 6))
sns.barplot(x="ProductName", y="TotalRevenue", data=df_revenue, color="mediumseagreen")
plt.title("Total Revenue Generated Per Product", fontsize=16)
plt.xlabel("Product Name", fontsize=12)
plt.ylabel("Total Revenue ($)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

print("Query: Distribution of Payment Amounts by Payment Method:")
query4 = """
SELECT PaymentMethod, Amount
FROM Payment;
"""
cursor.execute(query4)
payment_data = cursor.fetchall()
df_payment = pd.DataFrame(payment_data, columns=["PaymentMethod", "Amount"])
print(df_payment.head())

# Visualization: Box plot of payment amounts by payment method
plt.figure(figsize=(10, 6))
sns.boxplot(x="PaymentMethod", y="Amount", data=df_payment, palette="Set2")
plt.title("Distribution of Payment Amounts by Payment Method", fontsize=16)
plt.xlabel("Payment Method", fontsize=12)
plt.ylabel("Payment Amount ($)", fontsize=12)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# Close the connection
cursor.close()
connection.close()
