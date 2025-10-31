from datetime import datetime

def log_crm_heartbeat():
    timestamp = datetime.now().strftime('%d/%m/%Y-%H:%M:%S')
    with open('/tmp/crm_heartbeat_log.txt', 'a') as f:
        f.write(f"{timestamp} CRM is alive\n")
CRONJOBS = [
    ('*/5 * * * *', 'crm.cron.log_crm_heartbeat'),
]