#!/bin/bash

VBoxManage import "output-studio/$1.ova" && echo '[imported]' && \
#VBoxManage modifyvm "$1" --natpf1 "ssh,tcp,,2222,,22" && echo '[ssh forwarded]' && \
VBoxManage modifyvm "$1" --natpf1 "service,tcp,,8000,,8000" &&  echo '[service forwarded]' && \
VBoxManage startvm "$1" --type headless && echo '[vm started]' 
