provider "google" {
  credentials = "${file("creds/serviceaccount.json")}"
  project     = "url-shortener-240801"
  region      = "us-west1"
  zone        = "us-west1-a"
}

provider "github" {
  token        = "${var.github_token}"
}

