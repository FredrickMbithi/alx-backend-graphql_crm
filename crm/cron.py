def log_crm_heartbeat():
from datetime import datetime
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} CRM is alive"
    # GraphQL hello query
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql/',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        query = gql("""
            query {
                hello
            }
        """)
        result = client.execute(query)
        hello_response = result.get('hello', 'No response')
        message += f" | GraphQL hello: {hello_response}"
    except Exception as e:
        message += f" | GraphQL error: {e}"
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(message + "\n")

from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport

def update_low_stock():
    from datetime import datetime
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    message = f"{timestamp} Low stock update: "
    try:
        transport = RequestsHTTPTransport(
            url='http://localhost:8000/graphql/',
            verify=True,
            retries=3,
        )
        client = Client(transport=transport, fetch_schema_from_transport=True)
        mutation = gql("""
            mutation {
                updateLowStockProducts {
                    updatedProducts { name stock }
                    message
                }
            }
        """)
        result = client.execute(mutation)
        updates = result['updateLowStockProducts']['updatedProducts']
        msg = result['updateLowStockProducts']['message']
        if updates:
            for prod in updates:
                message += f"{prod['name']} (Stock: {prod['stock']}), "
        else:
            message += "No products updated. "
        message += f"Msg: {msg}"
    except Exception as e:
        message += f"GraphQL error: {e}"
    with open('/tmp/low_stock_updates_log.txt', 'a') as f:
        f.write(message + "\n")

CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
    ('0 */12 * * *', 'crm.cron.update_low_stock'),
]