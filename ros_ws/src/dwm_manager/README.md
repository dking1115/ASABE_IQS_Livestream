# Set up service
copy dwm_startup.service to /etc/systemd/system/
sudo systemctl enable dwm_startup.service
sudo systemctl start dwm_startup.service


# Running from launch file
ros2 launch dwm_manager dwm_manager.launch.py