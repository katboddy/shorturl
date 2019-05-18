resource "google_storage_bucket" "key-bucket" {
  name = "shorturl-key-bucket"
}

resource "google_kms_key_ring" "key-ring" {
  name     = "${var.key_ring}"
  location = "${var.key_location}"
}

resource "google_kms_crypto_key" "crypto-key" {
  name            = "${var.key_name}"
  key_ring        = "${google_kms_key_ring.key-ring.self_link}"
  rotation_period = "2592000s"
  lifecycle {
    prevent_destroy = true
  }
}
