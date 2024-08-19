import os
from celery import Celery

# задать стандартный модуль настроек Django
# для программы 'celery'.
#amqps://uebnofyc:hFhiv9SiD_6zOsuhlFfdp_tZGiwC2zcP@shrimp.rmq.cloudamqp.com/uebnofyc
#amqp://guest@localhost//

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
app = Celery('config', broker='amqps://uebnofyc:hFhiv9SiD_6zOsuhlFfdp_tZGiwC2zcP@shrimp.rmq.cloudamqp.com/uebnofyc')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()



@app.task(bind=True)
def debug_task(self):
    print(f'Request {self.request!r}')



#, backend="redis://localhost:6379"