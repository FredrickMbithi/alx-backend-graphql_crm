# CRM Celery & Report Setup

## Install Redis and dependencies
- Install Redis: `sudo apt-get install redis-server`
- Start Redis: `sudo service redis-server start`
- Install Python dependencies: `pip install -r requirements.txt`

## Run migrations
- `python manage.py migrate`

## Start Celery worker
- `celery -A crm worker -l info`

## Start Celery Beat
- `celery -A crm beat -l info`

## Verify logs
- Check `/tmp/crm_report_log.txt` for weekly report entries.

## What the report includes
- Total number of customers
- Total number of orders
- Total revenue (sum of all orders)

## Troubleshooting
- Ensure Redis is running on `localhost:6379`
- Check Celery worker and beat logs for errors
