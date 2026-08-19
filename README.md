# Taiwan Market Data APIs

Clean JSON APIs for Taiwan stock market and government data — institutional flows, financial statements, dividends, margin/short balances, insider filings, procurement tenders and more. 22 Actors on the [Apify platform](https://apify.com/chamarix), all built the same way:

- **Official sources only** — TWSE, TPEx, TAIFEX, TDCC, MOPS, and government open-data endpoints. No third-party aggregators.
- **Cross-validated on every run** — where an independent official endpoint exists for the same data, each run fetches it and compares field-by-field. Accounting identities (e.g. `net = buy − sell`, balance-sheet equations) are asserted per row.
- **Normalized schemas** — ROC calendar dates → ISO 8601, consistent field names across listed (TWSE), OTC (TPEx) and emerging boards, full official Chinese line items preserved alongside.
- **Pay per result** — most Actors cost $0.50 per 1,000 records. Tracking a 10-stock watchlist daily costs well under $1/month.

## The suite

### Chip / flow data (籌碼面)

| Actor | Data | History |
|---|---|---|
| [twse-institutional-trades](https://apify.com/chamarix/twse-institutional-trades) | Daily foreign / investment-trust / dealer buy-sell per stock, TWSE listed (三大法人買賣超) | multi-year |
| [tpex-institutional-trades](https://apify.com/chamarix/tpex-institutional-trades) | Same for TPEx OTC — where Taiwan's small-cap semi names live | multi-year |
| [taifex-institutional-derivatives](https://apify.com/chamarix/taifex-institutional-derivatives) | Institutional futures & options positions (TAIFEX), incl. TXO put/call ratio | rolling 3y |
| [taiwan-margin-trading](https://apify.com/chamarix/taiwan-margin-trading) | Daily margin trading & short sale balances per stock (融資融券) | 2024+ |
| [taiwan-sbl-short-sale-balance](https://apify.com/chamarix/taiwan-sbl-short-sale-balance) | Securities-lending short sale balances (借券賣出餘額) | multi-year |
| [taiwan-day-trading-stats](https://apify.com/chamarix/taiwan-day-trading-stats) | Day-trading volume, value & ratio per stock (現股當沖) | 2014+ |
| [tdcc-shareholding-dispersion](https://apify.com/chamarix/tdcc-shareholding-dispersion) | Weekly TDCC shareholding dispersion — retail vs whale structure (股權分散表) | weekly |
| [taiwan-foreign-shareholding](https://apify.com/chamarix/taiwan-foreign-shareholding) | Foreign ownership % and remaining quota per stock (外資持股) | snapshot |
| [taiwan-etf-regular-investment](https://apify.com/chamarix/taiwan-etf-regular-investment) | Monthly regular savings plan rankings — top stocks & ETFs by investor accounts, retail flow not price (定期定額) | 2020-10+ |

### Fundamentals (基本面)

| Actor | Data | History |
|---|---|---|
| [taiwan-monthly-revenue](https://apify.com/chamarix/taiwan-monthly-revenue) | Monthly revenue of 1,900+ listed & OTC companies, MoM/YoY (月營收) | monthly |
| [taiwan-financial-statements](https://apify.com/chamarix/taiwan-financial-statements) | Quarterly income statement, balance sheet & cash flow, identities checked per row (財報三表) | 2013Q1+ |
| [taiwan-dividend-calendar](https://apify.com/chamarix/taiwan-dividend-calendar) | Ex-dividend / ex-rights dates, reference prices, payouts (除權息) | 2003+ |

### Events & governance (事件面)

| Actor | Data | History |
|---|---|---|
| [taiwan-stock-alerts](https://apify.com/chamarix/taiwan-stock-alerts) | Watch-list, disposition & short-sale suspension alerts (注意股/處置股) | multi-year |
| [taiwan-insider-share-transfers](https://apify.com/chamarix/taiwan-insider-share-transfers) | Insider share-transfer filings — directors, officers, 10% holders (內部人轉讓申報) | 2002+ |
| [taiwan-director-shareholdings](https://apify.com/chamarix/taiwan-director-shareholdings) | Monthly director / officer / 10%-holder shareholdings and share-pledge ratio (董監持股質押) | 1999+ |
| [taiwan-block-trades](https://apify.com/chamarix/taiwan-block-trades) | Every block trade with price, size, paired/continuous and basket constituents (鉅額交易) | 2005+ |
| [taiwan-shareholder-meetings](https://apify.com/chamarix/taiwan-shareholder-meetings) | Shareholder meeting dates & venues, book-closure periods, board elections, e-voting windows (股東會) | 2005+ |
| [taiwan-emerging-stock-quotes](https://apify.com/chamarix/taiwan-emerging-stock-quotes) | Emerging Stock Board quotes, bid/ask & turnover, company register and listing-application status — the pre-IPO tier (興櫃) | 2003+ |
| [taiwan-treasury-stock-buybacks](https://apify.com/chamarix/taiwan-treasury-stock-buybacks) | Every buyback ever filed — purpose, price band and window announced, versus shares actually bought and average price paid (庫藏股) | 2000+ |
| [taiwan-warrants-daily](https://apify.com/chamarix/taiwan-warrants-daily) | Every listed & OTC warrant priced daily — OHLC, underlying close, strike, exercise ratio, expiry, plus moneyness, premium and leverage (權證) | 2004+ |

### Government & civic data

| Actor | Data |
|---|---|
| [taiwan-tender-monitor](https://apify.com/chamarix/taiwan-tender-monitor) | Government e-procurement tenders — open calls, awards, failures (政府採購) |
| [taiwan-legislator-monitor](https://apify.com/chamarix/taiwan-legislator-monitor) | Legislative Yuan bills, legislators & meetings (立法院) |

## Quickstart

Every Actor runs the same way. You need a free [Apify account](https://apify.com) and its API token.

### curl

```bash
# Run the TWSE institutional trades Actor synchronously and get JSON back
curl -s -X POST \
  "https://api.apify.com/v2/acts/chamarix~twse-institutional-trades/run-sync-get-dataset-items?token=$APIFY_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"startDate": "2026-08-11", "stockCodes": ["2330", "2454"]}'
```

### Python

See [`examples/quickstart.py`](examples/quickstart.py) for a version with error handling.

```python
from apify_client import ApifyClient

client = ApifyClient("YOUR_APIFY_TOKEN")

run = client.actor("chamarix/twse-institutional-trades").call(
    run_input={"startDate": "2026-08-11", "stockCodes": ["2330", "2454"]}
)
for item in client.dataset(run["defaultDatasetId"]).iterate_items():
    print(item["stock_code"], item["foreign_net"])
```

### Node.js

See [`examples/quickstart.mjs`](examples/quickstart.mjs).

```js
import { ApifyClient } from 'apify-client';

const client = new ApifyClient({ token: 'YOUR_APIFY_TOKEN' });

const run = await client.actor('chamarix/twse-institutional-trades').call({
  startDate: '2026-08-11',
  stockCodes: ['2330', '2454'],
});
const { items } = await client.dataset(run.defaultDatasetId).listItems();
console.log(items);
```

### Scheduling

Any Actor can run on a cron schedule inside Apify (Console → Schedules) and push results to a webhook, Google Sheets, or your own endpoint — no server needed.

## Notes on the data

- **Dates**: all inputs/outputs use ISO 8601 (`2026-08-11`). ROC calendar dates (民國) from the official sources are converted for you.
- **Units**: monetary fields note their unit in the schema (TWD, thousand TWD, shares, lots). Taiwan sources mix these freely; the Actors do not.
- **Coverage**: unless noted, each Actor covers TWSE listed + TPEx OTC; several also include the emerging board.
- **Backfills**: history depth varies by what the official source actually serves — each Actor's README documents the exact floor and what happens when you query past it (explicit error, never silent truncation).

## Who is this for

Quant research on TW equities, dashboards, portfolio monitoring, market-structure studies, B2G sales intelligence, investigative journalism, civic tech.

## Questions / requests

Open an [issue](https://github.com/cc77556/taiwan-market-data-actors/issues) — including requests for Taiwan data sources not covered yet.
