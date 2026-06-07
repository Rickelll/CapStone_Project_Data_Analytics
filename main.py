import pandas as pd

PURCHASED_ORDERS = 'purchase_orders.csv'
CANCELLED_ORDERS = 'canceled_orders.csv'

def split_order_types(df):
    """
    Splits the dataset into:
    - purchase_orders: normal valid purchases
    - cancelled_orders: invoices that start with C
    - returned_orders: orders with negative quantity
    """

    # Make a copy so we do not damage the original dataset
    df = df.copy()

    # Fill missing descriptions
    df["Description"] = df["Description"].fillna("Unknown")

    # Remove rows with missing CustomerID
    df = df.dropna(subset=["CustomerID"]).copy()

    # Cancelled orders: InvoiceNo starts with C
    cancelled_orders = df[df["InvoiceNo"].astype(str).str.startswith("C")].copy()

    # Normal purchases only
    purchase_orders = df[
        (~df["InvoiceNo"].astype(str).str.startswith("C")) &
        (df["Quantity"] > 0) &
        (df["UnitPrice"] > 0)
    ].copy()

    # Convert InvoiceNo to int only for normal purchases
    purchase_orders["InvoiceNo"] = purchase_orders["InvoiceNo"].astype(int)

    return purchase_orders, cancelled_orders


def create_customer_sales_dataset(purchase_orders):
    print("Creating customer sales dataset...")

    purchase_orders = purchase_orders.copy()

    # Create row value
    purchase_orders["RowValue"] = (
        purchase_orders["Quantity"] * purchase_orders["UnitPrice"]
    )

    # Convert InvoiceDate
    purchase_orders["InvoiceDate"] = pd.to_datetime(purchase_orders["InvoiceDate"])

    # First create order-level totals
    order_values = (purchase_orders.groupby(["CustomerID", "InvoiceNo"])
        .agg(
            InvoiceDate=("InvoiceDate", "max"),
            OrderValue=("RowValue", "sum"),
            TotalQuantity=("Quantity", "sum")
        ).reset_index())

    # Reference date for recency
    reference_date = order_values["InvoiceDate"].max() + pd.Timedelta(days=1)

    # Create one row per customer
    customer_sales_data = (order_values.groupby("CustomerID")
        .agg(Frequency=("InvoiceNo", "nunique"),
            Recency=("InvoiceDate", lambda x: (reference_date - x.max()).days),
            MonetaryValue=("OrderValue", "sum"),
            AverageOrderValue=("OrderValue", "mean"),
            TotalQuantity=("TotalQuantity", "sum")
        ).reset_index())

    # Round money columns
    money_columns = ["MonetaryValue", "AverageOrderValue"]

    customer_sales_data[money_columns] = customer_sales_data[money_columns].round(2)

    # Save to CSV
    customer_sales_data.to_csv("customer_order_sales_data.csv",index=False,float_format="%.2f")

    print(customer_sales_data.head())
    print("customer_order_sales_data.csv has been created.")

    return customer_sales_data

def customer_sales_data(purchase_orders):
    print("Welcome to Customer Data")

    # Make a copy so the original dataset is safe
    purchase_orders = purchase_orders.copy()

    # Create value for each product row
    purchase_orders["RowValue"] = (purchase_orders["Quantity"] * purchase_orders["UnitPrice"])

    # Convert InvoiceDate to datetime
    purchase_orders["InvoiceDate"] = pd.to_datetime(purchase_orders["InvoiceDate"])

    # Create total value for each order/invoice
    order_values = (purchase_orders.groupby(["CustomerID", "InvoiceNo"]).agg(InvoiceDate=("InvoiceDate", "max"),OrderValue=("RowValue", "sum")).reset_index()).round(2)

    # Sort by customer and date so running totals work correctly
    order_values = order_values.sort_values(by=["CustomerID", "InvoiceDate", "InvoiceNo"])

    # MonetaryValue: running total spent by the customer
    order_values["MonetaryValue"] = (order_values.groupby("CustomerID")["OrderValue"].cumsum()).round(2)

    # AverageOrderValue: running average spend per order
    order_values["AverageOrderValue"] = (order_values["MonetaryValue"] / len(order_values)).round(2)

    # Keep columns in the order you want
    customer_sales_data = order_values[
        [
            "CustomerID",
            "InvoiceNo",
            "InvoiceDate",
            "MonetaryValue",
            "AverageOrderValue",
            "OrderValue"
        ]
    ]

    # Save to CSV
    customer_sales_data.to_csv("customer_sales_data.csv", index=False)

    print(customer_sales_data.head())
    print("customer_sales_data.csv has been created.")

    return customer_sales_data

dataset = pd.read_csv('customer_segmentation_data.csv', encoding="cp1252")

#Checking for missing values
#print(dataset.isnull().sum())
#print("Length of the Data: ",len(dataset))

# Convert CustomerID to int

#There is still plent of useful data where the description isnt so filling the missing data with unkown would be the best option to keep all the data good.
dataset['Description'] = dataset['Description'].fillna('Unknown')

#Checking missing values in dataset['Description']
#print(dataset.isnull().sum())

#Dropping CustomerID because we cant create new Reliable CustomerID data
dataset = dataset.dropna(subset=['CustomerID'])

#making sure all customerID is int value
dataset["CustomerID"] = dataset["CustomerID"].astype(int)

#Adding all data to DataFrame after all missing data has been dealt with
df = pd.DataFrame(dataset)

#using the function we can split all of data to make the cancelled, returned and normal orders into different datasets
purchase_orders, cancelled_orders = split_order_types(dataset)

print("Purchase orders:", len(purchase_orders))
print("Cancelled orders:", len(cancelled_orders))

purchase_orders.to_csv("purchase_orders.csv", index=False)
cancelled_orders.to_csv("cancelled_orders.csv", index=False)

print(df.columns)

while True:
    try:
        question = int(input("Enter Your Choice: "))
    except ValueError:
        print("Please enter a number.")
        continue
    if question == 1:
        create_customer_sales_dataset(purchase_orders)
    elif question == 2:
        customer_sales_data(purchase_orders)
