# flask_asr

sudo apt-get install python3-pip python3-dev nginx
sudo pip3 install virtualenv


virtualenv venv
pip install -r requirements.txt


#wsgi test
uwsgi --socket 0.0.0.0:5000 --protocol=http -w wsgi:app


#start
sudo nano /etc/systemd/system/myproject.service
***
[Unit]
Description=uWSGI instance to serve myproject
After=network.target

[Service]
User=sammy
Group=www-data
WorkingDirectory=/home/sammy/myproject
Environment="PATH=/home/sammy/myproject/myprojectenv/bin"
ExecStart=/home/sammy/myproject/myprojectenv/bin/uwsgi --ini myproject.ini

[Install]
WantedBy=multi-user.target
***
sudo systemctl start myproject
sudo systemctl enable myproject


sudo systemctl restart nginx




# firewall
sudo ufw allow 5000
sudo ufw delete allow 5000
sudo ufw allow 'Nginx Full'
