import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from datetime import datetime as dt

sales_dashboard_embed_code = '''<div class='tableauPlaceholder' id='viz1782000930954' style='position: relative'><noscript><a href='#'><img alt='Sales Performance Dahsboard ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;SalesPerformanceDahsboard&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;SalesPerformanceDahsboard' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;SalesPerformanceDahsboard&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782000930954');                    var vizElement = divElement.getElementsByTagName('object')[0];                    if ( divElement.offsetWidth > 800 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else if ( divElement.offsetWidth > 500 ) { vizElement.style.width='1000px';vizElement.style.height='827px';} else { vizElement.style.width='100%';vizElement.style.height='1727px';}                     var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

gross_revenue_kpi = '''<div class='tableauPlaceholder' id='viz1781822430643' style='position: relative'><noscript><a href='#'><img alt='Gross Revenue KPI ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;GrossRevenueKPI&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;GrossRevenueKPI' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;GrossRevenueKPI&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1781822430643');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

net_revenue_kpi = '''<div class='tableauPlaceholder' id='viz1781822462904' style='position: relative'><noscript><a href='#'><img alt='Net Revenue KPI  ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;NetRevenueKPI&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;NetRevenueKPI' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;NetRevenueKPI&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1781822462904');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

revenue_lost_kpi = '''<div class='tableauPlaceholder' id='viz1781822485923' style='position: relative'><noscript><a href='#'><img alt='Revenue Lost KPI ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;RevenueLostKPI&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;RevenueLostKPI' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;RevenueLostKPI&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1781822485923');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

revenue_growth_kpi = '''<div class='tableauPlaceholder' id='viz1782001030848' style='position: relative'><noscript><a href='#'><img alt='Revenue Growth KPI ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;RevenueGrowthKPI&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;RevenueGrowthKPI' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;RevenueGrowthKPI&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782001030848');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

average_invoices_kpi = '''<div class='tableauPlaceholder' id='viz1782001711676' style='position: relative'><noscript><a href='#'><img alt='Average Completed Invoices ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;AverageCompletedInvoices&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;AverageCompletedInvoices' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;AverageCompletedInvoices&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782001711676');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

total_invoices_kpi = '''<div class='tableauPlaceholder' id='viz1782001655034' style='position: relative'><noscript><a href='#'><img alt='Total Invoices ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;TotalInvoices&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;TotalInvoices' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;TotalInvoices&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782001655034');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

monthly_completed_cancelled_revenue = """<div class='tableauPlaceholder' id='monthlyRevenueCancellationViz' style='position: relative; width: 100%;'>   <noscript>       <a href='#'>           <img                 alt='Monthly Revenue vs Cancellation Loss'                src='https://public.tableau.com/static/images/Ca/Capstone_Project_Code-Institue_backup/RevenuevsCancellationLoss/1_rss.png'                style='border: none; width: 100%;'            />     </a>    </noscript>    <object class='tableauViz' style='display:none; width:100%; height:650px;'>       <param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' />        <param name='embed_code_version' value='3' />        <param name='site_root' value='' />        <param name='name' value='Capstone_Project_Code-Institue_backup/RevenuevsCancellationLoss' />        <param name='tabs' value='no' />        <param name='toolbar' value='no' />        <param name='static_image' value='https://public.tableau.com/static/images/Ca/Capstone_Project_Code-Institue_backup/RevenuevsCancellationLoss/1.png' />        <param name='animate_transition' value='yes' />        <param name='display_static_image' value='yes' />        <param name='display_spinner' value='yes' />       <param name='display_overlay' value='yes' />        <param name='display_count' value='no' />        <param name='language' value='en-GB' />        <param name='filter' value='publish=yes' />    </object></div><script type='text/javascript'>   var divElement = document.getElementById('monthlyRevenueCancellationViz');    var vizElement = divElement.getElementsByTagName('object')[0];    vizElement.style.width = '100%';    vizElement.style.height = '650px';    var scriptElement = document.createElement('script');scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';vizElement.parentNode.insertBefore(scriptElement, vizElement);</script>"""

top10_countries_by_completed_revenue = '''<div class='tableauPlaceholder' id='viz1782003023595' style='position: relative'><noscript><a href='#'><img alt='Top Countries by Completed Revenue ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;TopCountriesbycompletedRevenueBarChart&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;TopCountriesbycompletedRevenueBarChart' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;TopCountriesbycompletedRevenueBarChart&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782003023595');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

