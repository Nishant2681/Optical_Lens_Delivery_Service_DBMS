import mysql.connector
import random
from faker import Faker
from datetime import datetime

# Initialize Faker for generating random data
fake = Faker()

# Connect to MySQL database
connection = mysql.connector.connect(
    host="localhost",
    user="root", 
    password="2001",
    database="optics"
)
cursor = connection.cursor()

# Define data insertion functions for each table
def populate_customer_table(num_records=50):
    customer_ids = []
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone = fake.phone_number()[:10]
        address = fake.address()
        
        cursor.execute("""
        INSERT INTO Customer (FirstName, LastName, Email, Phone, Address) 
        VALUES (%s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone, address))
        
        customer_ids.append(cursor.lastrowid)
    return customer_ids

def populate_supplier_table(num_records=20):
    supplier_ids = []
    for _ in range(num_records):
        name = fake.company()
        contact = fake.name()
        email = fake.email()
        phone = fake.phone_number()[:10]
        
        cursor.execute("""
        INSERT INTO Supplier (Name, ContactPerson, Email, Phone) 
        VALUES (%s, %s, %s, %s)
        """, (name, contact, email, phone))
        
        supplier_ids.append(cursor.lastrowid)
    return supplier_ids

def populate_shipping_method_table(num_records=10):
    shipping_method_ids = []
    for _ in range(num_records):
        name = fake.word()
        cost = round(random.uniform(5, 20), 2)
        estimated_delivery_time = f"{random.randint(1, 7)}:00:00"  # Hours in HH:MM:SS format
        
        cursor.execute("""
        INSERT INTO ShippingMethod (Name, Cost, EstimatedDeliveryTime) 
        VALUES (%s, %s, %s)
        """, (name, cost, estimated_delivery_time))
        
        shipping_method_ids.append(cursor.lastrowid)
    return shipping_method_ids

def populate_prescription_table(customer_ids, num_records=50):
    prescription_ids = []
    for _ in range(num_records):
        customer_id = random.choice(customer_ids)
        right_eye_power = round(random.uniform(-5, 5), 2)
        left_eye_power = round(random.uniform(-5, 5), 2)
        expiration_date = fake.date_between(start_date="today", end_date="+1y")
        
        cursor.execute("""
        INSERT INTO Prescription (CustomerID, RightEyePower, LeftEyePower, ExpirationDate) 
        VALUES (%s, %s, %s, %s)
        """, (customer_id, right_eye_power, left_eye_power, expiration_date))
        
        prescription_ids.append(cursor.lastrowid)
    return prescription_ids

def populate_payment_table(order_ids, num_records=50):
    payment_ids = []
    for order_id in order_ids:
        amount = round(random.uniform(50, 500), 2)
        payment_date = fake.date_between(start_date="-1y", end_date="today")
        payment_method = random.choice(['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer'])
        
        cursor.execute("""
        INSERT INTO Payment (OrderID, Amount, PaymentDate, PaymentMethod) 
        VALUES (%s, %s, %s, %s)
        """, (order_id, amount, payment_date, payment_method))
        
        payment_ids.append(cursor.lastrowid)
    return payment_ids

def update_order_with_payment_id(order_ids, payment_ids):
    for order_id, payment_id in zip(order_ids, payment_ids):
        cursor.execute("""
        UPDATE `Order` SET PaymentID = %s WHERE OrderID = %s
        """, (payment_id, order_id))

def populate_product_table(supplier_ids, num_records=50):
    product_ids = []
    for _ in range(num_records):
        supplier_id = random.choice(supplier_ids)
        product_name = fake.word() + ' Lens'
        type_ = random.choice(['Single Vision', 'Bifocal', 'Progressive'])
        price = round(random.uniform(20, 150), 2)
        quantity_in_stock = random.randint(0, 100)
        
        cursor.execute("""
        INSERT INTO Product (SupplierID, ProductName, Type, Price, QuantityInStock) 
        VALUES (%s, %s, %s, %s, %s)
        """, (supplier_id, product_name, type_, price, quantity_in_stock))
        
        product_ids.append(cursor.lastrowid)
    return product_ids

def populate_inventory_table(product_ids, num_records=50):
    inventory_ids = []
    for _ in range(num_records):
        product_id = random.choice(product_ids)
        quantity_available = random.randint(10, 100)
        last_restock_date = fake.date_between(start_date="-6m", end_date="today")
        
        cursor.execute("""
        INSERT INTO Inventory (ProductID, QuantityAvailable, LastRestockDate) 
        VALUES (%s, %s, %s)
        """, (product_id, quantity_available, last_restock_date))
        
        inventory_ids.append(cursor.lastrowid)
    return inventory_ids

def populate_order_table(customer_ids, shipping_method_ids, num_records=50):
    order_ids = []
    for _ in range(num_records):
        customer_id = random.choice(customer_ids)
        shipping_method_id = random.choice(shipping_method_ids)
        order_date = fake.date_between(start_date="-1y", end_date="today")
        order_status = random.choice(['Pending', 'Shipped', 'Delivered', 'Cancelled'])
        
        cursor.execute("""
        INSERT INTO `Order` (OrderDate, OrderStatus, CustomerID, ShippingMethodID) 
        VALUES (%s, %s, %s, %s)
        """, (order_date, order_status, customer_id, shipping_method_id))
        
        order_ids.append(cursor.lastrowid)
    return order_ids

def populate_employee_table(num_records=30):
    employee_ids = []
    for _ in range(num_records):
        first_name = fake.first_name()
        last_name = fake.last_name()
        email = fake.email()
        phone = fake.phone_number()[:10]
        position = random.choice(['Sales', 'Support', 'Technician'])
        hire_date = fake.date_between(start_date="-5y", end_date="today")
        
        cursor.execute("""
        INSERT INTO Employee (FirstName, LastName, Email, Phone, Position, HireDate) 
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (first_name, last_name, email, phone, position, hire_date))
        
        employee_ids.append(cursor.lastrowid)
    return employee_ids

