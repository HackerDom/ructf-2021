#!/bin/bash

VBoxManage controlvm "$1" acpipowerbutton

VBoxManage unregistervm "$1"