top10_products_by_completed_revenue = '''<div class='tableauPlaceholder' id='viz1782003113916' style='position: relative'><noscript><a href='#'><img alt='Which products produce the most revenue? ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;TopProductsbyRevenueBarChart&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;TopProductsbyRevenueBarChart' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;TopProductsbyRevenueBarChart&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782003113916');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

total_customers_kpi = '''<div class='tableauPlaceholder' id='viz1782006348136' style='position: relative'><noscript><a href='#'><img alt='Total Customers KPI ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;TotalCustomersKPI&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;TotalCustomersKPI' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;TotalCustomersKPI&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782006348136');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

vip_customers_kpi = '''<div class='tableauPlaceholder' id='viz1782006361412' style='position: relative'><noscript><a href='#'><img alt='VIP customers ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;VIPcustomers&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;VIPcustomers' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;VIPcustomers&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782006361412');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

loyal_customers_kpi = '''<div class='tableauPlaceholder' id='viz1782006389496' style='position: relative'><noscript><a href='#'><img alt='Loyal Customers ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;LoyalCustomers&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;LoyalCustomers' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;LoyalCustomers&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782006389496');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

at_risk_customers_kpi = '''<div class='tableauPlaceholder' id='viz1782006400525' style='position: relative'><noscript><a href='#'><img alt='At Risk Customers ' src='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;AtRiskCustomers&#47;1_rss.png' style='border: none' /></a></noscript><object class='tableauViz'  style='display:none;'><param name='host_url' value='https%3A%2F%2Fpublic.tableau.com%2F' /> <param name='embed_code_version' value='3' /> <param name='site_root' value='' /><param name='name' value='Capstone_Project_Code-Institue_backup&#47;AtRiskCustomers' /><param name='tabs' value='no' /><param name='toolbar' value='yes' /><param name='static_image' value='https:&#47;&#47;public.tableau.com&#47;static&#47;images&#47;Ca&#47;Capstone_Project_Code-Institue_backup&#47;AtRiskCustomers&#47;1.png' /> <param name='animate_transition' value='yes' /><param name='display_static_image' value='yes' /><param name='display_spinner' value='yes' /><param name='display_overlay' value='yes' /><param name='display_count' value='yes' /><param name='language' value='en-GB' /><param name='filter' value='publish=yes' /></object></div>                <script type='text/javascript'>                    var divElement = document.getElementById('viz1782006400525');                    var vizElement = divElement.getElementsByTagName('object')[0];                    vizElement.style.width='100%';vizElement.style.height=(divElement.offsetWidth*0.75)+'px';                    var scriptElement = document.createElement('script');                    scriptElement.src = 'https://public.tableau.com/javascripts/api/viz_v1.js';                    vizElement.parentNode.insertBefore(scriptElement, vizElement);                </script>'''

st.sidebar.header('Customer Segmentation Analysis')
st.set_page_config(
    page_title="Capstone Dashboard",
    layout="wide"
)
st.markdown("""
<style>
.block-container {
    max-width: 100% !important;
    width: 100% !important;
    padding-left: 1rem !important;
    padding-right: 1rem !important;
}
</style>
""", unsafe_allow_html=True)

def centered_title(text):
    st.markdown(
        f"<h1 style='text-align: center;'>{text}</h1>",
        unsafe_allow_html=True
    )


def centered_subheader(text):
    st.markdown(
        f"<h2 style='text-align: center;'>{text}</h2>",
        unsafe_allow_html=True
    )


def centered_text(text):
    st.markdown(
        f"<p style='text-align: center;'>{text}</p>",
        unsafe_allow_html=True
    )

with st.sidebar:
    selected = option_menu(
        menu_title = "Menu",
        options = ["Home","Customer Order Search", "Sales Report","Customer Segmentation","About"]
    )

