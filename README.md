# 3-tier
sample 3-tier for deployment

create a sample web app : frontend, application layer, database layer
install sqlite locally for visualizing the users in db
create a repo in github, git add ., git commit -m "", git push origin

----->DEPLOYING FLASK WITH NGINX
✅ Prerequisites
Flask app is cloned to EC2
EC2 instance is running Ubuntu
Security group has port 80 open (for HTTP)
🛠 Step-by-Step Deployment Process
1.  connect to the instance
2. update system packages - sudo apt update -y
3. install dependencies - apt install python3-pip python3-venv nginx-y
4. set up flask environment:
- git clone ...........
- cd 3-tier
- python3 -m venv venv
- source venv/bin/activate
- pip install -r requirements.txt #if you get error in this step no file or directory
  . vi requirements.txt
Flask
Flask_SQLAlchemy
gunicorn
5. install and test gunicorn
  pip install gunicorn
gunicorn --bind 127.0.0.1:8000 app:app --daemon    # this deamons helps to run the gunicorn in background # first app means the file name(app.py) and 2nd app means flask instance inside the file i.e., app= Flask(__name__)
Test it internally:  curl http://127.0.0.1:8000
6.Configure NGINX to forward port 80 to Gunicorn (port 8000):
  cd /etc/nginx/sites-available/flask_app
  
        server {
            listen 80;
            server_name YOUR_PUBLIC_IP;
        
            location / {
                proxy_pass http://127.0.0.1:8000;
                proxy_set_header Host $host;
                proxy_set_header X-Real-IP $remote_addr;
            }
        }
Then enable the config:
sudo ln -s /etc/nginx/sites-available/flask_app /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx


Once this is done, you can open your browser and go to: http://<your-EC2-public-IP>
LOADBALANCING WITH AUTOSCALING 
tep-by-Step AWS Deployment (Flask + Gunicorn + NGINX + ASG + ALB)
🔧 1. Prepare Your Flask App
Ensure your Flask app is production-ready with:

requirements.txt

gunicorn as WSGI server

nginx configuration for reverse proxy

📦 2. Create a Custom AMI
Launch an EC2 instance (Amazon Linux or Ubuntu).

SSH into the instance and:

Install Python, pip, nginx, and gunicorn.

Clone your app from GitHub.

Set up a virtual environment.

Run: pip install -r requirements.txt

Configure gunicorn to run on port 8000.

Configure nginx to proxy requests from port 80 to 127.0.0.1:8000.

Enable and start nginx.

Test the app works via browser (use public IP).

Once the setup is tested, go to AWS console → EC2 → Create Image from this instance → Name it e.g. FlaskAppImage.

⚙️ 3. Create a Launch Template
Go to EC2 → Launch Templates → Create new.

Use the AMI you created.

Add required instance type, security groups (allow 80, 8000 if needed).

Add user data only if additional setup is required (e.g., auto-start gunicorn on reboot using systemd).

🌐 4. Create a Target Group
Go to EC2 → Target Groups → Create:

Target type: Instance

Protocol: HTTP

Port: 80

Health Check Path: / (or /login if that's guaranteed available)

Register no targets yet (will be auto-registered by ASG)

🌉 5. Create an Application Load Balancer (ALB)
Go to EC2 → Load Balancers → Create ALB:

Internet-facing, IPv4.

Add listeners on port 80.

In Target Groups, select the one created above.

Security group must allow port 80.

📈 6. Create an Auto Scaling Group (ASG)
Go to EC2 → Auto Scaling → Create ASG:

Choose the Launch Template.

Attach to the ALB you created.

Specify min/max/desired capacity (e.g., 1–2).

Set up health checks (use ELB health check).

Scaling policy: Manual or dynamic (optional for practice).
 1. Check ALB Health and Connectivity
Go to EC2 → Target Groups → Your Target Group

Check if instances show "healthy" status.

Go to Load Balancers → Your ALB

Copy the DNS name and open it in your browser (http://<alb-dns>).

Your Flask app should load successfully.

✅ 2. Check Load Balancing
If you have more than one instance running, ALB will distribute traffic across them.

To confirm:

Modify your Flask app to log or print the instance ID or hostname:

python
Copy code
import socket
@app.route("/")
def home():
    return f"Served from: {socket.gethostname()}"
Deploy this updated app in your AMI or instance.

Refresh the browser multiple times at http://<alb-dns> and observe the instance name — it should alternate if two instances are active.

✅ 3. Check Auto Scaling Triggers (Optional but Recommended)
You can test Auto Scaling by:

Manually increasing instance count in ASG (change Desired Capacity to 2 or more).

Or, simulate CPU load (for example, using a stress tool) if scaling policy is CPU-based:

bash
Copy code
sudo apt install stress
stress --cpu 2 --timeout 120
Then check if a new instance is launched by ASG.

✅ 4. Use CloudWatch Monitoring
Go to CloudWatch → Metrics → Auto Scaling / EC2

View CPU, network traffic, number of instances.

You can also create alarms for scale in/out.

What User Data Does in an ASG Launch?
User data is a startup script that runs when your EC2 instance launches. It usually:

Activates your Python virtual environment (if needed)

Starts the Gunicorn server (gunicorn --bind 127.0.0.1:8000 app:app)

Ensures Nginx is started and configured

Logs errors (optional)

If you didn’t include user data:

Your instance starts from the AMI, but doesn’t automatically launch your app.

So your app is not running, and ALB returns DNS or 502 errors.

✅ Fix It: Add a Proper User Data Script
Edit your Launch Template → Add this user data (adjust paths as needed):

bash
Copy code
#!/bin/bash
cd /home/ubuntu/3-tier
source venv/bin/activate
gunicorn --bind 127.0.0.1:8000 app:app --daemon
systemctl restart nginx
🔁 Then, create a new launch template version with this script and update your ASG to use it.

🧪 To Debug Now
SSH into the instance

Run this manually:

bash
Copy code
cd /home/ubuntu/3-tier
source venv/bin/activate
gunicorn --bind 127.0.0.1:8000 app:app --daemon
sudo systemctl restart nginx
Then open your ALB DNS in the browser.





----------------------------
user data

#!/bin/bash
# Update and install system packages
apt update -y
apt install -y python3-pip python3-venv nginx
git clone
cd 3-tier
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install --upgrade pip
pip install flask gunicorn
pip install flask Flask_SQLAlchemy gunicorn
# Start Gunicorn server in background
nohup venv/bin/gunicorn --bind 127.0.0.1:8000 app:app &

# Configure Nginx
cat <<EOF > /etc/nginx/sites-available/flaskapp

server {
    listen 80;
    server_name localhost;
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }
}
EOF

ln -s /etc/nginx/sites-available/flaskapp /etc/nginx/sites-enabled
rm /etc/nginx/sites-enabled/default
systemctl restart nginx


move to jenkins






