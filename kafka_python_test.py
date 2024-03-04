import datetime
import json
#pip install pandas
import pandas
import sys
import subprocess
import time 

#pip install kafka-python
from kafka import KafkaProducer
from kafka import KafkaConsumer

from helpers import Helpers
from model_api import Model_Api

KAFKA_BOOSTRAP_SERVER = 'localhost:9093'
TITLES_MAX = 2
TITLE_START = 14602

my_list = []
host = 'api.discogs.com'
model_api_obj = Model_Api()
model_api_obj.url_parameters_add({'page': '1'})
model_api_obj.url_parameters_add({'per_page': '2'})
producer = None
tries = 0
while producer is None:
    try:
        tries+=1
        if tries > 3:
            print('Máximo tentativas, programa ira abortar.')
            sys.exit(1)
        producer = KafkaProducer(bootstrap_servers=[KAFKA_BOOSTRAP_SERVER])
        print(f'Iniciando o Kafka producer at {datetime.datetime.utcnow()}')
    except Exception as e:
        if 'NoBrokersAvailable' in str(e):
            subprocess.run("docker-compose up")
            print('Falha ao inciar o Kafka, nenhum broker disponível')

n = 0
while len(my_list) < TITLES_MAX:
    content = model_api_obj.get(host, f'/artists/{TITLE_START}/releases?', True)
    ret = model_api_obj.recursively_content_json(content)
    my_dict = {}
    for item in model_api_obj.list_result:
        if 'artist' in item:
            my_dict['artist'] = item['artist']
        elif 'title' in item:
            my_dict['title'] = item['title']
        elif 'year' in item:
            my_dict['year'] = item['year']
    my_dict['unique_name'] = f"{my_dict['artist']}_{my_dict['title']}"
    if Helpers.list_json_exists_by_key(my_list, 'unique_name', my_dict['unique_name']) is None:
        my_list.append(my_dict)
        print(f"Adicionando item único de indice {n} a lista, de um total de {TITLES_MAX} tentativas")
    TITLE_START +=1
    
    time.sleep(1)
print(f"Itens na lista a enviados ao Kafka: {len(my_list)}")

#Realiza a leitura do arquivo csv, converte para o formato dicionário e envia as mensagens para o tópico com o producer
topic_name = 'data-topic-discogs'
n = 0
for item in my_list:
    key = str(n).encode('utf-8')
    try:
        ack = producer.send(topic=topic_name, key=key, value=json.dumps(item))
        metadata = ack.get()
        print(metadata.topic, metadata.partition, key)
    except Exception as e:
        if 'is not defined' in str(e):
            print("Producer não foi definido, verificar se kafka está respondendo")
    n +=1

try:
    producer.flush()
    print(f"Wrote {n} messages into topic: {topic_name}")
except Exception as e:
    if 'is not defined' in str(e):
        print("Producer não foi definido, verificar se kafka está respondendo")

#Crie um consumidor todas as mensagens do tópico, mas não marque como 'lidas' (enable_auto_commit=False)
#para que possamos relê-los quantas vezes quisermos.
consumer = KafkaConsumer(topic_name,
                         group_id = 'Topicos',
                         bootstrap_servers=[KAFKA_BOOSTRAP_SERVER],
                         value_deserializer=lambda m: json.loads(m.decode('utf-8')),
                         auto_offset_reset ='earliest',
                         enable_auto_commit=False,
                         consumer_timeout_ms = 10000
                         )

#Ler o consumidor, concatenar todas as linhas, normalizando o json
lista = []

for message in consumer:
    global combined
    data = pandas.json_normalize(message.value)
    lista.append(data)
    print(data)

Conjunto = pandas.concat(lista)
Conjunto.head(5)