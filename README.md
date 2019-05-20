# shorturl

Functionality overview:
1. Insert URL into box.
2. Get a short URL back.
3. Insert shortened URL in your browser.
4. Redirect to original URL.

# Components:
1. Flask url shortening app, from here:
https://impythonist.wordpress.com/2015/10/31/building-your-own-url-shortening-service-with-python-and-flask/
2. Cloud SQL database on GCP.
3. Dockerfile to build the Flask app.
4. Kubernetes stack containing the deployment (Flask app + Cloud SQL Proxy), service (LoadBalancer) and encrypted secrets for DB user and password.
5. Terraform defined infrastructure - GKE cluster (autoscaling 1-10 nodes), Cloud Build to trigger the deployment, KMS key setup, Bucket to contain the KMS encryption key.

# Steps to deploy:
1. Create a terraform service account on GCP and download the json (permissions for buckets, kms, cloud SQL, GKE cluster, Cloud Build)
2. Enable Cloud SQL, Cloud Build, KMS API
3. Terraform init, plan, apply
4. Encrypt the creds yaml file - first base64 the vars, then encrypt using the kms.
echo -n username | base64
gcloud kms encrypt --location=us --keyring=shorturl-key-ring --key=shorturl-crypto-key --ciphertext-file=shorturl-creds.yaml.enc --plaintext-file=shorturl-creds.yaml
5. Git push - will deploy the app to the cluster.

# TODO:
1. Create static IP address, DNS record, SSL and add Cloudflare
2. Update ENV variables to include host:port

# What should be done before going to prod:
1. Cloud Build trigger is deployed manually, should be added to terraform, the SA for Cloud Build needs permission for "container.clusters.get".
2. kubectl create secret generic cloudsql-instance-credentials --from-file=sqlcredentials.json - done manually, should create a secret in yaml
3. Add liveness probe on https
4. Make stackdriver alert to email / slack.
5. Unit tests
6. Load and latency tests.
7. The trigger should run on tag instead of branch, this way there can be a separation between pushes to prod or dev and tag won't have to be hardcoded in cloudbuild.yaml.

# Security considerations:
1. Most of the infra is in GCP so the actual VMs are secured by GCP, but adding Cloudflare and SSL is important.
2. GKE sits in a default VPC, should create a custom VPC.
3. Firewall rules only allow http/https traffic.
4. Cloud SQL has no outside access.
5. IAM permissions are based on the smallest possible permission set.
6. Stackdriver logs are adding the observability.
7. Secrets are encrypted, no sensitive data in the repo.

# Scaling and latency considerations:
1. GKE cluster will scale up to 10 instances. Maybe add "max pods per node"? This should be tested.
2. Cloud SQL might not be fast enough for mlns of users. Extend the app to be able to use an abstract storage, test with different stores, like:
- Redis
- DynamoDB
- Datastore
- Cassandra
- Druid


