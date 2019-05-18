provider "google" {
  credentials = "${file("creds/serviceaccount.json")}"
  project     = "${var.gcp_project}"
  region      = "${var.gcp_region}"
  zone        = "${var.gcp_zone}"
}

provider "github" {
  token        = "${var.github_token}"
}
