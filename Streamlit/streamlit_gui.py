import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu


st.sidebar.header('Customer Segmentation Analysis')

with st.sidebar:
    selected = option_menu(
        menu_title = "Menu",
        options = ["Home","Customer Order Search","About"]
    )

def load_order_data():
    purchased_orders = pd.read_csv('completed_purchase_orders.csv')

    cancelled_orders = pd.read_csv('cancelled_orders.csv')

    return purchased_orders, cancelled_orders

def home_page():
    st.header('Home Page')
    st.write("This app analyses customer sales data to understand business revenue, cancellation losses, top-performing countries/products, customer value groups, and order value prediction using machine learning.")

    st.subheader('Main Questions Answered')

    st.write('How much revenue did the business make?')

    st.write('Are sales increasing or decreasing?')

    st.write('How much revenue was lost through cancellations?')

    st.write('Which countries produce the most revenue?')

    st.write('Which customer groups are most valuable?')

    st.write('How well did the regression model predict order value?')


def search_customer_order():
    st.title('Customer Order Search')

    purchased_orders, cancelled_orders = load_order_data()

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

if __name__ == '__main__':
    if selected=="Home":
        home_page()
    elif selected=="Customer Order Search":
        search_customer_order()










