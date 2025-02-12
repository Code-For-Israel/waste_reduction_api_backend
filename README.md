# Waste Reduction Backend
This repo includes:
1. Python Flask backend server used to get information from the inference server, process and store the data in PostgreSQL
2. Dockerfiles & docker-compose configurations for easy launch of the backend including all dependencies


# Launch an instance in AWS

1. Connect to AWS waste-reduction account
2. Create a new EC2 instance from the `Launch instances` wizard
    1. Give it a name
    2. Click `Browse more AMIs`
    3. In search bar search for `ami-013d3da30d7c5977d` and choose from `Community AMIs` - Deep Learning Base AMI (
       Ubuntu 18.04) Version 55.0 (press `Select`)
    4. Instance type: `t2.micro	`
    5. Key pair - choose the `ireland-eu-west-1-waste-reduction-key.pem`
    6. Allow all network traffics
        1. Allow SSH traffic from
        2. Allow HTTPS traffic from the internet
        3. Allow HTTP traffic from the internet
    7. Choose 128GB
    8. Press `Launch instance`
3. To log in to the instance use: `ssh -i ireland-eu-west-1-waste-reduction-key.pem ubuntu@<instance_public_ip>`



```bash
sudo apt-get -y update

# postgresql
sudo apt install postgresql postgresql-contrib
sudo apt-get -y install python-psycopg2
sudo apt-get -y install libpq-dev
sudo systemctl start postgresql.service

# python
cd waste_reduction_api_backend
pip3 install -r requirements.txt 

python3 run.py
```

Note that in case you are using the backend as a service, you should use:
```bash

sudo nano /lib/systemd/system/waste-reduction-backend.service

[Unit]
Description=Waste Reduction Backend Service
After=network-online.target

[Service]
ExecStart=/home/ubuntu/waste_reduction_api_backend/src/start.sh
User=ubuntu

[Install]
WantedBy=multi-user.target


sudo systemctl daemon-reload
sudo systemctl enable waste-reduction-backend.service
sudo systemctl start waste-reduction-backend.service
sudo systemctl status waste-reduction-backend.service
```

