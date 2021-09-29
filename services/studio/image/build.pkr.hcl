source "virtualbox-ovf" "studio" {
  source_path = "base.ova"
  ssh_username = "root"
  ssh_private_key_file = "keys/id_rsa"

  vboxmanage = [
    ["modifyvm", "{{.Name}}", "--memory", "8096"],
    ["modifyvm", "{{.Name}}", "--cpus", "4"]
  ]

  shutdown_command = "echo 'packer' | sudo -S shutdown -P now"

  headless = true
  format= "ova"
}

build {
  sources = ["sources.virtualbox-ovf.studio"]

  provisioner "shell" {
    inline = [
      #
      # Wait apt-get lock
      #
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",

      #
      # Update core packages
      #
      "apt clean",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",
      "apt update",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",
      "apt-get upgrade -y -q -o Dpkg::Options::='--force-confdef' -o Dpkg::Options::='--force-confold'",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",

      #
      # Install docker and docker-compose
      #
      "apt install -y -q apt-transport-https ca-certificates nfs-common",
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
      "add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"",
      "apt update",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",
      "apt install -y -q docker-ce",
      "curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
      "chmod +x /usr/local/bin/docker-compose",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",

      #
      # Install redis
      #
      "apt install -y -q redis-server",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",

      #
      # Install ssl 
      #
      "dpkg --add-architecture i386",
      "apt update",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",
      "apt install -y -q libssl-dev:i386",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",
    ]
  }

  provisioner "file" {
    source = "../container-svc"
    destination = "~/container-svc"
  }

  provisioner "file" {
    source = "../bin"
    destination = "/usr/bin/studio"
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
    inline = ["cd ~/container-svc", "./build.sh"]
  }

  provisioner "shell" {
    inline = [
      "systemctl daemon-reload",
      "systemctl enable studio.service",
      "systemctl enable redis-server.service",
    ]
  }
}