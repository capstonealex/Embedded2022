# Read current values
cat /proc/sys/net/core/rmem_max
cat /proc/sys/net/core/rmem_default

# # Temporarily set new values. To permanently set, do it via sysctl.conf
echo 212992 | sudo tee /proc/sys/net/core/rmem_max
echo 212992 | sudo tee /proc/sys/net/core/rmem_default
