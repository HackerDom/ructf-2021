source "virtualbox-ovf" "studio" {
  source_path = "base.ova"
  ssh_username = "root"
  ssh_private_key_file = "keys/id_rsa"

  headless = true
}

build {
  sources = ["sources.virtualbox-ovf.studio"]

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
      "sudo apt install -y -q redis-server",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",
    ]
  }

  provisioner "file" {
    source = "../container-svc/"
    destination = ~/container-svc/"
  }

  provisioner "file" {
    source = "../build.sh"
    destination = ~/container-svc/"
  }

  provisioner "file" {
    source = "../bin/"
    destination = "/usr/bin/studio/"
  }

  provisioner "shell" {
    inline = [
      "~/build.sh",
    ]
  }

  provisioner "file" {
    source = "../studio.service"
    destination = "/etc/systemd/system/studio.service"
  }
}