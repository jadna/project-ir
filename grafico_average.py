import matplotlib.pyplot as plt

# Dados
methods = ['BM25', 'SBERT_COS', 'SBERT_DOT']
average_times_test = [16.33152, 348.62141, 300.19057]

# Dados
methods = ['BM25', 'SBERT_COS', 'SBERT_DOT']
average_times_train = [15.45795797280595, 127.48401236093945, 124.19014462299134]

# Criar o gráfico de barras
plt.bar(methods, average_times_train, color='orange')

# Adicionar os valores acima das barras
for i in range(len(methods)):
    plt.text(methods[i], average_times_train[i] + 1, str(round(average_times_train[i], 2)), ha='center')

# Adicionar título e rótulos
plt.title('Média de Tempo por Método com o dataset TRAIN')
plt.xlabel('')
plt.ylabel('Tempo Médio (ms)')

# Exibir o gráfico
plt.savefig('./output/average_time_train.png')
plt.show()



