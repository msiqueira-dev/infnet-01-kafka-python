import ast
import csv
import datetime
import json
import sys
import subprocess
import time 

#pip install kafka-python
from kafka import KafkaProducer
from kafka import KafkaConsumer
from kafka.admin import KafkaAdminClient, NewTopic
from kafka.structs import TopicPartition

from helpers import Helpers
from model_api import Model_Api
from GraphMatPlot import GraphMatPlot

KAFKA_BOOSTRAP_SERVER = 'localhost:9093'
API_TITLES_MAX = 200
API_TITLE_START = 14602
TOPIC_NAME = 'data-topic-discogs'
RESTART_TOPIC_IF_CREATED = True

my_list = []
host = 'api.discogs.com'
model_api_obj = Model_Api()
model_api_obj.url_parameters_add({'page': '1'})
model_api_obj.url_parameters_add({'per_page': '2'})


#Excluindo Tópico
if RESTART_TOPIC_IF_CREATED:
    try:
        admin_client = KafkaAdminClient(bootstrap_servers=[KAFKA_BOOSTRAP_SERVER])
        admin_client.delete_topics([TOPIC_NAME])
        print("Topico excluido, recriando")
        time.sleep(5)
    except Exception as e:
        if 'UnknownTopicOrPartitionError: Request' in str(e):
            print(f"Tópico {TOPIC_NAME} não existe, por tanto não necessário apagar")
        else:
            print(e)
#Criando Tópico
try:
    topic_list = [NewTopic(name=TOPIC_NAME, num_partitions=1, replication_factor=1)]
    admin_client.create_topics(new_topics=topic_list, validate_only=False)
    print("Topico recriado com sucesso")
    time.sleep(5)
except Exception as e:
    if f"[Error 36]" in str(e):
        print(f"Topico {TOPIC_NAME} já existe")

#Criando o producer
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

#Lendo dados da API Discogs, utilizando a biblioteca de minha autoria que le genericamente APIS
skipper = 0 
while len(my_list) < API_TITLES_MAX:
    content = model_api_obj.get(host, f'/artists/{API_TITLE_START}/releases?', True)
    ret = model_api_obj.recursively_content_json(content)
    my_dict = {}
    for item in model_api_obj.list_result:
        if 'artist' in item:
            my_dict['artist'] = item['artist'].replace('\\', '-').replace('//', '-')
        elif 'title' in item:
            my_dict['title'] = item['title'].replace('\\', '-').replace('//', '-')
        elif 'year' in item:
            my_dict['year'] = item['year']
    if my_dict:
        if my_dict['artist'] and my_dict['title']:
            my_dict['unique_name'] = f"{my_dict['artist']}_{my_dict['title']}"
            if Helpers.list_json_exists_by_key(my_list, 'unique_name', my_dict['unique_name']) is None:
                skipper = 0
                my_list.append(my_dict)
                msg  = f"Adicionando item {API_TITLE_START} a lista. Atualmente a lista "
                msg += f"possui {len(my_list)} elementos, de um total de {API_TITLES_MAX}"
                print(msg)
            else:
                skipper = skipper + 2
            API_TITLE_START = API_TITLE_START + 1 + skipper
            print(f"Título atual {API_TITLE_START}: Unique_Name: {my_dict['unique_name']}")
    time.sleep(3)
print(f"Itens na lista a enviados ao Kafka: {len(my_list)}")

#Enviando dados recebidos da API para o Kafka, através do produtor anteriormente criado
counter = 0
for item in my_list:
    key = str(counter).encode('utf-8')
    try:
        ack = producer.send(topic=TOPIC_NAME, key=key, value=json.dumps(item).encode('utf-8'))
        metadata = ack.get()
    except Exception as e:
        if 'is not defined' in str(e):
            print("Producer não foi definido, verificar se kafka está respondendo")
        else:
            print(e)
    counter +=1
try:
    producer.flush()
    print(f"Escreveu {counter} mensagens no tópico: {TOPIC_NAME}")
except Exception as e:
    if 'is not defined' in str(e):
        print("Producer não foi definido, verificar se kafka está respondendo")


#Cria um consumidor para obter os dados do kafka a partir de uma partição no topico especifico anteriormente criado
list_artist = []
list_title = []
list_year = []
consumer = KafkaConsumer(TOPIC_NAME, bootstrap_servers=KAFKA_BOOSTRAP_SERVER, 
                        auto_offset_reset='earliest', enable_auto_commit=False,
                        consumer_timeout_ms = 10000)
partitions = consumer.partitions_for_topic(TOPIC_NAME)
for p in partitions:
    topic_partition = TopicPartition(TOPIC_NAME, p)
    consumer.seek(partition=topic_partition, offset=0)
    for msg in consumer:
        dict_str = msg.value.decode("UTF-8")
        my_data = ast.literal_eval(dict_str)
        if 'artist' in my_data:
            list_artist.append(my_data['artist'])
        if 'title' in my_data:
            list_title.append(my_data['title'])
        if 'year' in my_data:
            list_year.append(my_data['year'])
    continue

#Prepara os dados obtidos para exibição de grafico usando a matplotlib com uma função feita por minha autoria
list_year.sort()
array_mult = []
array_x = []
for index, year in enumerate(list_year):
    found = False
    counter = 1
    index_update = 0
    for index_mult, item in enumerate(array_mult):
        if item[0] == year:
            found = True
            counter = item[1] + 1
            index_update = index_mult
            break
    if found is False:
        array_mult.append([list_artist[index], list_title[index], year, counter])
        array_x.append(year)
    else:
        array_mult[index_update][3] = counter
array_y = []
for item in array_mult:
    array_y.append(item[3])

#cria arquivo para exportação
with open('output.csv', 'w', newline='', encoding="utf-8") as file:
    writer = csv.writer(file)
    for item in array_mult:
        writer.writerow(item)

#Efetivamente usa GraphMatPlot para exibir os dados em janela com grafico de barras
graph = GraphMatPlot()
graph.axes_total = 1
graph.create_subplot()
title = f"Quantidade de disco lançados por ano com amostragem de {len(array_x)} dados"
bar1 = graph.matplot_create_bargraph(array_x, 'Ano', 'Ano', array_y, "Quantidade", 'Quantidade', title, 0)
graph.show()