import pandas as pd

PURCHASED_ORDERS = 'purchase_orders.csv'
CANCELED_ORDERS = 'cancelled_orders.csv'
CLEANED_PURCHASED_ORDERS = "completed_purchase_orders.csv"

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

def completed_purchases(purchased_orders_csv, cancelled_orders_csv):
    purchased_orders = pd.read_csv(purchased_orders_csv)
    cancelled_orders = pd.read_csv(cancelled_orders_csv)

    purchased_orders = purchased_orders.copy()
    cancelled_orders = cancelled_orders.copy()

    # Create row values
    purchased_orders["RowValue"] = (
        purchased_orders["Quantity"] * purchased_orders["UnitPrice"]
    )

    cancelled_orders["RowValue"] = (
        cancelled_orders["Quantity"] * cancelled_orders["UnitPrice"]
    )

    # Keep original InvoiceNo, but create clean version for cancelled orders
    purchased_orders["CleanInvoiceNo"] = purchased_orders["InvoiceNo"].astype(str)

    #Removes the C at the begining of cancelled orders
    cancelled_orders["CleanInvoiceNo"] = (
        cancelled_orders["InvoiceNo"]
        .astype(str)
        .str.replace("^C", "", regex=True)
    )

    # Convert dates
    purchased_orders["InvoiceDate"] = pd.to_datetime(purchased_orders["InvoiceDate"])
    cancelled_orders["InvoiceDate"] = pd.to_datetime(cancelled_orders["InvoiceDate"])

    # Invoice-level purchase values
    purchased_invoice_values = (
        purchased_orders
        .groupby(["CustomerID", "InvoiceNo"])
        .agg(
            PurchaseDate=("InvoiceDate", "max"),
            PurchaseInvoiceValue=("RowValue", "sum")
        )
        .reset_index()
    )

    # Invoice-level cancelled values
    cancelled_invoice_values = (
        cancelled_orders
        .groupby(["CustomerID", "InvoiceNo"])
        .agg(
            CancelledDate=("InvoiceDate", "max"),
            CancelledInvoiceValue=("RowValue", "sum")
        )
        .reset_index()
    )

    # Make cancelled value positive for matching
    cancelled_invoice_values["CancelledInvoiceValueAbs"] = (
        cancelled_invoice_values["CancelledInvoiceValue"].abs()
    )

    # Round values to avoid tiny decimal problems
    purchased_invoice_values["MatchValue"] = (
        purchased_invoice_values["PurchaseInvoiceValue"].round(2)
    )

    cancelled_invoice_values["MatchValue"] = (
        cancelled_invoice_values["CancelledInvoiceValueAbs"].round(2)
    )

    # Sort before matching
    purchased_invoice_values = purchased_invoice_values.sort_values(
        by=["CustomerID", "MatchValue", "PurchaseDate"]
    )

    cancelled_invoice_values = cancelled_invoice_values.sort_values(
        by=["CustomerID", "MatchValue", "CancelledDate"]
    )

    # Prevent duplicate many-to-many matches
    purchased_invoice_values["MatchNumber"] = (
        purchased_invoice_values
        .groupby(["CustomerID", "MatchValue"])
        .cumcount()
    )

    cancelled_invoice_values["MatchNumber"] = (
        cancelled_invoice_values
        .groupby(["CustomerID", "MatchValue"])
        .cumcount()
    )

    # Match reversed purchases
    matched_reversed_invoices = purchased_invoice_values.merge(
        cancelled_invoice_values,
        on=["CustomerID", "MatchValue", "MatchNumber"],
        how="inner",
        suffixes=("_purchase", "_cancelled")
    )

    # Keep only cancellations that happened after the purchase
    matched_reversed_invoices = matched_reversed_invoices[
        matched_reversed_invoices["CancelledDate"] >= matched_reversed_invoices["PurchaseDate"]
    ]

    # Get purchase invoice numbers that were reversed
    reversed_purchase_invoice_numbers = matched_reversed_invoices["InvoiceNo_purchase"]

    # Remove reversed purchase invoices from completed purchases
    completed_purchase_orders = purchased_orders[
        ~purchased_orders["InvoiceNo"].isin(reversed_purchase_invoice_numbers)
    ].copy()

    # Save separate CSV files
    matched_reversed_invoices.to_csv("matched_reversed_invoices.csv", index=False)
    completed_purchase_orders.to_csv("completed_purchase_orders.csv", index=False)

    print("Completed purchases")
    print("Reversed purchase invoices found:", len(reversed_purchase_invoice_numbers))
    print("Purchase rows before:", len(purchased_orders))
    print("Purchase rows after:", len(completed_purchase_orders))

    return completed_purchase_orders, matched_reversed_invoices

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

    # Convert InvoiceDate to datetime
    purchase_orders["InvoiceDate"] = pd.to_datetime(purchase_orders["InvoiceDate"])

    # Create value for each product row
    purchase_orders["RowValue"] = (
        purchase_orders["Quantity"] * purchase_orders["UnitPrice"]
    ).round(2)

    # Create invoice-level order value
    invoice_values = (
        purchase_orders
        .groupby(["CustomerID", "InvoiceNo"])
        .agg(
            InvoiceDate=("InvoiceDate", "max"),
            OrderValue=("RowValue", "sum")
        )
        .reset_index()
    )

    invoice_values["OrderValue"] = invoice_values["OrderValue"].round(2)

    # Sort invoices by customer and date
    invoice_values = invoice_values.sort_values(
        by=["CustomerID", "InvoiceDate", "InvoiceNo"]
    )

    # Running order count per customer
    invoice_values["OrderCount"] = (
        invoice_values.groupby("CustomerID").cumcount() + 1
    )

    # Running monetary value per customer
    invoice_values["MonetaryValue"] = (
        invoice_values.groupby("CustomerID")["OrderValue"].cumsum()
    ).round(2)

    # Running average order value per customer
    invoice_values["AverageOrderValue"] = (
        invoice_values["MonetaryValue"] / invoice_values["OrderCount"]
    ).round(2)

    # Merge invoice/customer features back onto the original product rows
    customer_sales_data = purchase_orders.merge(
        invoice_values[
            [
                "CustomerID",
                "InvoiceNo",
                "OrderValue",
                "OrderCount",
                "MonetaryValue",
                "AverageOrderValue"
            ]
        ],
        on=["CustomerID", "InvoiceNo"],
        how="left"
    )

    # Sort final dataset
    customer_sales_data = customer_sales_data.sort_values(
        by=["CustomerID", "InvoiceDate", "InvoiceNo"]
    )

    # Keep columns in useful order
    customer_sales_data = customer_sales_data[
        [
            "CustomerID",
            "InvoiceNo",
            "StockCode",
            "Description",
            "InvoiceDate",
            "Quantity",
            "UnitPrice",
            "OrderValue",
            "OrderCount",
            "MonetaryValue",
            "AverageOrderValue",
            "Country"
        ]
    ]

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

    # Sort before removing duplicate invoice rows
    regression_data = regression_data.sort_values(
        by=["CustomerID", "InvoiceDate", "InvoiceNo"]
    )

    # Keep one row per invoice
    # This fixes the duplicated InvoiceNo problem caused by product-level rows
    regression_data = regression_data.drop_duplicates(
        subset=["CustomerID", "InvoiceNo"],
        keep="first"
    ).copy()

    # Sort again before creating previous customer behaviour
    regression_data = regression_data.sort_values(
        by=["CustomerID", "InvoiceDate", "InvoiceNo"]
    )

    # Previous customer behaviour before the current invoice
    regression_data["PreviousMonetaryValue"] = (
        regression_data.groupby("CustomerID")["MonetaryValue"].shift(1)
    )

    regression_data["PreviousAverageOrderValue"] = (
        regression_data.groupby("CustomerID")["AverageOrderValue"].shift(1)
    )

    regression_data["PreviousOrderCount"] = (
        regression_data.groupby("CustomerID")["OrderCount"].shift(1)
    )

    regression_data["PreviousOrderValue"] = (
        regression_data.groupby("CustomerID")["OrderValue"].shift(1)
    )

    regression_data["PreviousInvoiceDate"] = (
        regression_data.groupby("CustomerID")["InvoiceDate"].shift(1)
    )

    regression_data["DaysSincePreviousOrder"] = (
        regression_data["InvoiceDate"] - regression_data["PreviousInvoiceDate"]
    ).dt.days

    # Drop first order for each customer because there is no previous behaviour
    regression_data = regression_data.dropna(
        subset=[
            "PreviousMonetaryValue",
            "PreviousAverageOrderValue",
            "PreviousOrderCount",
            "PreviousOrderValue",
            "DaysSincePreviousOrder"
        ]
    ).copy()

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

    print("This is your duplicate data:", regression_data["InvoiceNo"].duplicated().sum())

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

cleaned_purchased_orders = pd.read_csv(CLEANED_PURCHASED_ORDERS, encoding="cp1252")

if __name__ == "__main__":
    create_customer_order_sales_dataset(cleaned_purchased_orders)

    sales_data = customer_sales_data(cleaned_purchased_orders)

    create_regression_data(sales_data)

    completed_purchases(PURCHASED_ORDERS, CANCELED_ORDERS)