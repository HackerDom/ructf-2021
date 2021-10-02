packer {
  required_plugins {
    digitalocean = {
      version = ">= 1.0.0"
      source  = "github.com/hashicorp/digitalocean"
    }
  }
}

variable "api_token" {
  type = string
}

source "digitalocean" "vuln_image" {
  api_token    = var.api_token
  image        = "ubuntu-20-04-x64"
  region       = "ams3"
  size         = "s-2vcpu-4gb"
  ssh_username = "root"
}

build {
  sources = ["source.digitalocean.vuln_image"]

  provisioner "shell" {
    inline_shebang = "/bin/sh -ex"
    environment_vars = [
      "DEBIAN_FRONTEND=noninteractive",
    ]
    inline = [
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",

      "apt-get clean",
      "apt-get update",

      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",

      "apt-get upgrade -y -q -o Dpkg::Options::='--force-confdef' -o Dpkg::Options::='--force-confold'",

      # Install docker and docker-compose
      "apt-get install -y -q apt-transport-https ca-certificates curl gnupg lsb-release",
      "curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -",
      "add-apt-repository \"deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable\"",
      "apt-get update",
      "apt-get install -y -q docker-ce",
      "curl -L \"https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)\" -o /usr/local/bin/docker-compose",
      "chmod +x /usr/local/bin/docker-compose",
      
      # Install haveged, otherwise docker-compose may hang: https://stackoverflow.com/a/68172225/1494610
      "apt-get install -y -q haveged",

      # Add users for services
      "useradd -m -u 10000 -s /bin/bash employeexer",
      "useradd -m -u 10001 -s /bin/bash studio",
      "useradd -m -u 10002 -s /bin/bash metrics",
      "useradd -m -u 10003 -s /bin/bash white_album",
      "useradd -m -u 10004 -s /bin/bash spotiflag",
      "useradd -m -u 10005 -s /bin/bash trackbattle",
    ]
  }

  ### Ructf motd
  provisioner "shell" {
    inline = [
      "rm -rf /etc/update-motd.d/*",
    ]
  }
  provisioner "file" {
    source = "roles/base_image/files/ructf-banner.txt"
    destination = "/ructf-banner.txt"
  }
  provisioner "file" {
    source = "roles/base_image/files/00-header"
    destination = "/etc/update-motd.d/00-header"
  }
  provisioner "file" {
    source = "roles/base_image/files/10-help-text"
    destination = "/etc/update-motd.d/10-help-text"
  }
  provisioner "shell" {
    inline = [
      "chmod +x /etc/update-motd.d/*",
    ]
  }

  ### Copy services

  # Employeexer service

  provisioner "file" {
    source = "../services/employeexer/"
    destination = "/home/employeexer/"
  }

  # Metrics service

  provisioner "file" {
    source = "../services/metrics/"
    destination = "/home/metrics/"
  }

  # white_album service

  provisioner "file" {
    source = "../services/white_album/"
    destination = "/home/white_album/"
  }

  # white_album service

  provisioner "file" {
    source = "../services/spotiflag/"
    destination = "/home/spotiflag/"
  }

  # trackbattle service

  provisioner "file" {
    source = "../services/trackbattle/"
    destination = "/home/trackbattle/"
  }

  # Studio service
  provisioner "shell" {
    inline = [
      "cd ~studio",
      "mkdir image",
    ]
  }

  # For two following steps you need to run build scripts from ../services/studio/image first
  # And move image in /home/images/studio/packer-studio.ova
  provisioner "file" {
    source = "/home/images/studio/packer-studio.ova"
    destination = "/home/studio/image/packer-studio.ova"
  }
  provisioner "file" {
    source = "/home/images/studio/studio-vm.service"
    destination = "/etc/systemd/system/studio-vm.service"
  }
  provisioner "file" {
    source = "keys"
    destination = "/home/studio/"
  }

  provisioner "shell" {
    inline = [
      "cd ~employeexer",
      "docker-compose up --build -d || true",
    ]
  }

  provisioner "shell" {
    inline = [
      "cd ~metrics",
      "docker-compose up --build -d || true",
    ]
  }

  provisioner "shell" {
    inline = [
      "cd ~white_album",
      "docker-compose up --build -d || true",
    ]
  }

  provisioner "shell" {
    inline = [
      "cd ~spotiflag",
      "docker-compose up --build -d || true",
    ]
  }

  provisioner "shell" {
    inline = [
      "cd ~trackbattle",
      "docker-compose up --build -d || true",
    ]
  }

  provisioner "shell" {
    inline = [
      "cd ~studio",
      # Wait apt-get lock
      "while ps -opid= -C apt-get > /dev/null; do sleep 1; done",
      "apt-get -y -q install virtualbox",
  
      "systemctl daemon-reload",
  
      # Enable auto-start for VirtualBox VM. See https://kifarunix.com/autostart-virtualbox-vms-on-system-boot-on-linux/
      "mkdir -p /etc/vbox",
      "echo 'VBOXAUTOSTART_DB=/etc/vbox' | tee -a /etc/default/virtualbox",
      "echo 'VBOXAUTOSTART_CONFIG=/etc/vbox/autostartvm.cfg' | tee -a /etc/default/virtualbox",
      "echo 'default_policy = allow' | tee /etc/vbox/autostartvm.cfg",
      "VBoxManage setproperty autostartdbpath /etc/vbox/",

      "VBoxManage import image/packer-studio.ova --vsys 0 --vmname Studio",
      "VBoxManage modifyvm Studio --autostart-enabled on",
      "VBoxManage modifyvm Studio --cpus 4",
      "VBoxManage modifyvm Studio --memory 8192",
      "VBoxManage modifyvm Studio --natpf1 'serviceport,tcp,0.0.0.0,8000,,8000'",
      "VBoxManage modifyvm Studio --natpf1 'sshport,tcp,127.0.0.1,22,,2222'",

      "systemctl start studio-vm",
      "systemctl enable studio-vm",
    ]
  }

  # Fix some internal digitalocean+cloud-init scripts to be compatible with our cloud infrastructure
  provisioner "shell" {
    script = "digital_ocean_specific_setup.sh"
  }

  provisioner "shell" {
    inline = [
      "docker image prune --filter label=stage=builder -f",
    ]
  }
}
