import pandas as pd

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

    # Returned orders: Quantity is less than 0
    returned_orders = df[df["Quantity"] < 0].copy()

    # Normal purchases only
    purchase_orders = df[
        (~df["InvoiceNo"].astype(str).str.startswith("C")) &
        (df["Quantity"] > 0) &
        (df["UnitPrice"] > 0)
    ].copy()

    # Convert InvoiceNo to int only for normal purchases
    purchase_orders["InvoiceNo"] = purchase_orders["InvoiceNo"].astype(int)

    return purchase_orders, cancelled_orders, returned_orders

def value(purchase_orders):
    print("Welcome to Customer Data")

    # Make a copy so the original purchase_orders is not changed by accident
    purchase_orders = purchase_orders.copy()

    # Create order value once at the start
    purchase_orders["OrderValue"] = (
        purchase_orders["Quantity"] * purchase_orders["UnitPrice"]
    )

    # Make sure InvoiceDate is datetime once at the start
    purchase_orders["InvoiceDate"] = pd.to_datetime(purchase_orders["InvoiceDate"])

    while True:
        print("\n1. Show total order value")
        print("2. Show most frequent customers")
        print("3. Show most recent customers")
        print("4. Show highest customer spending")
        print("5. Show customer sales dataset")
        print("back. Exit menu")

        question = input("Enter Your Choice: ").lower()

        if question == "1":
            print(purchase_orders[["InvoiceNo", "CustomerID", "OrderValue"]].head())

        elif question == "2":
            frequency_customer = (purchase_orders.groupby("CustomerID")["InvoiceNo"].nunique().reset_index())

            frequency_customer = frequency_customer.rename(columns={"InvoiceNo": "Frequency"})

            most_frequent_customers = frequency_customer.sort_values(by="Frequency",ascending=False)

            print(most_frequent_customers.head())

        elif question == "3":
            reference_date = purchase_orders["InvoiceDate"].max() + pd.Timedelta(days=1)

            recency_customer = (purchase_orders.groupby("CustomerID")["InvoiceDate"].max().reset_index())

            recency_customer["Recency"] = (reference_date - recency_customer["InvoiceDate"]).dt.days

            recency_customer = recency_customer.drop(columns=["InvoiceDate"])

            # Most recent customers have the LOWEST recency
            recency_sort_values = recency_customer.sort_values(by="Recency",ascending=True)

            print(recency_sort_values.head())

        elif question == "4":
            monetary_customer = (purchase_orders.groupby("CustomerID")["OrderValue"].sum().reset_index())

            monetary_customer = monetary_customer.rename(columns={"OrderValue": "MonetaryValue"})

            sorted_monetary_customer = monetary_customer.sort_values(by="MonetaryValue",ascending=False)

            print(sorted_monetary_customer.head())

        elif question == "5":
            customer_sales = (purchase_orders.groupby("CustomerID").agg(Frequency=("InvoiceNo", "nunique"),
                    MonetaryValue=("OrderValue", "sum"),
                    TotalQuantity=("Quantity", "sum"),
                    LastPurchaseDate=("InvoiceDate", "max")).reset_index())

            customer_sales["AverageOrderValue"] = (customer_sales["MonetaryValue"] / customer_sales["Frequency"])

            reference_date = purchase_orders["InvoiceDate"].max() + pd.Timedelta(days=1)

            customer_sales["Recency"] = (reference_date - customer_sales["LastPurchaseDate"]).dt.days

            customer_sales = customer_sales.drop(columns=["LastPurchaseDate"])

            print(customer_sales.head())

        elif question == "back":
            print("Going back...")
            break

        else:
            print("Invalid choice. Please enter 1, 2, 3, 4, 5, or back.")


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
purchase_orders, cancelled_orders, returned_orders = split_order_types(dataset)

print("Purchase orders:", len(purchase_orders))
print("Cancelled orders:", len(cancelled_orders))
print("Returned orders:", len(returned_orders))

purchase_orders.to_csv("purchase_orders.csv", index=False)
cancelled_orders.to_csv("cancelled_orders.csv", index=False)
returned_orders.to_csv("returned_orders.csv", index=False)

print(df.columns)

while True:
    try:
        question = int(input("Enter Your Choice: "))
    except ValueError:
        print("Please enter a number.")
        continue
    if question == 1:
        value(purchase_orders)
