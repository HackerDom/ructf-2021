echo "---BEGIN SERVICE PRIVATE KEY---"
cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 320000 | head -n 1
echo "---END SERVICE PRIVATE KEY---"
