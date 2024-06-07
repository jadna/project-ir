import matplotlib.pyplot as plt

# Dados
methods = ['BM25', 'SBERT_COS', 'SBERT_DOT']
average_times = [16.33152, 348.62141, 300.19057]


# Criar o gráfico de barras
plt.bar(methods, average_times, color='orange')

# Adicionar os valores acima das barras
for i in range(len(methods)):
    plt.text(methods[i], average_times[i] + 1, str(round(average_times[i], 2)), ha='center')

# Adicionar título e rótulos
plt.title('Média de Tempo por Método')
plt.xlabel('')
plt.ylabel('Tempo Médio (ms)')

# Exibir o gráfico
plt.savefig('./output/average_time.png')
plt.show()



