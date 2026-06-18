import streamlit as st
import pandas as pd

st.title('Customer Order Search')

def load_data():
    purchased_orders = pd.read_csv('completed_purchase_orders.csv')

    cancelled_orders = pd.read_csv('cancelled_orders.csv')

    return purchased_orders, cancelled_orders

def search_customer_order():
    purchased_orders, cancelled_orders = load_data()

    order_type = st.selectbox("Select Order Type", ["Purchased Orders", "Cancelled Orders"])

    if order_type == "Purchased Orders":
        data = purchased_orders
    else:
        data = cancelled_orders

    data['InvoiceNo'] = data['InvoiceNo'].astype(str).str.strip().str.upper()

    invoice_no = st.text_input('What is your Invoice Number?').strip().upper()

    if invoice_no:
        matching_code = data[data['InvoiceNo'] == invoice_no]

        if not matching_code.empty:

            st.success('Your Orders have been found!!!')

            matching_code['Order_Value'] = matching_code['Quantity'] * matching_code['UnitPrice']

            st.write("Order Details: ")



            dataframe = st.dataframe(matching_code[['InvoiceNo','CustomerID','InvoiceDate','Country',
                                   'Description', 'Quantity', 'UnitPrice','Order_Value']].head(5))
            st.write(dataframe)

        else:
            st.error(f'No Order Found for Invoice Number: {invoice_no}')




search_customer_order()








