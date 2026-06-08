import pandas as pd
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score, confusion_matrix, classification_report

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

    #Frequency is in the top 25% because higher frequecny mean more loyalty
    high_frequency = dataset["Frequency"] >= frequency_limit

    #Recency is in the bottom 25% because lower recency the sooner they have purchased something
    recent_customer = dataset["Recency"] <= recency_limit

    #Average is in the top 25% because higher Average means more spent entirely in store
    high_average = dataset["AverageOrderValue"] >= average_limit

    #Monetary Value is in the top 25& because more overall spending means values customer
    high_monetary_value = dataset["MonetaryValue"] >= high_monetary_value

    # Starting everyone as Inactive Customer by default
    dataset['Customer_Status'] = 'Inactive'

    dataset.loc[high_frequency & recent_customer & high_average & high_monetary_value, "Customer_Status"] = 'VIP'

    dataset.loc[high_frequency & recent_customer & ~high_average, "Customer_Status"] = 'Loyal'

    dataset.loc[high_frequency & ~recent_customer, "Customer_Status"] = 'Risk'

    dataset.loc[~high_frequency & recent_customer, "Customer_Status"] = 'New'

    print(dataset['Customer_Status'].head(20))
    print(dataset.columns)

percentile_customer_based_segmentation(dataset)

#Mapping all customer status to use for K-means clustering for human visualisation
status_mapping ={
    "VIP": 5,
    "Loyal": 4,
    "Risk": 3,
    "New": 2,
    "Inactive": 1
}

dataset['Customer_Status'] = dataset['Customer_Status'].map(status_mapping)

df = pd.DataFrame(dataset)
print(df.dtypes)

#Dataset columns used for Kmeans clustering
X = dataset[['Frequency', 'Recency', 'AverageOrderValue', 'MonetaryValue']]

#Scaling our data
scaler = StandardScaler()
scaled_data = scaler.fit_transform(X)

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)

df['Cluster'] = kmeans.fit_predict(scaled_data)

print("K Means clustering completed......")
print(df, "<======= clustered data")
print(df[["CustomerID","Frequency","Recency","AverageOrderValue","MonetaryValue","Customer_Status","Cluster"]].head(20))

print(pd.crosstab(df["Customer_Status"], df["Cluster"]))

cluster_map = (df.groupby("Cluster")["Customer_Status"]
               .agg(lambda x: x.value_counts().idxmax())
               .to_dict()
               )

df["Predicted_Status"] = df["Cluster"].map(cluster_map)

accuracy = (df["Predicted_Status"] == df["Customer_Status"]).mean()

print("Cluster mapping:", cluster_map)
print("Accuracy:", round(accuracy * 100, 2), "%")

#silhouette score
score = silhouette_score(scaled_data, df["Cluster"])
print("Silhouette Score:", score)

#Confusion Matrix
print(confusion_matrix(df["Customer_Status"], df["Predicted_Status"]))
print(classification_report(df["Customer_Status"], df["Predicted_Status"]))


#The K-Means model achieved a silhouette score of 0.60, suggesting that the customer groups are reasonably well separated. However, when compared against the existing Customer_Status label, the clusters only achieved 64.94% agreement. This shows that the natural customer groups found by K-Means do not fully match the manually assigned customer status categories.
#After removing fully reversed purchase invoices, the K-Means cluster comparison score slightly decreased. However, the cleaned dataset was considered more reliable because reversed transactions no longer inflated customer value. Since K-Means is an unsupervised method, the customer status accuracy score was used only as a comparison measure, not as the main measure of model success.