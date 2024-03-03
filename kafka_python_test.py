import datetime
import json
#pip install pandas
import pandas
import time

#pip install kafka-python
from kafka import KafkaProducer
from kafka import KafkaConsumer

from helpers import Helpers
from model_api import Model_Api

KAFKA_BOOSTRAP_SERVER = 'localhost:9093'
TITLES_MAX = 5
TITLE_START = 14602

my_list = []
host = 'api.discogs.com'
model_api_obj = Model_Api()
model_api_obj.url_parameters_add({'page': '1'})
model_api_obj.url_parameters_add({'per_page': '2'})


producer = KafkaProducer(bootstrap_servers=[KAFKA_BOOSTRAP_SERVER])
print(f'Iniciando o Kafka producer at {datetime.datetime.utcnow()}')

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
    my_dict['unique_name'] = f"{my_dict['artist']}_{my_dict['title']}"
    if Helpers.list_json_exists_by_key(my_list, 'unique_name', my_dict['unique_name']) is None:
        my_list.append(my_dict)
    TITLE_START +=1
    print(len(my_list))
    print(TITLES_MAX)
    time.sleep(1)

#Realiza a leitura do arquivo csv, converte para o formato dicionário e envia as mensagens para o tópico com o producer
topic_name = 'data-topic-discogs'
n = 0
for item in my_list:
    key = str(n).encode('utf-8')
    ack = producer.send(topic=topic_name, key=key, value=json.dumps(item).encode('utf-8'))
    metadata = ack.get()
    n +=1
    print(metadata.topic, metadata.partition, key)

producer.flush()
print(f"Wrote {n} messages into topic: {topic_name}")

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