import subprocess
import os
import re
import signal


try:
    proc = subprocess.Popen(
        ["ps auxw | grep runserver"], stdout=subprocess.PIPE, shell=True)
    (out, err) = proc.communicate()

    id_ = [id_val for id_val in out.splitlines() if "python /Users/HARI/Documents/Pavana_Pharma/manage.py runserver" in id_val]

    id_ = re.findall(r'\d+', id_[0])[0]
    os.kill(int(id_), signal.SIGQUIT)
except:
    pass
