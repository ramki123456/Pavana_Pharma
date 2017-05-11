import os
import webbrowser

try:
    webbrowser.open('http://127.0.0.1:8000')
    os.system('python /home/brahma/Desktop/Pavana_Pharma/Pavana_Pharma/manage.py runserver')
except:
    webbrowser.open('http://127.0.0.1:8000')
