import psycopg2

def create_modelcars_schema():
    # Connect to the PostgreSQL server
    conn = psycopg2.connect(
        dbname="dataengineering",  # Use default DB to create the new one
        user="postgres",
        password="Kamui",
        host="localhost"
    )
    conn.autocommit = True
    cursor = conn.cursor()

    # Create the modelcars database
    cursor.execute("CREATE DATABASE modelcars;")
    conn.commit()

    # Connect to the new modelcars database
    cursor.close()
    conn.close()

    conn = psycopg2.connect(
        dbname="modelcars",  # Now connect to the modelcars DB
        user="postgres",
        password="Kamui",
        host="localhost"
    )
    cursor = conn.cursor()

    # Schema SQL
    schema_sql = '''
    -- Create table for customers
    CREATE TABLE customers (
        customer_number INT PRIMARY KEY,
        customer_name VARCHAR(100) NOT NULL,
        contact_last_name VARCHAR(50),
        contact_first_name VARCHAR(50),
        phone VARCHAR(20),
        address_line1 VARCHAR(100),
        address_line2 VARCHAR(100),
        city VARCHAR(50),
        state VARCHAR(50),
        postal_code VARCHAR(15),
        country VARCHAR(50),
        sales_rep_employee_number INT,
        credit_limit DECIMAL(10, 2)
    );

    -- Create table for employees
    CREATE TABLE employees (
        employee_number NUMERIC PRIMARY KEY,
        last_name VARCHAR(50) NOT NULL,
        first_name VARCHAR(50) NOT NULL,
        extension VARCHAR(50),
        email VARCHAR(100),
        office_code VARCHAR(10),
        reports_to NUMERIC,
        job_title VARCHAR(50)
    );

    -- Create table for offices
    CREATE TABLE offices (
        office_code VARCHAR(10) PRIMARY KEY,
        city VARCHAR(50) NOT NULL,
        phone VARCHAR(20),
        address_line1 VARCHAR(100),
        address_line2 VARCHAR(100),
        state VARCHAR(50),
        country VARCHAR(50),
        postal_code VARCHAR(15),
        territory VARCHAR(50)
    );

    -- Create table for order_details
    CREATE TABLE order_details (
        order_number INT,
        product_code VARCHAR(50),
        quantity_ordered INT,
        price_each DECIMAL(10, 2),
        orderline_number SMALLINT,
        PRIMARY KEY (order_number, product_code)
    );

    -- Create table for orders
    CREATE TABLE orders (
        order_number INT PRIMARY KEY,
        order_date DATE NOT NULL,
        required_date DATE,
        shipped_date DATE DEFAULT NULL,
        status VARCHAR(100),
        comments TEXT,
        customer_number INT
    );

    -- Create table for payments
    CREATE TABLE payments (
        customer_number INT,
        check_number VARCHAR(50),
        payment_date DATE,
        amount DECIMAL(10, 2),
        PRIMARY KEY (customer_number, check_number)
    );

    -- Create table for product_lines
    CREATE TABLE product_lines (
        product_line VARCHAR(50) PRIMARY KEY,
        text_description TEXT,
        html_description TEXT,
        image VARCHAR(255)
    );

    -- Create table for products
    CREATE TABLE products (
        product_code VARCHAR(15) PRIMARY KEY,
        product_name VARCHAR(70),
        product_line VARCHAR(50),
        product_scale VARCHAR(10),
        product_vendor VARCHAR(50),
        product_description TEXT,
        quantity_instock INT,
        warehouse_code VARCHAR(10),
        buy_price DECIMAL(10, 2),
        msrp DECIMAL(10, 2)
    );

    -- Create table for warehouses
    CREATE TABLE warehouses (
        warehouse_code VARCHAR(10) PRIMARY KEY,
        warehouse_name VARCHAR(100),
        warehousepctcap DECIMAL(5, 2)
    );
    '''
    
    # Execute the schema SQL
    cursor.execute(schema_sql)
    conn.commit()

    # Close the connection
    cursor.close()
    conn.close()

# Call the function to create the schema
create_modelcars_schema()