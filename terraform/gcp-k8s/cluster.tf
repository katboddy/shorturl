resource "google_container_cluster" "cluster" {
  name               = "url-shortener-cluster"
  description        = "url shortener cluster"
  remove_default_node_pool = true
  initial_node_count = 1
}

resource "google_container_node_pool" "primary_nodes" {
  name       = "main-node-pool"
  cluster    = "${google_container_cluster.cluster.name}"
  initial_node_count = 1
  autoscaling {
    max_node_count = 10
    min_node_count = 1
  }
  node_config {
    preemptible  = true
    machine_type = "n1-standard-1"
    disk_size_gb = 10
    oauth_scopes = [
      "https://www.googleapis.com/auth/compute",
      "https://www.googleapis.com/auth/devstorage.read_only",
      "https://www.googleapis.com/auth/logging.write",
      "https://www.googleapis.com/auth/monitoring"
    ]
  }
}

