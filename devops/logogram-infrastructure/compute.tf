
data "google_compute_zones" "available" {}

resource "google_compute_instance" "logogram-instance" {
  project      = "${var.project}"
  zone         = "${var.zone}"
  name         = "logogram-instance"
  machine_type = "g1-small"
  tags = ["http-firewall"]

  boot_disk {
    initialize_params {
      image = "logogram-base-image"
    }
  }

  network_interface {
    network = "default"

    access_config {
      nat_ip = "${var.ip-address}"
    }
  }

  metadata_startup_script = "${file("deploy_logogram.sh")}"

  metadata {
    ipAddress    = "${var.ip-address}"
  }
}
