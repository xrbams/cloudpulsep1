import pulumi
import pulumi_gcp as gcp
import json


def create_warehouse():
    # Define GCP project and dataset
    project = "shining-bazaar-436810-p2"  # Directly using the project ID
    dataset_name = "model_cars"  
    
    # Create BigQuery Dataset
    dataset = gcp.bigquery.Dataset(
        "model_cars_df",
        dataset_id=dataset_name,
        friendly_name="model_cars_df",
        location="US",  # Change if needed
        project=project
    )

    # Define schema for each table
    schemas = {
        "customers": [
                {"name": "customer_number", "type": "INT64", "mode": "REQUIRED"},
                {"name": "customer_name", "type": "STRING", "mode": "REQUIRED"},
                {"name": "contact_last_name", "type": "STRING"},
                {"name": "contact_first_name", "type": "STRING"},
                {"name": "phone", "type": "STRING"},
                {"name": "address_line1", "type": "STRING"},
                {"name": "address_line2", "type": "STRING"},
                {"name": "city", "type": "STRING"},
                {"name": "state", "type": "STRING"},
                {"name": "postal_code", "type": "STRING"},
                {"name": "country", "type": "STRING"},
                {"name": "sales_rep_employee_number", "type": "INT64"},
                {"name": "credit_limit", "type": "FLOAT64"},
            ],
        "employees":  [
                {"name": "employee_number", "type": "INT64", "mode": "REQUIRED"},
                {"name": "last_name", "type": "STRING", "mode": "REQUIRED"},
                {"name": "first_name", "type": "STRING", "mode": "REQUIRED"},
                {"name": "extension", "type": "STRING"},
                {"name": "email", "type": "STRING"},
                {"name": "office_code", "type": "STRING"},
                {"name": "reports_to", "type": "INT64"},
                {"name": "job_title", "type": "STRING"},
            ],
        "offices":  [
                {"name": "office_code", "type": "STRING", "mode": "REQUIRED"},
                {"name": "city", "type": "STRING", "mode": "REQUIRED"},
                {"name": "phone", "type": "STRING"},
                {"name": "address_line1", "type": "STRING"},
                {"name": "address_line2", "type": "STRING"},
                {"name": "state", "type": "STRING"},
                {"name": "country", "type": "STRING"},
                {"name": "postal_code", "type": "STRING"},
                {"name": "territory", "type": "STRING"},
            ],
        "orderdetails":  [
                {"name": "order_number", "type": "INT64", "mode": "REQUIRED"},
                {"name": "product_code", "type": "STRING", "mode": "REQUIRED"},
                {"name": "quantity_ordered", "type": "INT64"},
                {"name": "price_each", "type": "FLOAT64"},
                {"name": "orderline_number", "type": "INT64", "mode": "REQUIRED"},
            ],
        "orders":  [
                {"name": "order_number", "type": "INT64", "mode": "REQUIRED"},
                {"name": "order_date", "type": "DATE", "mode": "REQUIRED"},
                {"name": "required_date", "type": "DATE"},
                {"name": "shipped_date", "type": "DATE"},
                {"name": "status", "type": "STRING"},
                {"name": "comments", "type": "STRING"},
                {"name": "customer_number", "type": "INT64"},
            ],
        "payments":  [
                {"name": "customer_number", "type": "INT64"},
                {"name": "check_number", "type": "STRING", "mode": "REQUIRED"},
                {"name": "payment_date", "type": "DATE"},
                {"name": "amount", "type": "FLOAT64"},
            ],
        "productlines":  [
                {"name": "product_line", "type": "STRING", "mode": "REQUIRED"},
                {"name": "text_description", "type": "STRING"},
                {"name": "html_description", "type": "STRING"},
                {"name": "image", "type": "STRING"},
            ],
        "products":  [
                {"name": "product_code", "type": "STRING", "mode": "REQUIRED"},
                {"name": "product_name", "type": "STRING"},
                {"name": "product_line", "type": "STRING"},
                {"name": "product_scale", "type": "STRING"},
                {"name": "product_vendor", "type": "STRING"},
                {"name": "product_description", "type": "STRING"},
                {"name": "quantity_instock", "type": "INT64"},
                {"name": "warehouse_code", "type": "STRING"},
                {"name": "buy_price", "type": "FLOAT64"},
                {"name": "msrp", "type": "FLOAT64"},
            ],
        "warehouses":  [
                {"name": "warehouse_code", "type": "STRING", "mode": "REQUIRED"},
                {"name": "warehouse_name", "type": "STRING"},
                {"name": "warehousepctcap", "type": "FLOAT64"},
            ],
    }

    # Create all tables based on the schemas
    tables = {}
    for table_name, schema in schemas.items():
        print(f"Checking schema for {table_name}: type={type(schema)}, value={schema}")
        
        # Convert schema to JSON format
        schema_json = json.dumps(schema)
        
        # Create the BigQuery table with the JSON serialized schema
        tables[table_name] = gcp.bigquery.Table(
            f"{table_name}_table",
            dataset_id=dataset.dataset_id,
            table_id=table_name,
            schema=schema_json,  # Pass JSON serialized schema here
            project=project
        )

    # Export dataset ID and created tables
    pulumi.export("dataset_id", dataset.dataset_id)
    for table_name in tables:
        pulumi.export(f"{table_name}_table_id", tables[table_name].id)  # Export the IDs of created tables

    

# Call the function to create the warehouse
create_warehouse()