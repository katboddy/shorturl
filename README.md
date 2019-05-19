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

10. Instead of 1,2,3 maybe a little Django app on GKE? Would that end up cheaper / more scalable than Lambda? Test both.

# Steps taken so far:
Created a terraform service account on GCP and downloaded the json
(permissions: gke, buckets, kms, build, sql)
Enabled Cloud SQL, Cloud Build, KMS API
Terraform init, plan, apply
Encrypt creds - first base64 the vars, then encrypt using the kms
echo -n username | base64
gcloud kms encrypt --location=us --keyring=shorturl-key-ring --key=shorturl-crypto-key --ciphertext-file=shorturl-creds.yaml.enc --plaintext-file=shorturl-creds.yaml
Note: added container.clusters.get permission to the Cloud Build SA manually, update scripts.
Note: kubectl create secret generic cloudsql-instance-credentials --from-file=sqlcredentials.json done manually, add a yaml

