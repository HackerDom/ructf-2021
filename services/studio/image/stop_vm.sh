#!/bin/bash

VBoxManage controlvm "$1" poweroff

VBoxManage unregistervm "$1"
