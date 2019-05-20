# shorturl

Functionality overview:
1. Insert URL into box.
2. Get a short URL back.
3. Insert shortened URL in your browser.
4. Redirect to original URL.

# Components:
1. Flask app with a connection to DB - translating url to short url and redirecting short url to the original url - fixing some bugs still.
2. Cloud SQL database on GCP
3. Dockerfile to build the Flask app.
4. GKE stack containing the Flask app, the Cloud SQL Proxy, LoadBalancer service and secrets.
6. GKE cluster - autoscaling 1-10 nodes.
7. Cloud Build to trigger the deployment.
8. Bucket to contain the KMS encryption key for the secrets.
9. Stackdriver monitoring.

# Steps to deploy:
1. Create a terraform service account on GCP and download the json (permissions for buckets, kms, cloud SQL, GKE cluster, Cloud Build)
2. Enable Cloud SQL, Cloud Build, KMS API
3. Terraform init, plan, apply
4. Encrypt the creds yaml file - first base64 the vars, then encrypt using the kms.
echo -n username | base64
gcloud kms encrypt --location=us --keyring=shorturl-key-ring --key=shorturl-crypto-key --ciphertext-file=shorturl-creds.yaml.enc --plaintext-file=shorturl-creds.yaml

# TODO:
1. Fix the Flask app

# What should be done before going to prod:
1. Cloud Build is deployed manually, should be added to terraform, the SA for Cloud Build needs permission for "container.clusters.get".
2. kubectl create secret generic cloudsql-instance-credentials --from-file=sqlcredentials.json - done manually, should create a secret in yaml
3. Create static IP address, DNS record and SSL cert
4. Secure further using Cloudflare
5. Add liveness probe on https
6. Make stackdriver alert to email / slack.
7. Load and latency test.

# Security considerations:
1. Most of the infra is in GCP so the actual VMs are secured by GCP, but adding Cloudflare and SSL is important.
2. GKE sits in a default VPC, should create a custom VPC.
3. Firewall rules only allowing https traffic
4. Cloud SQL has no outside access
5. IAM permissions based on the smallest possible permission set.

# Scaling and latency considerations:
1. GKE cluster will scale up to 10 instances. Maybe add "max pods per node"? This should be tested.
2. Cloud SQL might not be fast enough for mln users. Consider using Redis or Datastore.

