from beir import util, LoggingHandler
from beir.retrieval import models
from beir.datasets.data_loader import GenericDataLoader
from beir.retrieval.evaluation import EvaluateRetrieval
from beir.retrieval.search.dense import DenseRetrievalExactSearch as DRES
import logging
import pathlib, os
import random
import pandas as pd
import datetime


logging.basicConfig(format='%(asctime)s - %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.INFO,
                    handlers=[LoggingHandler()])

dataset = "scifact" #scifact


url = "https://public.ukp.informatik.tu-darmstadt.de/thakur/BEIR/datasets/{}.zip".format(dataset)
out_dir = os.path.join(pathlib.Path(__file__).parent.absolute(), "datasets")
data_path = util.download_and_unzip(url, out_dir)


# Forneçe o caminho de dados onde o dataset foi baixado, descompactado e carrega os dados
split = "test"
corpus, queries, qrels = GenericDataLoader(data_folder=data_path).load(split=split)
corpus_ids, query_ids = list(corpus), list(queries)


# Para o benchmarking usando modelos densos, pode pegar qualquer documento, pois não importa quais os documentos escolhidos
number_docs = 10000
reduced_corpus = [corpus[corpus_id] for corpus_id in corpus_ids[:number_docs]]


start = datetime.datetime.now()


# Recuperação densa usando Dense Passage Retriever (DPR)
# DPR implementa uma estratégia de duas torres, ou seja, codifica a consulta e o documento separadamente.
# O modelo DPR foi ajustado usando a função de produto escalar (dot)
# Carregando modelo DPR usando SentenceTransformers precisa fornecer um '[SEP]' para separar títulos e passagens em documentos
model = DRES(models.SentenceBERT((
    "facebook-dpr-question_encoder-multiset-base",
    "facebook-dpr-ctx_encoder-multiset-base",
    " [SEP] "), batch_size=256))


# A função de score deve ser (cos_sim) para similaridade de cosseno ou (dot) para produto escalar
score_function = "cos_sim"
retriever = EvaluateRetrieval(model, score_function=score_function)

# Recuperar resultados densos (o formato dos resultados é idêntico ao qrels)
results = retriever.retrieve(corpus, queries)


# Avaliação da IR usando NDCG@k, MAP@K, RECALL@K e PRECISION@K
logging.info("Retriever evaluation for k in: {}".format(retriever.k_values))
ndcg, _map, recall, precision = retriever.evaluate(qrels, results, retriever.k_values)


# Retrieval Exemplo
top_k = 10

query_id, ranking_scores = random.choice(list(results.items()))
scores_sorted = sorted(ranking_scores.items(), key=lambda item: item[1], reverse=True)
logging.info("Query : %s\n" % queries[query_id])

# for rank in range(top_k):
#     doc_id = scores_sorted[rank][0]
#     # Format: Rank x: ID [Title] Body
#     logging.info("Rank %d: %s [%s] - %s\n" % (rank+1, doc_id, corpus[doc_id].get("title"), corpus[doc_id].get("text")))

    
end = datetime.datetime.now()
time_taken = (end - start)
time_taken = time_taken.total_seconds() * 1000
logging.info("Average time taken: {:.2f}ms".format((time_taken)/len(queries)))
# logging.info("{:.2f}ms".format(time_taken))


# Criando um DataFrame com os dados
data = {
    'ndcg': [ndcg[k] for k in ndcg],
    'map': [_map[k] for k in _map],
    'recall': [recall[k] for k in recall],
    'precision': [precision[k] for k in precision],
    'average_time': ((time_taken)/len(queries))
}

df = pd.DataFrame(data, index=['@{}'.format(k) for k in retriever.k_values])

# Exibi o DataFrame
# print(df)

df.to_csv('./output/sbert_'+score_function+'_'+split+'.csv')