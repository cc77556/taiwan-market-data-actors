// Minimal example: pull TWSE institutional buy/sell for a watchlist.
// npm install apify-client
import { ApifyClient } from 'apify-client';

const token = process.env.APIFY_TOKEN;
if (!token) {
  console.error('Set APIFY_TOKEN (get one free at https://console.apify.com/account/integrations)');
  process.exit(1);
}

const client = new ApifyClient({ token });

const run = await client.actor('chamarix/twse-institutional-trades').call({
  startDate: '2026-08-11',        // ISO date; data available from 2012-05-02
  stockCodes: ['2330', '2454'],   // omit to get the whole market (~1,300 rows/day)
});

if (run.status !== 'SUCCEEDED') {
  console.error(`Run finished with status ${run.status}`);
  process.exit(1);
}

const { items } = await client.dataset(run.defaultDatasetId).listItems();
for (const item of items) {
  console.log(
    item.date, item.stock_code, item.stock_name,
    'foreign:', item.foreign_net,
    'trust:', item.trust_net,
    'dealer:', item.dealer_net,
    'total:', item.total_institutional_net,
  );
}
