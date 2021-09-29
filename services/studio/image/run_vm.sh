#!/bin/bash

VBoxManage import "output-studio/$1.ova"
VBoxManage startvm "$1" --type headless