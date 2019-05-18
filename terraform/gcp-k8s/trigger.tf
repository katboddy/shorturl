//todo: make github repo trigget docker image using webhook and cloudbuild.yaml
//it is manually created right now

//
//resource "google_cloudbuild_trigger" "build_trigger_sourcerepo" {
//  description = "shorturl-build-trigger"
//  trigger_template {
//    tag_name = ".*"
//    repo_name = "shorturl"
//  }
//  filename = "cloudbuild.yaml"
//  substitutions {
//    _CLOUDSDK_COMPUTE_ZONE      = "${var.gcp_zone}"
//    _CLOUDSDK_CONTAINER_CLUSTER = "${var.cluster_name}"
//    _CLOUDSDK_PROJECT           = "${var.gcp_project}"
//    _CLOUDSDK_KEY_LOCATION      = "${var.key_location}"
//    _CLOUDSDK_KEY_RING          = "${var.key_ring}"
//    _CLOUDSDK_KEY_NAME          = "${var.key_name}"
//  }
//}
//
