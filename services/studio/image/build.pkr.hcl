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

      "dpkg --add-architecture i386",
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

      # Install ssl
      "sudo apt install libssl-dev:i386",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",
    ]
  }

  provisioner "file" {
    source = "../container-svc/"
    destination = "~/"
  }

  provisioner "file" {
    source = "../bin/"
    destination = "/usr/bin/"
  }

  provisioner "shell" {
    inline = [
      "cd container-svc",
      "./build.sh",
      "mv container-service-gin /usr/bin/container-svc",
    ]
  }

  provisioner "file" {
    source = "../studio.service"
    destination = "/etc/systemd/system/studio.service"
  }

  provisioner "file" {
    source = "../studio.service"
    destination = "/etc/systemd/system/studio.service"
  }

  provisioner "file" {
    source = "redis.conf"
    destination = "/etc/redis/redis.conf"
  }

  provisioner "shell" {
    inline = [
      "sudo systemctl daemon-reload",
      "sudo systemctl enable studio.service",
      "sudo systemctl enable redis.service",
    ]
  }
}