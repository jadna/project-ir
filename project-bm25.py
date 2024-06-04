from beir import util, LoggingHandler
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.lexical import BM25Search as BM25
import pathlib, os
import datetime
import logging
import random
import pandas as pd

random.seed(42)

# Elasticsearch
hostname = "localhost" #localhost
index_name = "scifact" # scifact


logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])


url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(index_name)
out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
data_path = util.download_and_unzip(url, out_dir)

# Forneçe o caminho de dados onde o dataset foi baixado, descompactado e carrega os dados
split = "test"
corpus, queries, qrels = GenericDataLoader(data_path).load(split=split)
corpus_ids, query_ids = list(corpus), list(queries)

# Amostra aleatória dos pares do Corpus Original
# Incluindo primeiramente todos os documentos relevantes, ou seja, presentes em qrels
corpus_set = set()
for query_id in qrels:
    corpus_set.update(list(qrels[query_id].keys()))
corpus_new = {corpus_id: corpus[corpus_id] for corpus_id in corpus_set}

# Remove k documentos relevantes já vistos e amostras de documentos aleatoriamente
remaining_corpus = list(set(corpus_ids) - corpus_set)
sample = 1000 - len(corpus_set)

for corpus_id in random.sample(remaining_corpus, sample):
    corpus_new[corpus_id] = corpus[corpus_id]

model = BM25(index_name=index_name, hostname=hostname)
bm25 = EvaluateRetrieval(model)

# Recuperar resultados densos (o formato dos resultados é idêntico ao qrels)
results = bm25.retrieve(corpus, queries)

# Indexa as passagens no índice separadamente
bm25.retriever.index(corpus_new)


# Avaliação da IR usando NDCG@k, MAP@K, RECALL@K e PRECISION@K
logging.info("Retriever evaluation for k in: {}".format(bm25.k_values)) 
ndcg, _map, recall, precision = bm25.evaluate(qrels, results, bm25.k_values)

 
# Retrieval Exemplo
query_id, scores_dict = random.choice(list(results.items()))
logging.info("Query : %s\n" % queries[query_id])

scores = sorted(scores_dict.items(), key=lambda item: item[1], reverse=True)
for rank in range(10):
    doc_id = scores[rank][0]
    logging.info("Doc %d: %s [%s] - %s\n" % (rank+1, doc_id, corpus[doc_id].get("title"), corpus[doc_id].get("text")))

# Salvando os tempos do benchmark
time_taken_all = {}

for query_id in query_ids:
    query = queries[query_id]
    
    # Medida do tempo para recuperar os 10 principais documentos BM25 usando latência de consulta única
    start = datetime.datetime.now()
    results = bm25.retriever.es.lexical_search(text=query, top_hits=10) 
    end = datetime.datetime.now()
    
    # Medição do tempo gasto em milissegundos (ms)
    time_taken = (end - start)
    time_taken = time_taken.total_seconds() * 1000
    time_taken_all[query_id] = time_taken
    logging.info("{}: {} {:.2f}ms".format(query_id, query, time_taken))


time_taken = list(time_taken_all.values())
logging.info("Average time taken: {:.2f}ms".format(sum(time_taken)/len(time_taken_all)))

# Criando um DataFrame com os dados
data = {
    'ndcg': [ndcg[k] for k in ndcg],
    'map': [_map[k] for k in _map],
    'recall': [recall[k] for k in recall],
    'precision': [precision[k] for k in precision],
    'average_time': (sum(time_taken)/len(time_taken_all))
}

df = pd.DataFrame(data, index=['@{}'.format(k) for k in bm25.k_values])
# df = pd.DataFrame(data, index=False)

# Exibir o DataFrame
# print(df)

df.to_csv('./output/bm25_'+index_name+'_'+split+'.csv')
