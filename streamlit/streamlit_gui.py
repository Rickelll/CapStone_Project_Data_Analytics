import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
import re

st.set_page_config(
    page_title="Capstone Dashboard",
    layout="wide"
)

st.markdown("""
<style>
/* ================================
   MAIN APP THEME
================================ */

/* Full app background */
.stApp {
    background-color: #0F172A;
    color: #F8FAFC;
}

/* Main content spacing */
.block-container {
    max-width: 95% !important;
    padding-top: 2rem !important;
    padding-left: 2rem !important;
    padding-right: 2rem !important;
}

/* Top bar */
header[data-testid="stHeader"] {
    background-color: #000000;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #000000;
    border-right: 1px solid #1E293B;
}

section[data-testid="stSidebar"] * {
    color: #F8FAFC !important;
}

/* Hide Streamlit menu/footer if you want cleaner app */
#MainMenu {
    visibility: hidden;
}

footer {
    visibility: hidden;
}

/* ================================
   HEADERS
================================ */

.page-header {
    background: linear-gradient(135deg, #000000, #111827, #1E293B);
    padding: 38px 28px;
    border-radius: 20px;
    margin-bottom: 30px;
    text-align: center;
    color: #F8FAFC;
    box-shadow: 0px 6px 18px rgba(0,0,0,0.35);
    border: 1px solid #334155;
}

.page-header h1 {
    font-size: 44px;
    font-weight: 850;
    margin-bottom: 10px;
    color: #F8FAFC;
}

.page-header p {
    font-size: 18px;
    color: #CBD5E1;
    margin: 0;
}

.section-heading {
    text-align: center;
    color: #F8FAFC;
    font-size: 30px;
    font-weight: 800;
    margin-top: 35px;
    margin-bottom: 20px;
}

.center-text {
    text-align: center;
    color: #CBD5E1;
    font-size: 17px;
    line-height: 1.6;
}

/* ================================
   CARDS / CHART AREAS
================================ */

.chart-title {
    text-align: center;
    color: #F8FAFC;
    font-size: 19px;
    font-weight: 800;
    margin-bottom: 10px;
}

/* Streamlit bordered containers */
div[data-testid="stVerticalBlockBorderWrapper"] {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 16px !important;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.28);
}

/* Divider */
hr {
    border-color: #334155 !important;
}

/* ================================
   TEXT
================================ */

h1, h2, h3, h4, h5, h6, p, label, span {
    color: #F8FAFC;
}

/* Muted markdown text */
div[data-testid="stMarkdownContainer"] {
    color: #CBD5E1;
}

/* ================================
   INPUTS
================================ */

.stTextInput input {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

.stTextInput input:focus {
    border-color: #38BDF8 !important;
    box-shadow: 0 0 0 1px #38BDF8 !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
    border: 1px solid #334155 !important;
    border-radius: 10px !important;
}

/* Multiselect */
div[data-baseweb="tag"] {
    background-color: #2563EB !important;
    color: white !important;
}

/* ================================
   BUTTONS
================================ */

.stButton > button {
    background-color: #2563EB;
    color: #FFFFFF;
    border: none;
    border-radius: 12px;
    padding: 0.65rem 1.3rem;
    font-weight: 800;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #1D4ED8;
    color: #FFFFFF;
    transform: translateY(-1px);
}

/* ================================
   METRICS
================================ */

div[data-testid="stMetric"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 16px;
    padding: 18px;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.25);
}

div[data-testid="stMetricLabel"] {
    color: #CBD5E1 !important;
}

div[data-testid="stMetricValue"] {
    color: #38BDF8 !important;
}

/* ================================
   TABLES
================================ */

div[data-testid="stDataFrame"] {
    border: 1px solid #334155;
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0px 4px 14px rgba(0,0,0,0.25);
}

/* ================================
   ALERT BOXES
================================ */

div[data-testid="stAlert"] {
    border-radius: 14px;
    border: 1px solid #334155;
}

/* ================================
   EXPANDERS / DIALOGS
================================ */

div[data-testid="stExpander"] {
    background-color: #1E293B;
    border: 1px solid #334155;
    border-radius: 14px;
}

/* Make links visible */
a {
    color: #38BDF8 !important;
}
</style>
""", unsafe_allow_html=True)

