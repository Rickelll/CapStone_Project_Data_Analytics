import pandas as pd

dataset = pd.read_csv('customer_order_sales_data.csv')

#checking min and max frequency to be able see a good range
#print(dataset['Frequency'].min(), dataset['Frequency'].max())

VIP = []

# Create customer limits using quantiles
# 0.75 means the top 25% of customers
# 0.25 means the lowest 25% of customers
def percentile_customer_based_segmentation(dataset):
    #using quantile to distribute evenly dataset
    frequency_limit = dataset["Frequency"].quantile(0.75)
    recency_limit = dataset["Recency"].quantile(0.25)
    average_limit = dataset["AverageOrderValue"].quantile(0.75)
    high_monetary_value = dataset["MonetaryValue"].quantile(0.25)

    # Starting everyone as Inactive Customer by default
    dataset['Customer_Status'] = 'Inactive'

    #Frequency is in the top 25% because higher frequecny mean more loyalty
    high_frequency = dataset["Frequency"] >= frequency_limit

    #Recency is in the bottom 25% because lower recency the sooner they have purchased something
    recent_customer = dataset["Recency"] <= recency_limit

    #Average is in the top 25% because higher Average means more spent entirely in store
    high_average = dataset["AverageOrderValue"] >= average_limit

    #Monetary Value is in the top 25& because more overall spending means values customer
    high_monetary_value = dataset["MonetaryValue"] >= high_monetary_value


    vip_customer = dataset[high_frequency & recent_customer & high_average & high_monetary_value]

    loyal_customer = dataset[high_frequency & recent_customer & ~high_average]

    at_risk_customer = dataset[high_frequency & ~recent_customer]

    new_customer = dataset[~high_frequency & recent_customer]

    inactive_customer = dataset[~high_frequency & ~recent_customer]

    print("Length of data: ",len(dataset))
    print("VIP customers: ",len(vip_customer))
    print("Loyal Customers: ",len(loyal_customer))
    print("At risk of losing : ",len(at_risk_customer))
    print("New customers: ",len(new_customer))
    print("Inactive Customers: ",len(inactive_customer))

percentile_customer_based_segmentation(dataset)
