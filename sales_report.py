import pandas as pd
import matplotlib.pyplot as plt
from main import cancelled_orders
from pathlib import Path

TABLEAU_DATA_PATH = Path("tableau_data")
TABLEAU_DATA_PATH.mkdir(parents=True, exist_ok=True)

#Reading the datasets
purchase_orders = pd.read_csv("purchase_orders.csv")
canceled_orders = pd.read_csv("cancelled_orders.csv")
completed_purchases = pd.read_csv("completed_purchase_orders.csv")

def save_tableau_csv(dataframe, filename):
    file_path = TABLEAU_DATA_PATH / filename
    dataframe.to_csv(file_path, index=False)
    print(f"Saved Tableau file: {file_path}")

def revenue(purchase_orders, canceled_orders, completed_purchases):
    # Create revenue values for each row
    total_revenue_purchases = purchase_orders["Quantity"] * purchase_orders["UnitPrice"]
    canceled_revenue_orders = canceled_orders["Quantity"] * canceled_orders["UnitPrice"]

    # Total revenue values
    purchase_revenue = total_revenue_purchases.sum()
    canceled_revenue = canceled_revenue_orders.sum()

    # Cancelled orders are negative, so adding them gives net revenue
    net_revenue = purchase_revenue + canceled_revenue

    print("Revenue of Purchase Orders:", round(purchase_revenue, 2))
    print("Revenue of Canceled Orders:", round(canceled_revenue, 2))
    print("Net Revenue:", round(net_revenue, 2))

    # Average purchase invoice value
    average_order_purchased_value = purchase_revenue / purchase_orders["InvoiceNo"].nunique()

    # Average cancelled invoice value, shown as positive
    average_order_canceled_value = abs(canceled_revenue) / canceled_orders["InvoiceNo"].nunique()

    # Net average invoice value
    total_invoices = (
        purchase_orders["InvoiceNo"].nunique()
        + canceled_orders["InvoiceNo"].nunique()
    )

    net_average_invoice_value = net_revenue / total_invoices

    # Completed purchases
    completed_purchases_order = completed_purchases["Quantity"] * completed_purchases["UnitPrice"]

    # Average completed purchase invoice value
    average_completed_purchase_invoice_value = (completed_purchases_order.sum() / completed_purchases["InvoiceNo"].nunique())

    print("Average Order Purchased Value:", round(average_order_purchased_value, 2))
    print("Average Order Canceled Value:", round(average_order_canceled_value, 2))
    print("Average Completed Purchases Orders:", round(average_completed_purchase_invoice_value, 2))
    print("Total Invoices:", total_invoices)
    print("Net Average Invoice Value:", round(net_average_invoice_value, 2))

    #Highest and lowest invoice values, not row values
    completed_purchases = completed_purchases.copy()
    completed_purchases["RowValue"] = completed_purchases["Quantity"] * completed_purchases["UnitPrice"]

    invoice_purchased_values = (completed_purchases
        .groupby("InvoiceNo")["RowValue"]
        .sum()
        .reset_index(name="InvoiceValue")
    )


    canceled_orders = canceled_orders.copy()
    canceled_orders["RowValue"] = canceled_orders["Quantity"] * canceled_orders["UnitPrice"]

    invoice_canceled_values = (canceled_orders
        .groupby("InvoiceNo")["RowValue"]
        .sum()
        .reset_index(name="CancelledInvoiceValue")
    )

    biggest_sale = invoice_purchased_values["InvoiceValue"].max()
    smallest_sale = invoice_purchased_values["InvoiceValue"].min()

    smallest_canceled = abs(invoice_canceled_values["CancelledInvoiceValue"].max())
    biggest_canceled = abs(invoice_canceled_values["CancelledInvoiceValue"].min())

    print("Biggest Purchase Invoice:", round(biggest_sale, 2))
    print("Smallest Purchase Invoice:", round(smallest_sale, 2))

    print("Biggest Canceled Invoice:", round(biggest_canceled, 2))
    print("Smallest Canceled Invoice:", round(smallest_canceled, 2))

    #The largest invoice values were treated as outliers because the top purchase invoices had matching cancellation invoices with the same values. For example, invoice 581483 had a value of €168,469.60 and was followed by cancellation invoice C581484 with a value of -€168,469.60. This shows why net revenue is more reliable than gross revenue when analysing sales performance.
    #After some further inspection during this stage some orders were canceled after so the base case action it make clean the data by removing matching order values and having one more invoice from purchased and canceled orders
    #Remove fully cancelled purchases so reversed orders do not distort sales metrics or clustering.

    #Over 148 purchases weren't completed and put into a separate csv file called matched_reversed_invoices

    #After removing purchase invoices that appeared to be fully reversed by cancellation invoices, the largest completed purchase invoice was €31,698.16. This gives a more realistic view of completed sales activity than the original gross purchase dataset, where the largest invoice was later cancelled.

    #The average recorded purchase invoice value was €480.87. After removing purchase invoices that appeared to be fully reversed by cancellation invoices, the average completed purchase invoice value was €464.75. This cleaned value gives a more realistic view of successful customer purchases and was used for customer behaviour analysis and clustering.
    print(completed_purchases.columns)

    return net_revenue


