import MySQLdb

print(f"MySQLdb.version_info: {MySQLdb.version_info}")
print(f"MySQLdb.release: {MySQLdb.release}")

# Try to see what Django checks
try:
    version = MySQLdb.version_info
    if version < (2, 2, 1):
        print(f"ERROR: Old version detected: {version}")
    else:
        print(f"SUCCESS: Version {version} is OK!")
except Exception as e:
    print(f"Error checking version: {e}")

import sys
import os

# Add the project to the path
sys.path.insert(0, os.path.dirname(__file__))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Ecommerce.settings')

# Initialize Django
import django
django.setup()

print("\n--- After Django setup ---")
from django.db import connection
print(f"Database backend: {connection.vendor}")
try:
    print(f"Database version: {connection.mysql_version}")
except Exception as e:
    print(f"Error getting database version: {e}")
