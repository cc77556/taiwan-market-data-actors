"""Minimal example: pull TWSE institutional buy/sell for a watchlist.

pip install apify-client
"""
import os
import sys

from apify_client import ApifyClient

TOKEN = os.environ.get("APIFY_TOKEN")
if not TOKEN:
    sys.exit("Set APIFY_TOKEN (get one free at https://console.apify.com/account/integrations)")

client = ApifyClient(TOKEN)

run = client.actor("chamarix/twse-institutional-trades").call(
    run_input={
        "startDate": "2026-08-11",           # ISO date; data available from 2012-05-02
        "stockCodes": ["2330", "2454"],      # omit to get the whole market (~1,300 rows/day)
    }
)

if run["status"] != "SUCCEEDED":
    sys.exit(f"Run finished with status {run['status']}")

for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(
        item["date"],
        item["stock_code"],
        item["stock_name"],
        "foreign:", item["foreign_net"],
        "trust:", item["trust_net"],
        "dealer:", item["dealer_net"],
        "total:", item["total_institutional_net"],
    )
