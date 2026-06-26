## Customer Sales Analytics Dashboard

# Project Overview

This project is a data analytics capstone project focused on analysing customer sales behaviour from a retail transaction dataset.

The original dataset used in this project was called customer_segmentation_data.csv.

The main goal of the project was to take raw customer transaction data and turn it into useful business insights. The project looks at sales revenue, cancellations, completed purchases, customer value, customer segmentation, product performance, country performance, and order value prediction.

The final output is an interactive Streamlit dashboard supported by Tableau visualisations and Python-based analysis. The project combines data cleaning, exploratory data analysis, customer segmentation, machine learning, and dashboard storytelling.

* Python
* Pandas
* Scikit-learn
* Tableau
* Streamlit
* Git / GitHub
* Jupyter Notebook
* AI assistant support for debugging, planning, and explanation

# Main Business Questions 

The project was designed around the following business questions:

* How much revenue did the business generate?
* How much revenue was lost through cancellations?
* Are sales increasing or decreasing over time?
* Which countries generate the most completed revenue?
* Which products generate the most completed revenue?
* Which customer groups are most valuable?
* Can previous customer behaviour help predict future order value?
* How can customer and invoice-level data be explored in an interactive dashboard?

These questions helped guide the full project, from data cleaning to the final dashboard design.

# Dataset Description

The dataset contains retail transaction data. Each row represents a product line inside an invoice. This means one invoice can appear more than once if a customer bought multiple products in the same order.

The main columns in the dataset were:

* InvoiceNo - the invoice or order number
* StockCode - the product code
* Description - the product description
* Quantity - the number of items purchased or cancelled
* InvoiceDate - the date and time of the transaction
* UnitPrice - the price per item
* CustomerID - an anonymous customer identifier
* Country - the country linked to the order

The dataset included normal purchases, cancelled invoices, missing values, repeated invoice rows, and customers with multiple purchases over time.

Because of this, the raw data needed to be cleaned and reshaped before it could be used for reliable analysis.

# Project Structure

The project was split into different Python files to keep the work organised.