#are sales increasing or decreasing overitme
def sales_over_time(completed_purchases, canceled_orders):
    print("Sales Over Time")

    completed_purchases = completed_purchases.copy()
    canceled_orders = canceled_orders.copy()

    # Make sure InvoiceDate is datetime
    completed_purchases["InvoiceDate"] = pd.to_datetime(completed_purchases["InvoiceDate"])
    canceled_orders["InvoiceDate"] = pd.to_datetime(canceled_orders["InvoiceDate"])

    # Create value for each row
    completed_purchases["RowValue"] = (completed_purchases["Quantity"] * completed_purchases["UnitPrice"])
    canceled_orders['RowValue'] = abs(canceled_orders['Quantity']) * canceled_orders['UnitPrice']


    # Create month column for purchases
    completed_purchases["Month"] = (
        completed_purchases["InvoiceDate"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    #create month column for cancellations
    canceled_orders["Month"] = (
        canceled_orders["InvoiceDate"]
        .dt.to_period("M")
        .dt.to_timestamp()
    )

    monthly_cancellations = (
        canceled_orders.groupby("Month")
        .agg(MonthlyRevenue=("RowValue", "sum"),
             TotalInvoices=("InvoiceNo", "nunique"),
             )
        .reset_index())

    monthly_sales = (
        completed_purchases.groupby("Month")
        .agg(
            MonthlyRevenue=("RowValue", "sum"),
            TotalInvoices=("InvoiceNo", "nunique")
            )
            .reset_index())

    # Average purchase invoice value per month
    monthly_sales["AverageInvoiceValue"] = (monthly_sales["MonthlyRevenue"] / monthly_sales["TotalInvoices"])

    # Average cancellation invoice value per month
    monthly_cancellations['AverageInvoiceValue'] = (monthly_cancellations['MonthlyRevenue'] / monthly_cancellations['TotalInvoices'])

    # Round values
    monthly_sales["MonthlyRevenue"] = monthly_sales["MonthlyRevenue"].round(2)
    monthly_sales["AverageInvoiceValue"] = monthly_sales["AverageInvoiceValue"].round(2)

    monthly_cancellations['MonthlyRevenue'] = monthly_cancellations['MonthlyRevenue'].round(2)
    monthly_cancellations['AverageInvoiceValue'] = monthly_cancellations['AverageInvoiceValue'].round(2)

    # Compare first month to last month
    monthly_sales_complete = monthly_sales.iloc[:-1]

    monthly_cancellations_complete = monthly_cancellations.iloc[:-1]

    first_month_revenue = monthly_sales_complete["MonthlyRevenue"].iloc[0]
    last_month_revenue = monthly_sales_complete["MonthlyRevenue"].iloc[-1]

    first_month_loss = monthly_cancellations_complete["MonthlyRevenue"].iloc[0]
    last_month_loss =  monthly_cancellations_complete["MonthlyRevenue"].iloc[-1]

    revenue_change = last_month_revenue - first_month_revenue
    percentage_change = (revenue_change / first_month_revenue) * 100

    revenue_loss = last_month_loss - first_month_loss
    percentage_loss = (revenue_loss / last_month_loss) * 100

    print("First Month Revenue:", round(first_month_revenue, 2))
    print("Last Month Revenue:", round(last_month_revenue, 2))
    print("Revenue Change:", round(revenue_change, 2))
    print("Percentage Change:", round(percentage_change, 2), "%")

    print("================================================")

    print("First Month Loss:", round(first_month_loss, 2))
    print("Last Month Loss:", round(last_month_loss, 2))
    print("Revenue Loss:", round(revenue_loss, 2))
    print("Percentage Loss:", round(percentage_loss, 2), "%")

    if revenue_change > 0:
        print("Sales increased over time.")
    elif revenue_change < 0:
        print("Sales decreased over time.")
    else:
        print("Sales stayed the same over time.")

    plt.figure(figsize=(10, 5))
    plt.plot(monthly_sales_complete["Month"], monthly_sales_complete["MonthlyRevenue"], marker="o")
    plt.title("Monthly Sales Revenue Over Time")
    plt.xlabel("Month")
    plt.ylabel("Revenue")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))
    plt.plot(monthly_cancellations_complete["Month"], monthly_cancellations_complete["MonthlyRevenue"], marker="o")
    plt.title("Monthly Sales loss Over Time")
    plt.xlabel("Month")
    plt.ylabel("loss")
    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.show()

    plt.figure(figsize=(10, 5))

    plt.plot(
        monthly_sales_complete["Month"],
        monthly_sales_complete["MonthlyRevenue"],
        marker="o",
        label="Completed Sales Revenue"
    )

    plt.plot(
        monthly_cancellations_complete["Month"],
        monthly_cancellations_complete["MonthlyRevenue"],
        marker="o",
        label="Cancellation Value"
    )

    plt.title("Monthly Completed Sales vs Cancellation Value")
    plt.xlabel("Month")
    plt.ylabel("Value")
    plt.xticks(rotation=0)
    plt.legend()
    plt.tight_layout()
    plt.show()


    return monthly_sales
    #Sales revenue increased by 105.75% between the first recorded month and the last complete month. The final month was excluded from the trend comparison because it appeared incomplete and caused a misleading drop in the graph.
    #Monthly sales revenue increased by 105.75% between the first complete month and the last complete month analysed. Sales fluctuated during the early months, but revenue increased strongly from September to November, reaching the highest monthly revenue in November. The final incomplete month was excluded to avoid misleading the trend analysis.
