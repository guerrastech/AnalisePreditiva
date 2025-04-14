import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import pickle
import numpy as np
from sklearn.model_selection import train_test_split

# Carregar os dados
df = pd.read_csv('income_evaluation.csv', encoding='ISO-8859-1')

# Limpar espaços dos nomes e valores
df.columns = df.columns.str.strip()
df = df.applymap(lambda x: x.strip() if isinstance(x, str) else x)

# Substituir '?' por NaN e remover linhas com valores ausentes
df.replace('?', np.nan, inplace=True)
df.dropna(inplace=True)

# Substituir valores categóricos por números
df['income'] = df['income'].replace({"<=50K": 0, ">50K": 1})
df["sex"] = df["sex"].replace({"Male": 1, "Female": 2})

df["occupation"] = df["occupation"].replace({
    'Adm-clerical': 1, 'Exec-managerial': 2, 'Handlers-cleaners': 3,
    'Prof-specialty': 4, 'Other-service': 5, 'Sales': 6, 'Craft-repair': 7,
    'Transport-moving': 8, 'Farming-fishing': 9, 'Machine-op-inspct': 10,
    'Tech-support': 11, '?': 12, 'Protective-serv': 13, 'Armed-Forces': 14,
    'Priv-house-serv': 15
})

# Seleção de variáveis
X = df[['education-num', 'age', 'occupation', 'sex', 'capital-gain']]
y = df['income']

# Divisão treino/teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Treinamento
modelo = RandomForestClassifier()
modelo.fit(X_train, y_train)

# Salvar modelo
with open('modelo_preditivo.pkl', 'wb') as f:
    pickle.dump(modelo, f)

print("Modelo salvo com sucesso!")
