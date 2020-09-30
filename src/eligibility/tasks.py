from backend.celery import app
from .models import EligibilityQueue
from iep.models import ClientIEP


@app.task
def enqueue_eligibility():
    ieps = ClientIEP.objects.filter(client__is_new=False, end_date=None)
    for iep in ieps:
        EligibilityQueue.objects.create(client=iep.client, requestor=None)