#best months and worst months

    #Completed sales revenue increased strongly over time, especially from September to November. Cancellation values fluctuated month to month but remained much lower than completed sales revenue. This suggests that although cancellations caused some revenue loss, they did not change the overall positive sales trend.

#Top countries by completed Revenue
def countries_by_completed_purchases(completed_revenue):
    print("Top Countries by Completed Purchases:")

    completed_purchases = completed_revenue.copy()

    completed_purchases['RowValue'] = (
        completed_purchases["Quantity"] * completed_purchases["UnitPrice"]
    )

    # Group revenue by country
    country_revenue = (
        completed_purchases
        .groupby("Country")
        .agg(
            CompletedRevenue=("RowValue", "sum"),
            TotalInvoices=("InvoiceNo", "nunique"),
            TotalCustomers=("CustomerID", "nunique")
        )
        .reset_index()
    )

    # Average invoice value by country
    country_revenue["AverageInvoiceValue"] = (country_revenue["CompletedRevenue"] / country_revenue["TotalInvoices"])

    # Round values
    country_revenue["CompletedRevenue"] = country_revenue["CompletedRevenue"].round(2)
    country_revenue["AverageInvoiceValue"] = country_revenue["AverageInvoiceValue"].round(2)

    # Sort highest revenue countries first
    country_revenue = country_revenue.sort_values(
        by="CompletedRevenue",
        ascending=False
    )

    save_tableau_csv(country_revenue, "country_revenue.csv")

    print(country_revenue.head(10))

    top_10_countries = country_revenue.head(10)

    plt.figure(figsize=(10, 5))
    plt.barh(top_10_countries["Country"],top_10_countries["CompletedRevenue"]
    )

    plt.title("Top 10 Countries by Completed Revenue")
    plt.xlabel("Completed Revenue")
    plt.ylabel("Country")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

    return country_revenue

    #Completed purchase revenue was grouped by country to identify which markets contributed the most to successful sales. Reversed and cancelled purchases were excluded so the country revenue figures reflect completed customer transactions.

countries_by_completed_purchases(completed_purchases)

#Top Products by completed revenue
def top_products_by_completed_purchases(completed_purchases):
    print("Top Products by Completed Purchases:")

    completed_purchases = completed_purchases.copy()

    # Create value for each row
    completed_purchases["RowValue"] = (completed_purchases["Quantity"] * completed_purchases["UnitPrice"])

    # Group by product
    product_revenue = (completed_purchases.groupby(["StockCode", "Description"]).agg(
            CompletedRevenue=("RowValue", "sum"),
            TotalQuantitySold=("Quantity", "sum"),
            TotalInvoices=("InvoiceNo", "nunique"),
            TotalCustomers=("CustomerID", "nunique")).reset_index()
    )

    # Average revenue per invoice for each product
    product_revenue["AverageInvoiceValue"] = (product_revenue["CompletedRevenue"] / product_revenue["TotalInvoices"])

    # Round values
    product_revenue["CompletedRevenue"] = product_revenue["CompletedRevenue"].round(2)
    product_revenue["AverageInvoiceValue"] = product_revenue["AverageInvoiceValue"].round(2)

    # Sort by highest revenue
    product_revenue = product_revenue.sort_values(by="CompletedRevenue",ascending=False)

    print(product_revenue.head(10))

    top_10_products = product_revenue.head(10)

    plt.figure(figsize=(10, 6))

    plt.barh(top_10_products["Description"],top_10_products["CompletedRevenue"])

    plt.title("Top 10 Products by Completed Revenue")
    plt.xlabel("Completed Revenue")
    plt.ylabel("Product")
    plt.gca().invert_yaxis()
    plt.tight_layout()
    plt.show()

    #Completed purchase revenue was grouped by product to identify the highest earning products. Cancelled and reversed purchases were excluded so the results reflect products that generated successful revenue.

    return product_revenue

#One-Time buyes vs repeat buyers


print("Sales Report of Customer Segmentation")

countries_by_completed_purchases(completed_purchases)

print('=============================================')

top_products_by_completed_purchases(completed_purchases)

print('=============================================')

revenue(purchase_orders, canceled_orders, completed_purchases)

print('=============================================')

sales_over_time(completed_purchases, canceled_orders)

