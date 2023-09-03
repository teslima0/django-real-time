"""
from celery import shared_task, Celery
from .models import Test
#from celery.decorators import periodic_task
from celery.schedules import crontab
#from celery

from celery import shared_task, Celery
from .models import Test
from celery.task import periodic_task
from celery.schedules import crontab

app = Celery("your_project_name")  # Replace "your_project_name" with your actual project name
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@app.task
def create_test_object(name):
    Test.objects.create(name=name)

@app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    sender.add_periodic_task(crontab(minute="*/1"), run_create_objs.s())

@app.task
def run_create_objs():
    create_test_object.delay(name='new2020')


@shared_task
def create_test_object(name):
    Test.objects.create(name=name)

@periodic_task(run_every=(crontab(minute='*/1')))
def run_create_objs():
    create_test_object.delay(name='new2020')
app = Celery()

app.conf.beat_schedule = {
    # Executes every day at  12:30 pm.
    'run-every-afternoon': {
        'task': 'tasks.elast',
        'schedule': crontab(hour=12, minute=30),
        'args': (),
    },
}

@shared_task
def create_test_object(name):
    Test.objects.create(name=name)
"""
from celery import Celery,shared_task
import requests
from .models import Test,Position
from  .utils import get_random_code
app = Celery("RealTime")  # Replace "your_project_name" with your actual project name
app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()

@shared_task
def get_crypto_data():
    url = 'https://api.coingecko.com/api/v3/coins/markets?vs_currency=USD&order=market_cap_desc&per_page=100&page=1&sparkline=false'
    data = requests.get(url).json()

    for item in data:
        p, _ = Position.objects.get_or_create(name=item['name'])
        p.image = item['image']
        p.price = item['current_price']
        p.rank = item['market_cap_rank']
        p.market_cap = item['market_cap']
        p.save()

@app.task
def get_crypto_current():
    get_crypto_data.delay()
"""
@app.task
def create_test_object(name):
    Test.objects.create(name=name)

@app.task
def create_all_code():
    for test in Test.objects.all():
        test.code =get_random_code()
        test.save()

@app.task
def run_create_objs():
    create_test_object.delay(name='new2020')
"""
app.conf.beat_schedule = {
    'run-create-objs-every-minute': {
        'task': 'app.task.run_create_objs',  # Replace 'path.to.run_create_objs' with the actual path to the task
        'schedule': 60.0,  # Run every 60 seconds (1 minute)
    },
}
