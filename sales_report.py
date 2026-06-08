import pandas as pd

from main import cancelled_orders

#Reading the datasets
purchase_orders = pd.read_csv("purchase_orders.csv")
canceled_orders = pd.read_csv("cancelled_orders.csv")

print(purchase_orders.columns)
def revenue(purchase_orders, canceled_orders):
    #Total Revenue from valid purchases, order_total from purchases - cancelled_orders_total from cancelled
    total_revenue_purchases = purchase_orders['Quantity'] * purchase_orders['UnitPrice']

    canceled_revenue_orders = canceled_orders['Quantity'] * canceled_orders['UnitPrice']

    #Because the quantity in the datasets are negative we have to add them to the total revenue
    total_revenue = total_revenue_purchases.sum() + canceled_revenue_orders.sum()
    print("Revenue of Purchase Orders:", total_revenue_purchases.sum())
    print("Revenue of Canceled Orders:", canceled_revenue_orders.sum())
    print("Net Revenue: ", total_revenue.round(2))

    # average order value
    average_order_purchased_value = total_revenue_purchases.sum() / purchase_orders['InvoiceNo'].nunique()

    average_order_canceled_value = abs(canceled_revenue_orders.sum()) / canceled_orders['InvoiceNo'].nunique()

    total_invoices = purchase_orders['InvoiceNo'].nunique() + canceled_orders['InvoiceNo'].nunique()

    average_order_value_sum = total_revenue.sum() / total_invoices

    print("Average Order Purchased Value:", average_order_purchased_value.round(2))
    print("Average Order Canceled Value:", average_order_canceled_value.round(2))
    print("Total Invoices:", total_invoices)
    print("Average Order Value:", average_order_value_sum.round(2))
    return total_revenue

#average order value



#highest and lowest sales

#are sales increasing or decreasing overitme

#best months and worst months



revenue(purchase_orders, canceled_orders)