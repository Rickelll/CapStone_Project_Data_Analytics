import pandas as pd

from main import cancelled_orders

#Reading the datasets
purchase_orders = pd.read_csv("purchase_orders.csv")
canceled_orders = pd.read_csv("cancelled_orders.csv")
completed_purchases = pd.read_csv("completed_purchase_orders.csv")

print(purchase_orders.columns)
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

    print("Average Order Purchased Value:", round(average_order_purchased_value, 2))
    print("Average Order Canceled Value:", round(average_order_canceled_value, 2))
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

    biggest_purchase_invoice_max = invoice_purchased_values.sort_values(
        by="InvoiceValue", ascending=False
    ).head(5)

    biggest_purchase_invoice = invoice_purchased_values.sort_values(
        by="InvoiceValue", ascending=True
    ).head(5)
    print(biggest_purchase_invoice_max)
    print(biggest_purchase_invoice)

    biggest_canceled_invoice_max = invoice_canceled_values.sort_values(
        by="CancelledInvoiceValue", ascending=False
    ).head(5)

    biggest_canceled_invoice = invoice_canceled_values.sort_values(
        by="CancelledInvoiceValue", ascending=True
    ).head(5)
    print(biggest_canceled_invoice_max)
    print(biggest_canceled_invoice)
    #The largest invoice values were treated as outliers because the top purchase invoices had matching cancellation invoices with the same values. For example, invoice 581483 had a value of €168,469.60 and was followed by cancellation invoice C581484 with a value of -€168,469.60. This shows why net revenue is more reliable than gross revenue when analysing sales performance.
    #After some further inspection during this stage some orders were canceled after so the base case action it make clean the data by removing matching order values and having one more invoice from purchased and canceled orders
    #Remove fully cancelled purchases so reversed orders do not distort sales metrics or clustering.
    return net_revenue


#are sales increasing or decreasing overitme

#best months and worst months



revenue(purchase_orders, canceled_orders, completed_purchases)