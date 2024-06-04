import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

dataset = "train"
metricas = ['ndcg', 'map', 'recall', 'precision']

for metrica in metricas:
    # metrica = "NDCG"

    df_bm25 = pd.read_csv('./output/bm25_scifact_'+dataset+'.csv')
    df_sbert_cos = pd.read_csv('./output/sbert_cos_sim_'+dataset+'.csv')
    df_sbert_dot = pd.read_csv('./output/sbert_dot_'+dataset+'.csv')

    # Dados fornecidos
    labels = [metrica.upper()+df_bm25['Unnamed: 0'], metrica.upper()+'@3', metrica.upper()+'@5', metrica.upper()+'@10', metrica.upper()+'@100', metrica.upper()+'@1000']

    bm25 = df_bm25[metrica.lower()]
    sbert_cos = df_sbert_cos[metrica.lower()]
    sbert_dot = df_sbert_dot[metrica.lower()]

    # Configurações do gráfico
    x = np.arange(len(labels))  # Posições no eixo x
    width = 0.2  # Largura das barras

    fig, ax = plt.subplots(figsize=(12, 6))

    # Criação das barras
    rects1 = ax.bar(x - width, bm25, width, label='BM25')
    rects2 = ax.bar(x, sbert_cos, width, label='SBERT_COS')
    rects3 = ax.bar(x + width, sbert_dot, width, label='SBERT_DOT')

    # Adição de rótulos, título e legenda
    ax.set_ylabel(metrica.upper())
    ax.set_xlabel('')
    ax.set_title('Desempenho dos Algoritmos usando a métrica '+metrica.upper()+' do dataset '+dataset.upper())
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    # Adição de rótulos nas barras
    def autolabel(rects):
        """Adiciona rótulos nas barras."""
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height:.2f}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # Margem de espaço acima da barra
                        textcoords="offset points",
                        ha='center', va='bottom')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)

    # Ajuste do layout para evitar cortes nos rótulos
    fig.tight_layout()

    # Salvar e mostrar gráfico
    plt.savefig('./output/comparacao_algoritmos_'+metrica+'_'+dataset+'.png')
    plt.show()