st.sidebar.header('Customer Segmentation Analysis')


sales_dashboard_embed_code = '''<div class='tableauPlaceholder' id='viz1782000930954' style='position: relative'><noscript><a href='#'><img alt='Sales Performance Dahsboard ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;SalesPerformanceDahsboard&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;SalesPerformanceDahsboard' /><param name='tabs' value='no' /><param name='toolbar' value='no' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;SalesPerformanceDahsboard&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782000930954');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else { vizElement.style.width='100%';vizElement.style.height='1727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

gross_revenue_kpi = '''<div class='tableauPlaceholder' id='viz1782153926146' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;GrossRevenueKPI&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;GrossRevenueKPI' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;GrossRevenueKPI&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782153926146');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

net_revenue_kpi = '''<div class='tableauPlaceholder' id='viz1782153942545' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;NetRevenueKPI&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;NetRevenueKPI' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;NetRevenueKPI&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782153942545');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

revenue_lost_kpi = '''<div class='tableauPlaceholder' id='viz1782153963745' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;RevenueLostKPI&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;RevenueLostKPI' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;RevenueLostKPI&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782153963745');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

revenue_growth_kpi = '''<div class='tableauPlaceholder' id='viz1782153982689' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;RevenueGrowthKPI&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;RevenueGrowthKPI' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;RevenueGrowthKPI&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782153982689');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

average_invoices_kpi = '''<div class='tableauPlaceholder' id='viz1782154017769' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;AverageCompletedInvoice&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;AverageCompletedInvoice' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;AverageCompletedInvoice&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154017769');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

total_invoices_kpi = '''<div class='tableauPlaceholder' id='viz1782154036000' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;TotalInvoices&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;TotalInvoices' /><param name='tabs' value='yes' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;TotalInvoices&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154036000');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

monthly_completed_cancelled_revenue = '''<div class='tableauPlaceholder' id='viz1782154071827' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;4X&#47;4XT3CS59S&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;4XT3CS59S' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;4X&#47;4XT3CS59S&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154071827');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

top10_countries_by_completed_revenue = '''<div class='tableauPlaceholder' id='viz1782154104940' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;SD&#47;SDQ98PC7X&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;SDQ98PC7X' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;SD&#47;SDQ98PC7X&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154104940');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

top10_products_by_completed_revenue = '''<div class='tableauPlaceholder' id='viz1782154118658' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;4P&#47;4PBYHBWFB&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;4PBYHBWFB' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;4P&#47;4PBYHBWFB&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154118658');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

total_customers_kpi = '''<div class='tableauPlaceholder' id='viz1782154132256' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;G3&#47;G36Z74JWH&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;G36Z74JWH' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;G3&#47;G36Z74JWH&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154132256');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

vip_customers_kpi = '''<div class='tableauPlaceholder' id='viz1782154144710' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;34&#47;342S4SJRS&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;342S4SJRS' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;34&#47;342S4SJRS&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154144710');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

loyal_customers_kpi = '''<div class='tableauPlaceholder' id='viz1782154161580' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;JP&#47;JP9BWXQYC&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;JP9BWXQYC' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;JP&#47;JP9BWXQYC&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154161580');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

at_risk_customers_kpi = '''<div class='tableauPlaceholder' id='viz1782154178385' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;46&#47;46YYDJYFT&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;46YYDJYFT' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;46&#47;46YYDJYFT&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154178385');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

