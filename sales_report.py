import pandas as pd

from main import cancelled_orders

#Reading the datasets
purchase_orders = pd.read_csv("purchase_orders.csv")
cancelled_orders = pd.read_csv("cancelled_orders.csv")

print(purchase_orders.columns)
def revenue(purchase_orders, cancelled_orders):
    #Total Revenue from valid purchases, order_total from purchases - cancelled_orders_total from cancelled
    total_revenue_purchases = purchase_orders['Quantity'] * purchase_orders['UnitPrice']

    canceled_orders = cancelled_orders['Quantity'] * cancelled_orders['UnitPrice']

    #Because the quantity in the datasets are negative we have to add them to the total revenue
    total_revenue = total_revenue_purchases.sum() + canceled_orders.sum()
    print("Revenue of Purchase Orders:", total_revenue_purchases.sum())
    print("Revenue of Canceled Orders:", canceled_orders.sum())
    print("Net Revenue: ", total_revenue.round(2))
    return total_revenue

#average order value



#highest and lowest sales

#are sales increasing or decreasing overitme

#best months and worst months



revenue(purchase_orders, cancelled_orders)