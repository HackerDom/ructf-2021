source "virtualbox-iso" "sandbox" {
  guest_os_type = "Ubuntu_64"
  iso_url = "http://releases.ubuntu.com/20.04/ubuntu-20.04.3-live-server-amd64.iso"
  ssh_username = "packer"
  ssh_password = "packer"
  iso_checksum = "sha1:a6077cb573271ec3c85f9d8abb60c60471dcb73b"

  memory = 1024

  shutdown_command = "echo 'packer@docker.sandbox.2021.ctf.hitb.org' | sudo -S shutdown -P now"

  export_opts = [
    "--manifest",
    "--vsys", "0",
    "--description", "Studio",
    "--version", "1.0.0"
  ]
}

build {
  sources = ["sources.virtualbox-iso.sandbox"]

  provisioner "file" {
    source = "../keys/id_rsa.pub"
    destination = "~/id_rsa.pub"
  }

  provisioner "shell" {
    inline = [
      "sudo apt install -y redis-server",
    ]
  }
}