def load_order_data():
    purchased_orders = pd.read_csv('completed_purchase_orders.csv')

    cancelled_orders = pd.read_csv('cancelled_orders.csv')

    return purchased_orders, cancelled_orders

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
    st.header('Home Page')
    st.write("This app analyses customer sales data to understand business revenue, cancellation losses, top-performing countries/products, customer value groups, and order value prediction using machine learning.")

    st.subheader('Main Questions Answered')

    st.write('How much revenue did the business make?')

    st.write('Are sales increasing or decreasing?')

    st.write('How much revenue was lost through cancellations?')

    st.write('Which countries produce the most revenue?')

    st.write('Which customer groups are most valuable?')

    st.write('How well did the regression model predict order value?')


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

def search_customer_order():
    centered_title('Invoice Lookup')

    purchased_orders, cancelled_orders = load_order_data()

    left, middle, right = st.columns([1, 2, 1])

    with middle:
        order_type = st.selectbox("Select Order Type", ["Purchased Orders", "Cancelled Orders"])

    if order_type == "Purchased Orders":
        data = purchased_orders
    else:
        data = cancelled_orders

    data['InvoiceNo'] = data['InvoiceNo'].astype(str).str.strip().str.upper()

    with middle:
        invoice_no = st.text_input('What is your Invoice Number?').strip().upper()

    with middle:
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

                    with middle:
                        inspect_button = st.button("Inspect")

                        if inspect_button:
                            show_order_popup(selected_data, order_type)
                        else:
                            st.info("Click one row in the table, then press Inspect.")

            else:
                st.error("No Invoice number Recognized or Invoice Number Doesn't exist.")

def sales_report():
    centered_title("Sales Report")

    centered_subheader("KPI ROW 1")

    col1, col2, col3 = st.columns(3)

    left, middle, right = st.columns([1, 10, 1])

    with left:
        with col1:
            components.html(gross_revenue_kpi, height=220,scrolling=False)

    with middle:
        with col2:
            components.html(net_revenue_kpi, height=220, scrolling=False)

    with right:
        with col3:
            components.html(revenue_lost_kpi, height=220, scrolling=False)

    st.divider()

    centered_subheader("KPI ROW 2")

    col4, col5, col6 = st.columns(3)

    with left:
        with col4:
            components.html(revenue_growth_kpi, height=220, scrolling=False)

    with middle:
        with col5:
            components.html(average_invoices_kpi, height=220, scrolling=False)

    with right:
        with col6:
            components.html(total_invoices_kpi, height=220, scrolling=False)

    st.divider()

    centered_subheader("MAIN CHART")

    components.html(monthly_completed_cancelled_revenue, height=700, scrolling=False)

    st.divider()

    centered_subheader("BOTTOM ROW CHART")

    col7, col8 = st.columns(2)

    with left:
        with col7:
            components.html(top10_countries_by_completed_revenue, height=500, scrolling=False)

    with right:
        with col8:
            components.html(top10_products_by_completed_revenue, height=500, scrolling=False)

def customer_segmentation():
    centered_title("Customer Segmentation")

    st.divider()

    centered_subheader("Small explanation")
    st.write('Customers were grouped using frequency, recency, average order value, and monetary value.')

    st.divider()

    centered_subheader("KPI/Overview:")

    col1, col2, col3, col4 = st.columns(4)

    left, middle, right = st.columns([1, 10, 1])

    with left:
        with col1:
            components.html(total_customers_kpi, height=220, scrolling=False)

    with middle:
        with col2:
            components.html(vip_customers_kpi, height=220, scrolling=False)

    with middle:
        with col3:
            components.html(loyal_customers_kpi, height=220, scrolling=False)

    with right:
        with col4:
            components.html(at_risk_customers_kpi, height=220, scrolling=False)

    st.divider()



if __name__ == '__main__':
    if selected=="Home":
        home_page()
    elif selected=="Customer Order Search":
        search_customer_order()
    elif selected == 'Sales Report':
        sales_report()










