PgSQLExtensionCheck
Overview
PgSQLExtensionCheck is a Python-based GUI utility designed to compare PostgreSQL extensions installed on an on-premises PostgreSQL server with those supported on Azure PostgreSQL Flexible Server. The tool helps database administrators and migration teams quickly identify compatibility gaps and streamline migration planning.
Features

Connects to both source (on-premises) and destination (Azure) PostgreSQL servers.
Fetches and compares installed extensions vs. Azure-supported extensions.
Highlights extensions installed on source but not supported on Azure, and vice versa.
Exports comparison results to CSV for documentation and reporting.
User-friendly interface built with Tkinter.

Requirements

Python 3.7+
psycopg2 (PostgreSQL connector)
Tkinter (standard with Python)
Access credentials for both source and Azure PostgreSQL servers

Usage

Enter connection details for both source and Azure PostgreSQL servers.
Click Run Comparison to view extension compatibility.
Click Export to CSV to save results.

Version History
v1.0.0

License
This project is released under Free License.