# Populate additional tables with foreign keys
def populate_customer_review(customer_ids, product_ids, num_records=50):
    review_ids = []
    for _ in range(num_records):
        customer_id = random.choice(customer_ids)
        product_id = random.choice(product_ids)
        rating = random.randint(1, 5)  # Rating between 1 and 5
        comment = fake.text(max_nb_chars=200)  # Random review comment
        review_date = fake.date_this_year()

        # Insert a new review into the CustomerReview table
        cursor.execute("""
        INSERT INTO CustomerReview (CustomerID, ProductID, Rating, Comment, ReviewDate) 
        VALUES (%s, %s, %s, %s, %s)
        """, (customer_id, product_id, rating, comment, review_date))
        
        # Capture the auto-generated ReviewID
        review_ids.append(cursor.lastrowid)
    
    return review_ids

def populate_return_refund(order_ids, product_ids, num_records=30):
    return_refund_ids = []
    for _ in range(num_records):
        order_id = random.choice(order_ids)
        product_id = random.choice(product_ids)
        return_reason = fake.sentence(nb_words=6)
        refund = round(random.uniform(5, 150), 2)  # Random refund amount
        
        # Insert a new return/refund record into the Return/Refund table
        cursor.execute("""
        INSERT INTO Return_Refund (OrderID, ProductID, ReturnReason, RefundAmount) 
        VALUES (%s, %s, %s, %s)
        """, (order_id, product_id, return_reason, refund))
        
        # Capture the auto-generated Return/RefundID
        return_refund_ids.append(cursor.lastrowid)
    
    return return_refund_ids
    
def populate_contains(order_ids, product_ids, num_records=50):
    for _ in range(num_records):
        order_id = random.choice(order_ids)
        product_id = random.choice(product_ids)
        
        cursor.execute("""
        INSERT IGNORE INTO Contains (OrderID, ProductID) 
        VALUES (%s, %s)
        """, (order_id, product_id))

