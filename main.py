import pandas as pd

PURCHASED_ORDERS = 'purchase_orders.csv'
CANCELED_ORDERS = 'cancelled_orders.csv'

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

    df['Country'] = df['Country'].astype('category').cat.codes


    # Remove rows with missing CustomerID
    df = df.dropna(subset=["CustomerID"]).copy()

    df['CustomerID'] = df['CustomerID'].astype(int)

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

def completed_purchases(purchased_orders, cancelled_orders):

    purchased_orders = pd.read_csv(purchased_orders)
    cancelled_orders = pd.read_csv(cancelled_orders)

    purchased_orders = purchased_orders.copy()

    cancelled_orders = cancelled_orders.copy()

    print(purchased_orders['InvoiceNo'].head(5))
    print(cancelled_orders['InvoiceNo'].head(5))

    print(purchased_orders.columns)
    print(cancelled_orders.columns)
    print("Completed purchases")


def create_customer_order_sales_dataset(purchase_orders):
    print("Creating customer sales dataset...")

    purchase_orders = purchase_orders.copy()

    # Create row value
    purchase_orders["RowValue"] = (purchase_orders["Quantity"] * purchase_orders["UnitPrice"])

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
    print(purchase_orders.columns)
    print(purchase_orders.dtypes)

    # Create value for each product row
    purchase_orders["RowValue"] = (purchase_orders["Quantity"] * purchase_orders["UnitPrice"])

    # Convert InvoiceDate to datetime
    purchase_orders["InvoiceDate"] = pd.to_datetime(purchase_orders["InvoiceDate"])

    # Create total value for each order/invoice
    order_values = (purchase_orders.groupby(["CustomerID", "InvoiceNo"]).agg(InvoiceDate=("InvoiceDate", "max"),
                                                                             Country=("Country", "first"),
                                                                             OrderValue=("RowValue", "sum"),
                                                                             ).reset_index()).round(2)

    # Round order value
    order_values["OrderValue"] = order_values["OrderValue"].round(2)

    # Sort by customer and date so running totals work correctly
    order_values = order_values.sort_values(by=["CustomerID", "InvoiceDate", "InvoiceNo"])

    # Running order count per customer
    order_values["OrderCount"] = (order_values.groupby("CustomerID").cumcount() + 1)

    # MonetaryValue: running total spent by the customer
    order_values["MonetaryValue"] = (order_values.groupby("CustomerID")["OrderValue"].cumsum()).round(2)

    # AverageOrderValue: running average spend per order
    order_values["AverageOrderValue"] = (order_values["MonetaryValue"] / order_values["OrderCount"]).round(2)

    # Keep columns in the order you want
    customer_sales_data = order_values[
        [
            "CustomerID",
            "InvoiceNo",
            "InvoiceDate",
            "OrderCount",
            "MonetaryValue",
            "AverageOrderValue",
            "Country",
            "OrderValue"
        ]
    ]

    # Save to CSV
    customer_sales_data.to_csv("customer_sales_data.csv", index=False)

    print(customer_sales_data.head())
    print("customer_sales_data.csv has been created.")

    return customer_sales_data

def create_regression_data(customer_sales_data):
    print("Creating regression dataset...")

    # Make a copy so the reporting dataset is not changed
    regression_data = customer_sales_data.copy()

    # Make sure InvoiceDate is datetime
    regression_data["InvoiceDate"] = pd.to_datetime(regression_data["InvoiceDate"])

    # Sort correctly before creating previous values
    regression_data = regression_data.sort_values(by=["CustomerID", "InvoiceDate", "InvoiceNo"])

    # Previous customer behaviour before the current order
    regression_data["PreviousMonetaryValue"] = (regression_data.groupby("CustomerID")["MonetaryValue"].shift(1))

    regression_data["PreviousAverageOrderValue"] = (regression_data.groupby("CustomerID")["AverageOrderValue"].shift(1))

    regression_data["PreviousOrderCount"] = (regression_data.groupby("CustomerID")["OrderCount"].shift(1))

    regression_data["PreviousOrderValue"] = (regression_data.groupby("CustomerID")["OrderValue"].shift(1))

    regression_data["PreviousInvoiceDate"] = (regression_data.groupby("CustomerID")["InvoiceDate"].shift(1))

    regression_data["DaysSincePreviousOrder"] = (regression_data["InvoiceDate"] - regression_data["PreviousInvoiceDate"]).dt.days

    # Drop first order for each customer because there is no previous behaviour
    regression_data = regression_data.dropna(subset=[
            "PreviousMonetaryValue",
            "PreviousAverageOrderValue",
            "PreviousOrderCount",
            "PreviousOrderValue",
            "DaysSincePreviousOrder"
        ]
    )

    # Keep only useful regression columns
    regression_data = regression_data[
        [
            "CustomerID",
            "InvoiceNo",
            "InvoiceDate",
            "Country",
            "PreviousMonetaryValue",
            "PreviousAverageOrderValue",
            "PreviousOrderCount",
            "PreviousOrderValue",
            "DaysSincePreviousOrder",
            "OrderValue"
        ]
    ]

    # Round numeric values
    regression_data = regression_data.round(2)

    # Save regression-ready CSV
    regression_data.to_csv("customer_regression_data.csv", index=False)

    print("customer_regression_data.csv has been created.")

    return regression_data

dataset = pd.read_csv('customer_segmentation_data.csv', encoding="cp1252")

#Adding all data to DataFrame after all missing data has been dealt with
df = pd.DataFrame(dataset)

#using the function we can split all of data to make the cancelled, returned and normal orders into different datasets
purchase_orders, cancelled_orders = split_order_types(dataset)


purchase_orders.to_csv("purchase_orders.csv", index=False)
cancelled_orders.to_csv("cancelled_orders.csv", index=False)


if __name__ == "__main__":
    create_customer_order_sales_dataset(purchase_orders)

    sales_data = customer_sales_data(purchase_orders)

    create_regression_data(sales_data)

    completed_purchases(PURCHASED_ORDERS, CANCELED_ORDERS)