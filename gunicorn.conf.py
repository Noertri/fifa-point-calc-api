import multiprocessing as mp


bind = ["0.0.0.0:5000"]
worker = mp.cpu_count()*2+1
wsgi_app = "wsgi:app"
accesslog = "/var/log/gunicorn/api_access.log"
errorlog = "/var/log/gunicorn/api_error.log"
