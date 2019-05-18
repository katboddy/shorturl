variable "dbpassword" {}
variable "dbuser" {}
variable "github_token" {}

variable "gcp_region" {
  default = "us-west1"
}

variable "gcp_zone" {
  default = "us-west1-a"
}

variable "gcp_project" {
  default = "url-shortener-240801"
}

variable "key_location" {
  default = "us"
}

variable "key_name" {
  default = "shorturl-crypto-key"
}

variable "key_ring" {
  default = "shorturl-key-ring"
}

variable "cluster_name" {
  default = "url-shortener-cluster"
}
