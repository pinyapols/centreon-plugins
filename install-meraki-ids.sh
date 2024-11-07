sudo python3 -m pip install requests
sudo curl -O https://raw.githubusercontent.com/pinyapols/centreon-plugins/refs/heads/main/check_meraki_ids.sh
sudo curl -O https://raw.githubusercontent.com/pinyapols/centreon-plugins/refs/heads/main/meraki_ids_allowed_event.py
sudo curl -O https://raw.githubusercontent.com/pinyapols/centreon-plugins/refs/heads/main/meraki_ids_event_count.py
sudo mv ~/check_meraki_ids.sh /usr/lib64/nagios/plugins/
sudo mv ~/meraki_ids_allowed_event.py /usr/lib64/nagios/plugins/
sudo mv ~/meraki_ids_event_count.py /usr/lib64/nagios/plugins/
sudo chown centreon:centreon /usr/lib64/nagios/plugins/check_meraki_ids.sh
sudo chown centreon:centreon /usr/lib64/nagios/plugins/meraki_ids_allowed_event.py
sudo chown centreon:centreon /usr/lib64/nagios/plugins/meraki_ids_event_count.py
sudo chmod 755 /usr/lib64/nagios/plugins/check_meraki_ids.sh
sudo chmod 755 /usr/lib64/nagios/plugins/meraki_ids_allowed_event.py
sudo chmod 755 /usr/lib64/nagios/plugins/meraki_ids_event_count.py