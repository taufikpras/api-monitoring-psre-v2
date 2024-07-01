
from src.db_schema.queue_schema import Queue_Schema
from src.core import queue_core, ticket_core
from src.util.crl_verifier import CRL_verifier
from src.util.ocsp_verifier import OCSP_verifier
import src.util.influx_handler as influx_handler

from src import parameters
from celery import Celery

celery_app = Celery('tasks', broker='redis://redis:6379/0', backend='redis://redis:6379/0')

celery_app.conf['CELERY_ENABLE_UTC'] = False
celery_app.conf['CELERY_TIMEZONE'] = parameters.TZ

@celery_app.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    sender.add_periodic_task(180.0, create_periodic_verification.s(), name='add every 180')

@celery_app.task()
def create_periodic_verification():
    crls_q = queue_core.create_crl_queues()
    ocsps_q = queue_core.create_ocsp_queues()
    for crl in crls_q:
        crl_verifier.delay(crl.__dict__)
    
    for ocsp in ocsps_q:
        ocsp_verifier.delay(ocsp.__dict__)

@celery_app.task()
def crl_verifier(queue: dict):
    verifier = CRL_verifier(queue)
    data = verifier.request_crl()
    verifier.verify_crl(data)
    verifier.get_crl_content(data)

    influx_handler.add_crl_metrics(verifier)
    ticket_core.log_ticket(verifier.result)

    return verifier.to_dict()

@celery_app.task()
def ocsp_verifier(queue: dict):
    verifier = OCSP_verifier(queue)
    data = verifier.request_ocsp()
    verifier.verify_ocsp(data)
    verifier.get_ocsp_content(data)
    
    influx_handler.add_ocsp_metrics(verifier)
    ticket_core.log_ticket(verifier.result)

    return verifier.to_dict()