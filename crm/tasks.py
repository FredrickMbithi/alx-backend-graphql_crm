import requests
from celery import shared_task
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
from datetime import datetime

@shared_task
def generate_crm_report():
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    message = f"{timestamp} - Report: "
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql/',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""
            query {
                totalCustomers
                totalOrders
                totalRevenue
            }
        """)
        result = client.execute(query)
        customers = result.get('totalCustomers', 0)
        orders = result.get('totalOrders', 0)
        revenue = result.get('totalRevenue', 0)
        message += f"{customers} customers, {orders} orders, {revenue} revenue"
    except Exception as e:
        message += f"GraphQL error: {e}"
    with open('/tmp/crm_report_log.txt', 'a') as f:
        f.write(message + "\n")
