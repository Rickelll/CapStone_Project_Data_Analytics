import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
from datetime import datetime as dt


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
    st.title('Invoice Lookup')

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

            display_df = matching_code[
                [
                    "InvoiceNo",
                    "CustomerID",
                    "InvoiceDate",
                    "Country",
                    "Description",
                    "Quantity",
                    "UnitPrice",
                    "Order_Value"
                ]
            ].copy().reset_index(drop=True)

            # Format date BEFORE showing the dataframe
            display_df["InvoiceDate"] = pd.to_datetime(display_df["InvoiceDate"])
            display_df["InvoiceDate"] = display_df["InvoiceDate"].dt.strftime("%d/%m/%Y")

            table_event = st.dataframe(
                display_df,
                use_container_width=True,
                hide_index=True,
                on_select="rerun",
                selection_mode="single-row"
            )

            selected_row = table_event.selection.rows

            if selected_row:
                selected_row_number = selected_row[0]
                selected_data = display_df.iloc[selected_row_number]

                inspect_button = st.button("Inspect")

                if inspect_button:
                    st.write(
                        f"This order was placed on {selected_data['InvoiceDate']}. \n"
                        f"The customer bought {selected_data['Quantity']} of \n"
                        f"{selected_data['Description']} at €{selected_data['UnitPrice']:.2f} per item, \n"
                        f"giving this Order a value of €{selected_data['Order_Value']:.2f}."
                    )
            else:
                st.info("Click one row in the table, then press Inspect.")

if __name__ == '__main__':
    if selected=="Home":
        home_page()
    elif selected=="Customer Order Search":
        search_customer_order()










