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

