import pandas as pd
import numpy as np
import os
import json
import matplotlib.pyplot as plt
import seaborn as sns

pd.set_option("display.max_rows", 20, "display.max_columns", 60)

def read_file(file_name):
    return pd.read_csv(file_name)

dataset = read_file("df.csv")
#print(dataset.head())

def read_types(file_name):
    dtypes = {}
    with open(file_name, mode='r') as file:
        dtypes = json.load(file)

    for key in dtypes.keys():
        if dtypes[key] == 'category':
            dtypes[key] = pd.CategoricalDtype()
        elif dtypes[key] == 'string':
            dtypes[key] = pd.StringDtype()
        else:
            dtypes[key] = np.dtype(dtypes[key])
    return dtypes
print(read_types("dtypes.json"))


need_dtypes = read_types("dtypes.json")

dataset = pd.read_csv("df.csv", usecols=lambda x: x in need_dtypes.keys(),
            dtype=need_dtypes)

dataset.info(memory_usage='deep')

plt.figure(figsize=(8, 6))
plt.plot(dataset.groupby(["day_of_week"])['length_minutes'].sum().values, marker='o', linestyle='-')
plt.title('Линейный график')
plt.grid(True)
plt.savefig('linear_plot.png')


plt.figure(figsize=(10, 6))
sns.barplot(x='day_of_week', y='day_of_week', data=dataset)
plt.title('Столбчатая диаграмма')
plt.xlabel('day_of_week')
plt.ylabel('day_of_week')
plt.tight_layout()
plt.savefig('bar_chart.png')


plt.figure(figsize=(8, 8))
data_for_pie = dataset['number_of_game'].value_counts()
plt.pie(data_for_pie, labels=data_for_pie.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')
plt.title('Круговая диаграмма')
plt.tight_layout()
plt.savefig('pie_chart.png')


numeric_data = dataset.select_dtypes(include=['float32', 'int32'])
corr_matrix = numeric_data.corr()
plt.figure(figsize=(10, 8))
sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt='.2f')
plt.title('Корреляционная матрица')
plt.tight_layout()
plt.savefig('correlation.png')

plt.figure(figsize=(8, 6))
sns.boxplot(x='number_of_game', y='h_errors', data=dataset)
plt.title('Boxplot')
plt.xlabel('Column1')
plt.ylabel('Column2')