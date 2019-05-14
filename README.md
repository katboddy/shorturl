# shorturl

Functionality overview:
1. Insert URL into box.
2. Get a short URL back.
3. Insert shortened URL in your browser.
4. Redirect to original URL.

Components:
1a. Frontend: basic website with an input field (maybe static s3 hosting?), fronted by CloudFlare with SSL
2a. Engine: bijective function (lambda / cloud function) converting long string to a shorter one (hashing? should we have a way to convert it back if the db fails?)
1&2b. Django app including a frontend + engine contenerized. Hosted on GKE or similar. 
3. Database (key-value type store for our hashtable)
4. Terraform to put the infra together and deploy for the first time.
5. Webhook for updates. Cloud trigger.
6. Stackdriver / Cloudwatch
7. Load test. Latency test.

