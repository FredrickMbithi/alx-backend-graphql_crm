#!/bin/bash
# Navigate to the project directory
cd /home/ghost/alx-backend-graphql_crm || exit 1

# Get current timestamp
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

# Prefer project venv python
if [ -x "./venv/bin/python" ]; then
    PYTHON="./venv/bin/python"
elif [ -x "./.venv/bin/python" ]; then
    PYTHON="./.venv/bin/python"
else
    PYTHON="$(command -v python3 || command -v python || true)"
fi

# Fall back error if no python
if [ -z "$PYTHON" ]; then
    echo "[$TIMESTAMP] ERROR: no python interpreter found" >> /tmp/customer_cleanup_log.txt
    exit 1
fi

# Execute Django shell command to delete inactive customers

DELETED_COUNT=$("$PYTHON" manage.py shell <<'PY'
from django.utils import timezone
from datetime import timedelta
from crm.models import Customer

one_year_ago = timezone.now() - timedelta(days=365)

# Customers with no orders OR only orders older than one year
inactive_customers = (Customer.objects.filter(orders__isnull=True) |
                      Customer.objects.filter(orders__created_at__lt=one_year_ago)).distinct()

count = inactive_customers.count()
inactive_customers.delete()
print(count)
PY
)

# Ensure a numeric default
DELETED_COUNT="${DELETED_COUNT:-0}"

# Log the result with timestamp
echo "[$TIMESTAMP] Deleted $DELETED_COUNT inactive customers" >> /tmp/customer_cleanup_log.txt