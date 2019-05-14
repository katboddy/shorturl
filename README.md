# shorturl

Functionality overview:
1. Insert URL into box.
2. Get a short URL back.
3. Insert shortened URL in your browser.
4. Redirect to original URL.

Components:
1. Frontend: basic website with an input field (maybe static s3 hosting?)
2. Engine: bijective function (lambda / cloud function) converting long string to a shorter one (hashing? should we have a way to convert it back if the db fails?)
3. API gateway for the website and lambda to talk together.
4. Database (key-value type store for our hashtable)
5. Terraform to put the infra together and deploy for the first time.
6. Webhook for updates. Cloud trigger.
7. Stackdriver / Cloudwatch
8. Load test. Latency test.

9. Most security should be covered by AWS/GCP but what's needed:
- IAM roles for function, gateway, bucket
- Cloudflare for SSL
- Some kind of alerting, maybe liveness probe with an alert to Slack?