customer_group_total_value = '''<div class='tableauPlaceholder' id='viz1782154194859' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;J9&#47;J9FHRSZND&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;J9FHRSZND' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;J9&#47;J9FHRSZND&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154194859');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

customer_group_total_per_customer = '''<div class='tableauPlaceholder' id='viz1782154214552' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;ZF&#47;ZF4F38N9D&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;ZF4F38N9D' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;ZF&#47;ZF4F38N9D&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154214552');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

mean_absolute_error_kpi = '''<div class='tableauPlaceholder' id='viz1782154242064' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Z5&#47;Z59FJ8WJY&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;Z59FJ8WJY' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Z5&#47;Z59FJ8WJY&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154242064');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

r2_score_kpi = '''<div class='tableauPlaceholder' id='viz1782154256225' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;H6&#47;H6HHPHCM7&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;H6HHPHCM7' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;H6&#47;H6HHPHCM7&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154256225');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

rmse_kpi = '''<div class='tableauPlaceholder' id='viz1782154274304' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;43&#47;43HBWQ7XZ&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;43HBWQ7XZ' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;43&#47;43HBWQ7XZ&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154274304');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

regression_model_prediction = '''<div class='tableauPlaceholder' id='viz1782154300066' style='position: relative'><noscript><a href='#'><img alt=' ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;85&#47;85FJMNKW2&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='path' value='shared&#47;85FJMNKW2' /> <param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;85&#47;85FJMNKW2&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782154300066');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''


def centered_title(text):
    st.markdown(
        f"<h1 style='text-align: center;'>{text}</h1>",
        unsafe_allow_html=True
    )


