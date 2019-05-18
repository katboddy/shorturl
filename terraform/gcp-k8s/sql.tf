resource "google_sql_database_instance" "instance" {
  name = "shorturl-instance"
  database_version = "POSTGRES_9_6"

  settings {
    tier = "db-f1-micro"
  }
}

resource "google_sql_database" "database" {
  name      = "shorturl"
  instance  = "${google_sql_database_instance.instance.name}"
}

resource "google_sql_user" "users" {
  name     = "${var.dbuser}"
  instance = "${google_sql_database_instance.instance.name}"
  host     = "*"
  password = "${var.dbpassword}"
}

