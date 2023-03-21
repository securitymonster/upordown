Quick notes for setting up on raspberry PI


# SYSTEM SERVICE on Raspberry
/etc/systemd/system/upordown.service:

# start of file
[Unit]
Description=Seb's Up Or Not Script
After=multi-user.target

[Service]
Type=idle
ExecStart=/usr/bin/python3 /usr/local/bin
Restart=always

[Install]
WantedBy=multi-user.target
# end of file

sudo systemctl daemon-reload
sudo systemctl enable upornot
sudo systemctl start upornot


# LOGROTATE on Raspberry
Assuming logrotate is configure in cron somewhere, for instance in /etc/cron.daily/logrotate.

/etc/logrotate.d/updown:

# start of file
/var/log/upordown.csv {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 640 pi pi
}
# end of file

Test with:

sudo logrotate -vf /etc/logrotate.d/updown



