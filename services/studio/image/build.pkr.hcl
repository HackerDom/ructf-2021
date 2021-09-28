source "virtualbox-iso" "studio" {
  guest_os_type = "Ubuntu_64"
  iso_url = "http://releases.ubuntu.com/20.04/ubuntu-20.04.3-live-server-amd64.iso"
  ssh_username = "packer"
  ssh_password = "packer"
  iso_checksum = "sha1:a6077cb573271ec3c85f9d8abb60c60471dcb73b"

  memory = 4096

  shutdown_command = "echo 'packer@packer' | sudo -S shutdown -P now"

  export_opts = [
    "--manifest",
    "--vsys", "0",
    "--description", "Studio",
    "--version", "1.0.0"
  ]

  headless = true
}

build {
  ssh_username = "packer"
  ssh_password = "packer"
  
  sources = ["sources.virtualbox-iso.studio"]

  provisioner "file" {
    source = "keys/id_rsa.pub"
    destination = "~/.ssh/id_rsa.pub"
  }

  provisioner "shell" {
    inline = [
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",

      "apt-get clean",
      "apt-get update",

      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",

      "apt-get upgrade -y -q -o Dpkg::Options::='--force-confdef' -o Dpkg::Options::='--force-confold'",

      # Install docker and docker-compose
      "apt-get install -y -q apt-transport-https ca-certificates nfs-common",
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
      "add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"",
      "apt-get update",
      "apt-get install -y -q docker-ce",
      "curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
      "chmod +x /usr/local/bin/docker-compose",

      # Install redis
      "sudo apt install -y redis-server",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",
    ]
  }

  provisioner "file" {
    source = "../container-svc/"
    destination = "/home/studio/"
  }

  provisioner "file" {
    source = "../bin/"
    destination = "/usr/bin/studio/"
  }
}