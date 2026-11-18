# Radio Price Watch

Live app: https://hardt0303.github.io/radio-price-watch/

This repository publishes the price dashboard and runs the scheduled price checks. It does not need to be installed on a Raspberry Pi or Pi-Star.

## Use the app

1. Open the live app link above on your phone or computer.
2. The Store prices section shows the latest verified Icom ID-5200A prices and each store's Buy link.
3. The app refreshes its displayed price file every minute. GitHub performs the actual store checks once an hour by default.
4. In **Your watch list**, add an item name and a **Buy at or below** price. A product link and current price are optional.
5. For custom items, enter or update the current price manually. The custom watch list is saved in the browser and device where it was entered; it does not sync between phone and computer, and custom items do not yet have automatic checks or alerts.

### Add the app to a phone or computer

**iPhone**

1. Open the live app in Safari.
2. Tap **Share**.
3. Tap **Add to Home Screen**.
4. Choose a name such as **Price Watch**, then tap **Add**.

**Windows computer**

1. Open the live app in Chrome or Edge.
2. Press **Ctrl+D** and save it as a bookmark.
3. Open the bookmark whenever you want the dashboard. You do not need to keep the Pi or computer running for GitHub's scheduled checks.

The store prices are the same on every device because they come from the published prices.json file. Custom watch-list entries are currently saved separately by each browser.

## How often GitHub checks stores

The schedule is in the file .github/workflows/pages.yml. The current setting is:

    schedule:
      - cron: "17 * * * *"

That means one check every hour, at 17 minutes past the hour. The schedule is UTC because this workflow does not set a timezone. A GitHub Actions run visits the six store product pages, updates prices.json, and publishes the dashboard.

The app's **Refresh prices** button only reloads the latest published data; it does not start a new store check. GitHub may start scheduled runs late during busy periods, so a cron time is not an exact guarantee. GitHub's shortest supported scheduled interval is once every five minutes.

### Change the schedule in GitHub

1. Open the repository: https://github.com/hardt0303/radio-price-watch
2. Open **.github/workflows/pages.yml**.
3. Select the pencil **Edit** button.
4. Under **schedule**, change the cron value.
5. Select **Commit changes**. The new setting takes effect after GitHub reads the updated workflow.

Examples:

| Cron value | How often |
| --- | --- |
| 17 * * * * | Every hour, at minute 17 (current setting) |
| 17 */2 * * * | Every 2 hours |
| 17,47 * * * * | Every 30 minutes |
| */15 * * * * | Every 15 minutes |
| */5 * * * * | Every 5 minutes, GitHub's shortest interval |
| 17 4 * * * | Once a day at 04:17 UTC |

A more frequent schedule checks retailer pages more often. The stores may limit automated requests, and GitHub may delay scheduled runs during busy periods. The current hourly schedule is a reasonable default.

### Run a check now

1. Open the repository's Actions page: https://github.com/hardt0303/radio-price-watch/actions
2. Select **Check prices and publish dashboard**.
3. Select **Run workflow**, then **Run workflow** again.

This starts one immediate check. It does not change the recurring schedule. The site's **Refresh prices** button does not run this workflow.

## What is automated today

- GitHub Actions checks the Icom ID-5200A at six retailer pages hourly and publishes verified readings.
- Price decreases are recorded in the dashboard's **Recent drops** section.
- If one store cannot be verified, the dashboard shows that status rather than treating an unverified reading as a new price.
- Custom products, custom buy-at targets, phone/desktop list syncing, and SMS/email notifications are not yet automated. Those need a shared account-backed store and a price-check/notification service; the current GitHub Pages app stores custom entries only in each browser.

## Repository files

- index.html — responsive dashboard and local custom watch list.
- update_prices.py — reads retailer product pages and updates the price history.
- prices.json — latest readings and recent price drops.
- .github/workflows/pages.yml — hourly schedule, manual run, and GitHub Pages deployment.
