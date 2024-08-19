from celery import shared_task
import requests
import redis
import time
from .producer import publish

from asgiref.sync import async_to_sync
import logging
from channels.layers import get_channel_layer
from django.core.cache import cache
from .models import Urls
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from .hesch_site import S3Client
import os
import sys

channel_layer = get_channel_layer()
logger = logging.getLogger()





@shared_task
def gereration(room, id):
    url = Urls.objects.get(hashc=id)
    if url.urlRDF:
    
        #res = requests.get(url.urlRDF)
        #if res.status_code == 200:
            # f'https://d36ca4c9-a6c7-477a-b301-3a26d80c7968.selstorage.ru/{id}.pdf'
        link = url.urlRDF
        async_to_sync(channel_layer.group_send)(
            room, {"type": "indicato", "text": link}
        )
        return room
    s3_client = S3Client(
        access_key="f24818ba24ab42f080c0debddf38a43d",
        secret_key="19bdbb659fca45d3bc02a338d1fe798b",
        endpoint_url="https://s3.storage.selcloud.ru", 
        bucket_name="post-public1"
    )
    text = cache.get(id)
    if not text:
        url = Urls.objects.filter(hashc=id)
        if url:
            try:
                res = requests.get(url[0].url)
                if res.status_code != 200:
                    text = 'Ошибка'
                    async_to_sync(channel_layer.group_send)(
                        room, {"type": "indicato", "text": text}
                    )
    
                    return room
                else:
                    text = res.text
                    
            except:
                text = 'Ошибка'
                async_to_sync(channel_layer.group_send)(
                        room, {"type": "indicato", "text": text}
                    )
                return room
        else:
            text = 'Ошибка'
            async_to_sync(channel_layer.group_send)(
                        room, {"type": "indicato", "text": text}
                    )
            return room

    byte_size = sys.getsizeof(text)
    if int(byte_size) > 116114:
        text = 'Размер текста слишком большой для PDF'
        async_to_sync(channel_layer.group_send)(
                        room, {"type": "indicato", "text": text}
                    )
        return room

    pdfmetrics.registerFont(TTFont('bold', 'ofont.ru_Lora.ttf'))
    pdfmetrics.registerFont(TTFont('regular', 'Lora-Regular.ttf'))
    
    doc = SimpleDocTemplate(f"{id}.pdf",pagesize=A4,
                        rightMargin=2*cm,leftMargin=2*cm,
                        topMargin=2*cm,bottomMargin=2*cm)
    
    
    doc.build([Paragraph(text.replace("\n", "<br />"), getSampleStyleSheet()['Normal']),])

    try:
        s3_client.upload_file(rf'{id}.pdf')
        link = f'https://d36ca4c9-a6c7-477a-b301-3a26d80c7968.selstorage.ru/{id}.pdf'
        url.urlRDF = link
        url.save()
    except:
        link = 'Ошибка'
        
    async_to_sync(channel_layer.group_send)(
        room, {"type": "indicato", "text": link}
    )
    os.remove(rf'{id}.pdf')
    return room




#"type": "indicato",