def page_header(title, subtitle=""):
    st.markdown(
        f"""
        <div class="page-header">
            <h1>{title}</h1>
            <p>{subtitle}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


def section_header(text):
    st.markdown(
        f"<h2 class='section-heading'>{text}</h2>",
        unsafe_allow_html=True
    )


def clean_tableau_embed(embed_code, height):
    # Hide Tableau controls
    embed_code = re.sub(
        r"<param\s+name=['\"]tabs['\"]\s+value=['\"]yes['\"]\s*/?>",
        "<param name='tabs' value='no' />",
        embed_code,
        flags=re.IGNORECASE
    )

    embed_code = re.sub(
        r"<param\s+name=['\"]toolbar['\"]\s+value=['\"]yes['\"]\s*/?>",
        "<param name='toolbar' value='no' />",
        embed_code,
        flags=re.IGNORECASE
    )

    embed_code = re.sub(
        r"<param\s+name=['\"]display_count['\"]\s+value=['\"]yes['\"]\s*/?>",
        "<param name='display_count' value='no' />",
        embed_code,
        flags=re.IGNORECASE
    )

    # Add showVizHome=no
    if "showVizHome" not in embed_code:
        embed_code = re.sub(
            r"(<param\s+name=['\"]embed_code_version['\"]\s+value=['\"]3['\"]\s*/?>)",
            r"\1 <param name='showVizHome' value='no' />",
            embed_code,
            count=1,
            flags=re.IGNORECASE
        )

    # Get the Tableau placeholder ID
    id_match = re.search(
        r"<div class=['\"]tableauPlaceholder['\"] id=['\"]([^'\"]+)['\"]",
        embed_code
    )

    if not id_match:
        return embed_code

    viz_id = id_match.group(1)

    # Replace Tableau's generated sizing script with our own consistent one
    new_script = f"""
    <script type='text/javascript'>
        var divElement = document.getElementById('{viz_id}');
        divElement.style.width = '100%';
        divElement.style.margin = '0 auto';
        divElement.style.textAlign = 'center';

        var vizElement = divElement.getElementsByTagName('object')[0];
        vizElement.style.width = '100%';
        vizElement.style.height = '{height}px';
        vizElement.style.margin = '0 auto';
        vizElement.style.display = 'block';

        var scriptElement = document.createElement('script');
        scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';
        vizElement.parentNode.insertBefore(scriptElement, vizElement);
    </script>
    """

    embed_code = re.sub(
        r"<script type=['\"]text/javascript['\"]>[\s\S]*?</script>",
        new_script,
        embed_code,
        flags=re.IGNORECASE
    )

    return embed_code

def normal_centered_text(text):
    st.markdown(
        f"<p class='center-text'>{text}</p>",
        unsafe_allow_html=True
    )

def tableau_card(title, embed_code, height=250):
    embed_code = clean_tableau_embed(embed_code, height)

    st.markdown(
        f"<div class='chart-title'>{title}</div>",
        unsafe_allow_html=True
    )

    with st.container(border=True):
        components.html(
            embed_code,
            height=height,
            scrolling=False
        )

def centered_text(text):
    st.markdown(
        f"<p style='text-align: center;'>{text}</p>",
        unsafe_allow_html=True
    )

with st.sidebar:
    selected = option_menu(
        menu_title="Capstone Dashboard",
        options=[
            "Home",
            "Customer Order Search",
            "Sales Report",
            "Customer Segmentation",
            "Regression Model",
            "About"
        ],
        icons=[
            "house",
            "search",
            "bar-chart",
            "people",
            "graph-up",
            "info-circle"
        ],
        menu_icon="cast",
        default_index=0,
        styles={
            "container": {
                "padding": "0!important",
                "background-color": "#000000"
            },
            "icon": {
                "color": "#38BDF8",
                "font-size": "18px"
            },
            "nav-link": {
                "font-size": "15px",
                "text-align": "left",
                "margin": "4px",
                "color": "#F8FAFC",
                "border-radius": "10px",
                "--hover-color": "#1E293B",
            },
            "nav-link-selected": {
                "background-color": "#2563EB",
                "color": "#FFFFFF",
                "font-weight": "700",
            },
            "menu-title": {
                "color": "#F8FAFC",
                "font-size": "18px",
                "font-weight": "800",
            }
        }
    )

def load_order_data():
    purchased_orders = pd.read_csv('completed_purchase_orders.csv')

    cancelled_orders = pd.read_csv('cancelled_orders.csv')

    return purchased_orders, cancelled_orders

def load_customer_status_data():
    customer_status_data = pd.read_csv('customer_order_sales_data.csv')

    customer_status_data['CustomerID'] = customer_status_data['CustomerID'].astype(str).str.strip()
    return customer_status_data

def format_invoice_date(date):
    date = pd.to_datetime(date)

    day = date.day

    if 11 <= day <= 13:
        suffix = "th"
    elif day % 10 == 1:
        suffix = "st"
    elif day % 10 == 2:
        suffix = "nd"
    elif day % 10 == 3:
        suffix = "rd"
    else:
        suffix = "th"

    return date.strftime(f"{day}{suffix} of %B %Y")

def show_tableau_kpi_card(title, embed_code, height=180):
    st.markdown(
        f"""
        <div style="
            background-color: white;
            border: 1px solid #D1D5DB;
            border-radius: 14px;
            padding: 12px;
            box-shadow: 0px 2px 8px rgba(0,0,0,0.08);
            text-align: center;
            margin-bottom: 15px;
        ">
            <h4 style="
                margin: 0 0 8px 0;
                color: #374151;
                font-size: 16px;
                font-weight: 700;
            ">
                {title}
            </h4>
        </div>
        """,
        unsafe_allow_html=True
    )

    components.html(
        embed_code,
        height=height,
        scrolling=False
    )

def home_page():
    centered_title('Home Page')
    st.write("This app analyses customer sales data to understand business revenue, cancellation losses, top-performing countries/products, customer value groups, and order value prediction using machine learning.")

    st.subheader('Main Questions Answered')

    st.write('How much revenue did the business make?')

    st.write('Are sales increasing or decreasing?')

    st.write('How much revenue was lost through cancellations?')

    st.write('Which countries produce the most revenue?')

    st.write('Which customer groups are most valuable?')

    st.write('How well did the regression model predict order value?')

    st.divider()

    insight_box(
        "Project Summary",
        "This Streamlit app brings together the main outputs of the project: sales performance, cancellation impact, customer segmentation, "
        "and regression model results. Tableau is used for polished dashboard visuals, while Streamlit adds interactive search and explanation."
    )

def about_page():
    centered_title("About This Project")
    centered_text("This project was built using Python, Streamlit, Tableau, and machine learning to analyse customer sales data.")

def insight_box(title, text):
    st.markdown(f"### {title}")
    st.info(text)

@st.dialog("Selected Order Details")
def show_order_popup(selected_data, order_type):
    st.write(f"**Invoice Number:** {selected_data['InvoiceNo']}")
    st.write(f"**Customer ID:** {selected_data['CustomerID']}")
    st.write(f"**Invoice Date:** {selected_data['InvoiceDate']}")
    st.write(f"**Country:** {selected_data['Country']}")
    st.write(f"**Product:** {selected_data['Description']}")
    st.write(f"**Quantity:** {selected_data['Quantity']}")
    st.write(f"**Unit Price:** €{selected_data['UnitPrice']:.2f}")
    st.write(f"**Order Value:** €{selected_data['Order_Value']:.2f}")

    st.write("Order Summary: ")

    if order_type == "Purchased Orders":
        st.write(
            f"This order was placed on {selected_data['InvoiceDate']}. "
            f"The customer bought {abs(selected_data['Quantity'])} of "
            f"{selected_data['Description']} at €{selected_data['UnitPrice']:.2f} per item, "
            f"giving this order a value of €{abs(selected_data['Order_Value']):.2f}."
        )

    elif order_type == "Cancelled Orders":
        st.write(
            f"This cancellation was recorded on {selected_data['InvoiceDate']}. "
            f"The customer cancelled {abs(selected_data['Quantity'])} of "
            f"{selected_data['Description']} at €{selected_data['UnitPrice']:.2f} per item, "
            f"meaning €{abs(selected_data['Order_Value']):.2f} was refunded or lost from revenue."
        )

def show_customer_mini_dashboard(customer_id, customer_status_data, purchased_orders):
    customer_status_data = customer_status_data.copy()
    purchased_orders = purchased_orders.copy()

    customer_status_data["CustomerID"] = (
        pd.to_numeric(customer_status_data["CustomerID"], errors="coerce")
        .astype("Int64")
        .astype(str)
    )

    purchased_orders["CustomerID"] = (
        pd.to_numeric(purchased_orders["CustomerID"], errors="coerce")
        .astype("Int64")
        .astype(str)
    )

    customer_details = customer_status_data[
        customer_status_data["CustomerID"] == customer_id
    ]

    customer_orders = purchased_orders[
        purchased_orders["CustomerID"] == customer_id
    ].copy()

    if customer_details.empty:
        st.warning("Customer Not Found")
        return

    customer_row = customer_details.iloc[0]

    if not customer_orders.empty:
        customer_orders["InvoiceDate"] = pd.to_datetime(customer_orders["InvoiceDate"])

        customer_orders["Order_Value"] = (
            customer_orders["Quantity"] * customer_orders["UnitPrice"]
        )

        last_purchase_date = customer_orders["InvoiceDate"].max()
        last_purchase_date = format_invoice_date(last_purchase_date)

        total_orders = customer_orders["InvoiceNo"].nunique()
        total_spent = customer_orders["Order_Value"].sum()
    else:
        last_purchase_date = "No completed purchase found"
        total_orders = 0
        total_spent = 0

    st.success("Customer Found!")

    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)

    col1.metric("Customer Status", customer_row["Customer_Status"])
    col2.metric("Recency", f"{customer_row['Recency']} days ago")
    col3.metric("Total Orders", int(total_orders))
    col4.metric("Total Spent", f"€{total_spent:,.2f}")

    centered_text("Customer Details:")

    display_df = pd.DataFrame({
        "Metric": [
            "Customer ID",
            "Customer Status",
            "Frequency",
            "Recency",
            "Total Quantity",
            "Average Order Value",
            "Monetary Value"
        ],
        "Value": [
            customer_row["CustomerID"],
            customer_row["Customer_Status"],
            customer_row["Frequency"],
            f"{customer_row['Recency']} days ago",
            customer_row["TotalQuantity"],
            f"€{customer_row['AverageOrderValue']:,.2f}",
            f"€{customer_row['MonetaryValue']:,.2f}"
        ]
    })

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

def search_customer_order():
    page_header('Invoice Lookup',"Search CustomerID for customer history and "
                                 "Search Invoice Number for Customer Orders")

    st.divider()

    purchased_orders, cancelled_orders = load_order_data()

    customer_status_data = load_customer_status_data()

    left, middle_left, center,middle_right, right = st.columns([0.5, 2, 1 ,2,  0.5])

    with middle_left:
        st.subheader("CustomerID")
        customer_id = st.text_input("Search Customer ID").strip()

        if customer_id:
            show_customer_mini_dashboard(
                customer_id,
                customer_status_data,
                purchased_orders
            )

    with middle_right:
        st.subheader('Invoice Lookup')
        order_type = st.selectbox("Select Order Type", ["Purchased Orders", "Cancelled Orders"])

    if order_type == "Purchased Orders":
        data = purchased_orders.copy()
    else:
        data = cancelled_orders.copy()

    data['InvoiceNo'] = data['InvoiceNo'].astype(str).str.strip().str.upper()

    with middle_right:
        invoice_no = st.text_input('What is your Invoice Number?').strip().upper()

    with middle_right:
        if invoice_no:
            invoice_match = data[data['InvoiceNo'] == invoice_no].copy()

            if not invoice_match.empty:

                st.success('Your Orders have been found!!!')

                invoice_match['Order_Value'] = invoice_match['Quantity'] * invoice_match['UnitPrice']

                st.write("Order Details: ")

                display_df = invoice_match[
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
                display_df["InvoiceDate"] = display_df["InvoiceDate"].apply(format_invoice_date)

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

                    left, middle, right = st.columns([1, 1, 1])

                    with middle_right:
                        inspect_button = st.button("Inspect")

                        if inspect_button:
                            show_order_popup(selected_data, order_type)
                        else:
                            st.info("Click one row in the table, then press Inspect.")

            else:
                st.error("No Invoice number Recognized or Invoice Number Doesn't exist.")
    st.divider()

    insight_box(
        "Invoice Lookup Insight",
        "This page allows individual customer orders to be inspected in detail. "
        "The customer search gives a quick summary of customer value and status, while the invoice lookup connects high-level sales results "
        "back to the original transaction rows."
    )

def sales_report():
    page_header(
        "Sales Report",
        "Main business performance from completed sales and cancellations."
    )

    section_header("Key Sales Metrics")

    col1, col2, col3 = st.columns(3)

    left, middle, right = st.columns([1, 10, 1])

    with col1:
        tableau_card("Gross Revenue", gross_revenue_kpi, height=220)

    with col2:
        tableau_card('Net Revenue', net_revenue_kpi, height=220)

    with col3:
        tableau_card('Revenue Lost', revenue_lost_kpi, height=220)

    st.divider()

    section_header("Key Sales Metrics")

    col4, col5, col6 = st.columns(3)

    with col4:
        tableau_card('Revenue Growth', revenue_growth_kpi, height=220)

    with col5:
        tableau_card('Average Invoices', average_invoices_kpi, height=220)

    with col6:
        tableau_card('Total Invoices', total_invoices_kpi, height=220)

    st.divider()

    section_header("MAIN CHART")

    tableau_card('Monthly Revenue', monthly_completed_cancelled_revenue, height=700)

    st.divider()

    section_header("BOTTOM ROW CHART")

    col7, col8 = st.columns(2)

    with col7:
        tableau_card('Top 10 Countries by Completed Revenue', top10_countries_by_completed_revenue, height=500)

    with col8:
        tableau_card('Top 10 Products by Completed Revenue', top10_products_by_completed_revenue, height=500)

    st.divider()

    insight_box(
        "Sales Insight",
        "The sales dashboard shows that completed revenue increased strongly over the period. "
        "Although cancellations caused revenue loss, they did not stop the overall upward sales trend. "
        "The top country and product charts also show where most completed revenue came from."
    )

def customer_segmentation():
    page_header("Customer Segmentation","Customers were grouped using frequency, recency, average order value, and monetary value.")

    st.divider()

    section_header("KPI Overview")

    col1, col2, col3, col4 = st.columns(4, gap="large")

    with col1:
        tableau_card('Total Customers', total_customers_kpi, height=220)

    with col2:
        tableau_card('Vip Customers', vip_customers_kpi, height=220)

    with col3:
        tableau_card('Loyal Customers',loyal_customers_kpi, height=220)

    with col4:
        tableau_card('Risk of Losing Customers', at_risk_customers_kpi, height=220)

    st.divider()

    section_header("Customer Value Charts")

    col5, col6 = st.columns(2, gap="large")

    with col5:
        tableau_card('Customer Group Monetary Value', customer_group_total_value, height=600)

    with col6:
        tableau_card('Average Value Per Customer Group', customer_group_total_per_customer, height=600)

    st.divider()

    section_header("Customer Status Filter")

    customer_status_data = load_customer_status_data()

    status_options = sorted(
        customer_status_data["Customer_Status"].dropna().unique()
    )

    selected_statuses = st.multiselect(
        "Filter by Customer Status",
        status_options,
        default=status_options
    )

    if selected_statuses:
        filtered_customers = customer_status_data[
            customer_status_data["Customer_Status"].isin(selected_statuses)
        ].copy()
    else:
        filtered_customers = customer_status_data.copy()

    display_df = filtered_customers[
        [
            "CustomerID",
            "Frequency",
            "Recency",
            "TotalQuantity",
            "AverageOrderValue",
            "MonetaryValue",
            "Customer_Status"
        ]
    ].copy()

    display_df = display_df.drop_duplicates(subset=["CustomerID"])

    display_df["Recency"] = display_df["Recency"].astype(int).astype(str) + " days ago"

    st.write(f"Showing {len(display_df)} customers")

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    st.divider()

    insight_box(
        "Customer Segmentation Insight",
        "Customers were grouped based on frequency, recency, average order value, and monetary value. "
        "This helps identify which customer groups are most valuable, which customers are loyal, "
        "and which customers may need attention because they have not purchased recently."
    )

def regression_model():
    page_header("Regression Model")

    section_header("KPI ROW")

    col1, col2, col3 = st.columns(3)

    with col1:
        tableau_card('Mean Absolute Error', mean_absolute_error_kpi, height=220)

    with col2:
        tableau_card('RMSE' , rmse_kpi, height=220)

    with col3:
        tableau_card('R2 Score',r2_score_kpi, height=220)

    st.divider()

    section_header('Actual Order Value vs Predicted Order Value')

    tableau_card('Regression Model', regression_model_prediction, height=700)

    st.divider()

    section_header('Insight')

    st.divider()

    insight_box(
        "Regression Model Insight",
        "The regression model shows limited predictive power, but it still gives useful insight into customer behaviour. "
        "The model predicts smaller order values better, while larger high-value orders are harder to predict accurately. "
        "This suggests that more detailed features, such as product categories or seasonal trends, could improve future predictions."
    )



if __name__ == '__main__':
    if selected=="Home":
        home_page()
    elif selected=="Customer Order Search":
        search_customer_order()
    elif selected == 'Sales Report':
        sales_report()
    elif selected == 'Customer Segmentation':
        customer_segmentation()
    elif selected == 'Regression Model':
        regression_model()
    elif selected == 'About':
        about_page()









