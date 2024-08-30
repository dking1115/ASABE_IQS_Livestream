# Set up service
copy dwm_startup.service to /etc/systemd/system/
sudo systemctl enable dwm_startup.service
sudo systemctl start dwm_startup.service


# Running from launch file
ros2 launch content_node content_node.launch.py