from .tasks import  gereration
from config import shared
from rest_framework import views
import redis
import requests
from rest_framework.response import Response
from .models import Urls
from .hesch_site import S3Client, text_which
import requests
from rest_framework.decorators import api_view
import os
import sys
from .producer import publish
from django.core.cache import cache
from asgiref.sync import sync_to_async




@api_view(['GET'])
def index(request, pk):
    
    text_cache = cache.get(pk)
    if text_cache:
        print('Текст из кеша')
        return Response(text_cache)
    else:
        url = Urls.objects.filter(hashc=pk)
        
        print('Текст из базы')
        if url:
            try:
                res = requests.get(url[0].url)
                if res.status_code != 200:
                    text = 'Ошибка'
                else:
                    text = res.text
                    cache.set(pk, text, 1000)
            except:
            
                text = 'Ошибка'
        else:
            return Response('Сыылка не найдена')
    
    return Response(text)


@api_view(['GET'])
def create_pdf(request, ip, id):
    
    room = ip + id
    print(room)
    res = gereration.delay(room, id)
    return Response('llllllll')

class IndexAPIView(views.APIView):
    def post(self, request):
        
        
        s3_client = S3Client(
        access_key="f24818ba24ab42f080c0debddf38a43d",
        secret_key="19bdbb659fca45d3bc02a338d1fe798b",
        endpoint_url="https://s3.storage.selcloud.ru", 
        bucket_name="post-public1"
    )
        text_post = request.data['body']
        byte_size = sys.getsizeof(text_post)
        print(byte_size)
        if byte_size > 11000000:
            return Response({'status' : '2',
                         'url' : 'Размер текста превышен, максимальный размер 10 мб',
                         })
        if not text_post:
            return Response({'status' : '1',
                         'url' : 'Поле ввода пусто',
                         })
       
      
        r = redis.Redis(host='localhost', port=6379, db=0)
        l = r.llen('hesc')
        #r.delete('asgi:group:indicator')
        if l < 100:
            requests.get("http://localhost:8000/api/v1/50/")
        if l < 3950:
            print(l, 'qqqqqqqq')
            publish()
            #hesch_gereration.delay()
        j = r.lpop('hesc')
        
        hasch_link = j.decode("utf-8")
        link = f'http://localhost:8080/{hasch_link}'
        text_which(text_post, hasch_link)
        try:
            s3_client.upload_file(rf'{hasch_link}.txt')
        except:
            return Response({'status' : '3',
                         'url' : 'Текст не сохранен',
                         })
        
        os.remove(rf'{hasch_link}.txt')
        if hasch_link and text_post:
            url_s3 = f'https://d36ca4c9-a6c7-477a-b301-3a26d80c7968.selstorage.ru/{hasch_link}.txt'
            
            url = Urls(hashc=hasch_link, url=url_s3)
            url.save()
            text_cache = cache.set(hasch_link, text_post, 1000)
            return Response({'status' : '200',
                         'url' : link,
                         })
        else:
            return Response({'status' : '3',
                         'url' : 'Текст не сохранен',
                         })