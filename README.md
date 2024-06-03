# Projeto de Recuperação de Informação

Esse projeto comparar dois algoritmos de recuperação da informação utilizando a biblioteca BEIR.
O projeto foi desenvolvido para a disciplina de recuperação da informação do doutorado em Engenharia de Informatica na Faculdade de Engenharia da Universidade do Porto.



## Dependências, instalação e execução

Para poder executar o Elasticsearch, você deve tê-lo instalado localmente (em seu desktop).
Dependendo do seu sistema operacional, você poderá descobrir como fazer download do Elasticsearch. Eu gosto deste guia para Ubuntu 18.04 - https://linuxize.com/post/how-to-install-elasticsearch-on-ubuntu-18-04/

Para obter mais detalhes, consulte aqui - https://www.elastic.co/downloads/elasticsearch.

Para instalar o projeto

```bash
  pip install requirements.txt
```

Altere nos aquivos project-ir-bm25.py e project-ir-SentenceBERT.py

```bash
  hostname = "your-hostname" 

  index_name = "your-index-name" 
```
    
executar o projeto é só rodar os aquivos

```bash
  python project-ir-bm25.py
  
  python project-ir-SentenceBERT.py
```



# Information Retrieval Project

This project compares two information retrieval algorithms using the BEIR library.
The project was developed for the information retrieval discipline of the PhD in Computer Engineering at the Faculty of Engineering of the University of Porto.

## Dependencies, installation and execution

To be able to run Elasticsearch, you must have it installed locally (on your desktop).
Depending on your operating system, you may be able to find out how to download Elasticsearch. I like this guide for Ubuntu 18.04 - https://linuxize.com/post/how-to-install-elasticsearch-on-ubuntu-18-04/

For more details, see here - https://www.elastic.co/downloads/elasticsearch.

To install the project

```bash
 pip install requirements.txt
```

Change the files project-ir-bm25.py and project-ir-SentenceBERT.py

```bash
 hostname = "your-hostname"

 index_name = "your-index-name"
```

run the project just run the files

```bash
 python project-ir-bm25.py

 python project-ir-SentenceBERT.py
```

### Comandos Elasticsearch

sudo systemctl start elasticsearch

sudo systemctl status elasticsearch

curl -X GET "localhost:9200/"