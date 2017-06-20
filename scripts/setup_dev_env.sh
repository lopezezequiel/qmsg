sudo apt-get install python-pip python-virtualenv;
git clone git@github.com:lopezezequiel/agiles-ci.git
cd agiles-ci
virtualenv env
source env/bin/activate
pip install -r requirements.txt
python manage.py migrate
