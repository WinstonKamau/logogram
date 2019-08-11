resource "google_compute_instance" "chef-server-instance" {
  project      = "${var.project}"
  zone         = "${var.zone}"
  name         = "chef-infra-server"
  machine_type = "n1-standard-1"
  tags         = ["http-firewall", "https-firewall"]

  boot_disk {
    initialize_params {
      image = "ubuntu-1604-xenial-v20190306"
    }
  }

  network_interface {
    network = "default"
    access_config {
      nat_ip = "${var.ip-address}"
    }	
  }
  metadata_startup_script = "${file("install_chef_server.sh")}"

    metadata {
    hostName    = "${var.hostname}"
  }
}