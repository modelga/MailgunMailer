import subprocess

from app import app


@app.route('/deploy', methods=['GET', 'POST'])
def deploy():
    try:
        subprocess.call("/srv/app/deploy.sh &", shell=True)
        return 'OK Deploy is running'
    except:
        return 'Something BAD Happend'