def populate_provides(supplier_ids, product_ids, num_records=50):
    for _ in range(num_records):
        supplier_id = random.choice(supplier_ids)
        product_id = random.choice(product_ids)
        
        cursor.execute("""
        INSERT IGNORE INTO Provides (SupplierID, ProductID) 
        VALUES (%s, %s)
        """, (supplier_id, product_id))

def populate_handles(employee_ids, ticket_ids, num_records=30):
    unique_pairs = set()

    while len(unique_pairs) < num_records:
        employee_id = random.choice(employee_ids)
        ticket_id = random.choice(ticket_ids)

        # Only insert if the (employee_id, ticket_id) pair is unique
        if (employee_id, ticket_id) not in unique_pairs:
            unique_pairs.add((employee_id, ticket_id))
            cursor.execute("""
                INSERT INTO Handles (EmployeeID, TicketID) 
                VALUES (%s, %s)
            """, (employee_id, ticket_id))

def populate_tracked_by(inventory_ids, product_ids, num_records=50):
    for _ in range(num_records):
        inventory_id = random.choice(inventory_ids)
        product_id = random.choice(product_ids)
        quantity = random.randint(10, 100)
        last_restock_date = fake.date_between(start_date="-6m", end_date="today")
        
        cursor.execute("""
        INSERT IGNORE INTO TrackedBy (InventoryID, ProductID, Quantity, LastRestockDate) 
        VALUES (%s, %s, %s, %s)
        """, (inventory_id, product_id, quantity, last_restock_date))

def populate_fulfills(order_ids, employee_ids, num_records=50):
    for _ in range(num_records):
        order_id = random.choice(order_ids)
        employee_id = random.choice(employee_ids)
        
        cursor.execute("""
        INSERT IGNORE INTO Fulfills (OrderID, EmployeeID) 
        VALUES (%s, %s)
        """, (order_id, employee_id))

def populate_customer_support_ticket(customer_ids, employee_ids, num_records=50):
    ticket_ids = []
    for _ in range(num_records):
        # Generate random data for each record
        customer_id = random.choice(customer_ids)
        employee_id = random.choice(employee_ids)
        issue_description = fake.sentence(nb_words=10)  # Random issue description
        status = random.choice(['Open', 'In Progress', 'Resolved', 'Closed'])
        creation_date = fake.date_this_year()  # Random date this year for creation
        resolution_date = None if status == 'Open' or status == 'In Progress' else fake.date_this_year()  # Random resolution date if closed or resolved
        
        # Insert the generated data into the CustomerSupportTicket table
        cursor.execute("""
            INSERT INTO CustomerSupportTicket (CustomerID, EmployeeID, IssueDescription, Status, CreationDate, ResolutionDate)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (customer_id, employee_id, issue_description, status, creation_date, resolution_date))
        ticket_ids.append(cursor.lastrowid)
    return ticket_ids

# Main function to populate all the tables
def populate_all_tables():
    # Populate independent tables
    supplier_ids = populate_supplier_table()
    product_ids = populate_product_table(supplier_ids)
    inventory_ids = populate_inventory_table(product_ids)
    employee_ids = populate_employee_table()
    shipping_method_ids = populate_shipping_method_table()
    customer_ids = populate_customer_table()
    prescription_ids = populate_prescription_table(customer_ids)
    ticket_ids = populate_customer_support_ticket(customer_ids, employee_ids)

    # Populate orders without payment ID
    order_ids = populate_order_table(customer_ids, shipping_method_ids)
    
    # Populate payments with order ID and update orders with payment ID
    payment_ids = populate_payment_table(order_ids)
    update_order_with_payment_id(order_ids, payment_ids)
    
    # Populate other tables dependent on completed tables
    populate_customer_review(customer_ids, product_ids)
    populate_return_refund(order_ids, product_ids)
    populate_contains(order_ids, product_ids)
    populate_provides(supplier_ids, product_ids)
    populate_handles(employee_ids, ticket_ids)
    populate_tracked_by(inventory_ids, product_ids)
    populate_fulfills(order_ids, employee_ids)
    
    # Commit changes
    connection.commit()

populate_all_tables()

# Close cursor and connection
cursor.close()
connection.close()