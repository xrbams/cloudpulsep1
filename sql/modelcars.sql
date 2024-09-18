

CREATE DATABASE modelcars;

\c modelcars

-- Create schema for modelcars data
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
    employee_number INT PRIMARY KEY,
    last_name VARCHAR(50) NOT NULL,
    first_name VARCHAR(50) NOT NULL,
    extension VARCHAR(10),
    email VARCHAR(100),
    office_code VARCHAR(10),
    reports_to INT,
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
    territory VARCHAR(10)
);

-- Create table for order_details
CREATE TABLE order_details (
    order_number INT,
    product_code VARCHAR(15),
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
    shipped_date DATE,
    status VARCHAR(15),
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
-- customers table: customer_number,customer_name,contact_last_name,contact_first_name,phone,address_line1,address_line2,city,state,postal_code,country,salesRepEmployeeNumber,credit_Limit
-- employees table: employee_number,last_name,first_name,extension,email,officecode,reports_to,job_title
-- offices table: office_code,city,phone,address_line1,address_line2,state,country,postal_code,territory
-- order_details table: order_number,product_code,quantity_ordered,price_each,orderline_number
-- orders table: order_number,order_date,required_date,shipped_date,status,comments,customer_number
-- payments table: customer_number,check_number,payment_date,amount
-- product_lines table: product_line,text_description,html_description,image
-- products table: product_code,product_name,product_line,product_scale,product_vendor,product_description,quantity_instock,warehouse_code,buy_price,msrp
-- warehouses table: warehouse_code,warehouse_name,warehousepctcap