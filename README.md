**Infraestrutura Kafka [24E1_2]**

Marcus Vinicius Barreto Siqueira

1. Escolha 5 conceitos fundamentais sobre o Apache Kafka e os descreva.
    1. Arquitetura de Pub/Sub (Publicação e Consumo) através de tópicos, que são cadastrados e podem receber dados através de publicação nos tópicos, enquanto que consumidores se cadastram em um tópico para leitura dos dados.
    2. Armazenar fluxos de registros de forma eficaz na ordem em que os registros foram gerados.
    3. Processar fluxos de registros em tempo real, onde o Kafka a possibilidade de trabalhar com dados em tempos reais e próximo de tempos reais, como Kafka sendo utilizado em grandes corporações como Netflix, serviço de streaming.
    4. Possibilidade de possuir uma fila morta, onde o que der erro não será descartado e poderá posteriormente ser reprocessado.
    5. Arquitetura que proporciona escalabilidade, onde há a possibilidade de adicionar novos producers, novos consumers, e novos brokers, onde os brokers permitem a escalabilidade do Kafka.
2. Descreva como é a arquitetura do Apache Kafka.
    1. O Kafka possui uma série de Brokers que são responsáveis por gerenciar o Kafka, onde quanto mais Brokers maior a capacidade de possuir producers e consumers. Producers ou produtores são aqueles que se conectam a estrutura Kafka para produzir dados, enquanto que consumers, ou consumidores são aqueles que se conectam ao kafka para consumir dados. Os dados são cadastrados e consumidos através de tópicos.
3. Apresente exemplos de utilização do Apache Kafka em bases NoSQL e SQL.
    1. Bases NoSQL tem padrão JSON e Kafka tem possibilidade de leitura serializada. Através de conectores o kafka pode se conectar em bancos de dados SQL como Postgresql.
4. Descrevas os principais benefícios em utilizar o Apache Kafka.
    1. Estrutura robusta e a facilidade de trabalhar com dados em tempo real, de forma escalável.
5. O que é um pipeline de dados?
    1. Um pipeline de dados é uma sequência de etapas interconectadas que permitem a coleta, armazenamento, transformação, análise e visualização de dados.
6. Dê 2 (dois) exemplos de aplicações onde os pipelines de dados são utilizados em seu dia-a-dia.
    1. Extração, tratamento e armazenamento de dados de clientes e fornecedores, atravéz de um sistema proprietário de aquisição e transporte de dados, desenvolvido em Python.
    2. Extração de dados do Google Cloud Storage, transformação e carregamento dos dados no Google Big Query, através de códigos em Python, executados através do Apache Airflow.
7. Selecione uma base de dados pública brasileira para utilizar neste exercício. Você pode baixá-la em algum formato que desejar (ex.: formato .csv). Informe onde e como você conseguiu os seus dados. Explique se são estruturados ou não estruturados. Cada linha/registro em seu banco de dados corresponde a quais informações? Cada registro possui quantas colunas associadas e quais atributos elas representam? Qual o tamanho do banco de dados escolhido?
    1. A Base pública a ser utilizada é do [discogs.com](http://discogs.com) através da API pública de consulta. Após a transformação dos dados obtidos, cada linha ou registro, corresponde ao nome do artista, nome do disco, e uma chave unica que é a junção do nome do artista com o nome do disco, para evitar repetições, e data de lançamento do disco. A tabela possui 4 colunas totais. O banco de dados tem a possibilidade de ter varios registros, mas para fins de estudo e teste foram usados 200 dados. ( A api possibilita muito mais dados, mas o consumo é um dado por vez, e com um tempo de intervalo para obtenção do dados ).
8. Formule pelo menos 2 perguntas sobre sua base de dados. O que você quer saber sobre os dados que escolheu?
    1. É possivel saber quantidade de lançamentos de um artista (A amostragem de dados utilizadas para teste é pequena dado a API de destino ter limitações para requisições não autenticadas, mas é possivel em um periodo maior de coleta, ter mais amostragem de dados).
    2. É possivel saber data de lançamento de um disco.
9. Formule uma hipótese sobre o que você acha que vai encontrar quando filtrar e analisar seus dados.
    1. Dado que a origem dos dados é Discogs, que se refere a discos, a tendencia é que nos anos mais recentes, o numero de discos seja menor, sendo assim se a API rodasse por bastante tempo coletando algo volume de dados, armazenando tudo no tópico, uma analise futura iria mostrar que discos de música, físico diminuiram com o surgimento de streaming de audio.
10. Crie uma nova variável a partir de outras variáveis da base de dados que te auxilie na avaliação de sua hipótese.
    1. Para avaliar minha hipotese seria necessarário alterar o valor da variavel global no Python API_TITLE_START para um numero maior que corresponde a lançamentos mais recentes, armazenar em outro topico e de lá já seria possível comprar a quantidade de discos de uma cenario atual com o cenario que está sendo utilizado por padrão (que está iniciando em um disco de ID referente ao ano de 1999).
11. Importe a sua base de dados na infraestrutura Kafka. Inclua em seu relatório a forma que você realizou a importação.
    1. Está sendo feito no arquivo kafka_python_test.py 
    É necessario ter o python instalado e as libs adicionados através do requirements.txt. Todo o teste foi realizando localmente utilizando a estrutura do docker, com comando docker-compose up.
12. Realize pré-processamento dos dados importados. Inclua eu seu relatório os códigos utilizados para o pré-processamento e criação de novas variáveis.
    1. Segue no repo do git os arquivos todos utilizados.
    Link: https://github.com/msiqueira-dev/infnet-01-kafka-python
13. Inclua em seu relatório o código fonte necessário para definir e executar um pipeline que implemente, na ordem correta, todos os passos de pré-processamento que você escolheu para analisar sua base de dados.
    1. Segue no repo do git os arquivos todos utilizados.
    Link: https://github.com/msiqueira-dev/infnet-01-kafka-python
14. Insira em seu relatório um esquema que represente o funcionamento de seu pipeline de dados.
    1. 
15. Exporte os seus dados processados em formato .csv e importe em um software de visualização. Se possível, você também pode integrar diretamente o Apache Kafka com uma ferramenta de visualização.
    1.
16. Utilizando a ferramenta de visualização, crie gráficos (no mínimo dos gráficos, um de barras e um de dispersão) um suportem as suas conclusões com relação às hipóteses investigadas.
    1. Foi criado um grafico de barras e para facilitação um arquivo .jpg foi anexado, mas caso necessário o programa, kafka_python_test.py, pode ser executado para gerar o gráfico, assim como é possivel alterar os parâmetros das variaveis globais no mesmo arquivo para aumentar ou diminuir a massa de dados obitidos da API do discogs.
17. Por fim, escreva um texto em seu relatório fazendo uma análise final, tendo em vista os resultados obtidos. Responda às perguntas que fez no início do exercício e discuta se sua hipótese foi confirmada ou refutada.
    1. As perguntas inicialmente foram respondidas após o projeto ja ter sido iniciado em python e os dados ja analisados, e na atualidado o lançamento de discos físicos se torna praticamente um item de colecionador, então é possivel observar que a massa de dados é menor para os anos mais recentes.