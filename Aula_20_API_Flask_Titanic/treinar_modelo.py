"""
Aula 20 — Passo 1: treina o Random Forest (Aula 09) e salva em modelo_titanic.pkl

Uso:  python treinar_modelo.py
"""
import os
import pickle
import time

import seaborn as sns
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

# ── Carregando e preparando o Titanic (mesma limpeza das aulas anteriores) ────
df = sns.load_dataset("titanic").copy()

df["age"]      = df["age"].fillna(df["age"].median())
df["embarked"] = df["embarked"].fillna(df["embarked"].mode()[0])
df = df.drop(columns=["deck"]).drop_duplicates().reset_index(drop=True)

df["tamanho_familia"] = df["sibsp"] + df["parch"] + 1
df["sex_enc"]         = (df["sex"] == "female").astype(int)

# As mesmas 5 features usadas desde a Aula 05
FEATURES = ["pclass", "sex_enc", "age", "tamanho_familia", "fare"]

X = df[FEATURES].copy()
y = df["survived"].copy()

X_treino, X_teste, y_treino, y_teste = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y)

# ── Treinando o campeão da Aula 09 ────────────────────────────────────────────
floresta = RandomForestClassifier(n_estimators=200, max_depth=5,
                                  min_samples_leaf=5, random_state=42)
floresta.fit(X_treino, y_treino)
acuracia = accuracy_score(y_teste, floresta.predict(X_teste))

# ── Empacotando e salvando ────────────────────────────────────────────────────
pacote = {
    "modelo": floresta,
    "features": FEATURES,          # a ORDEM das colunas importa!
    "acuracia_teste": round(acuracia, 4),
    "treinado_em": time.strftime("%Y-%m-%d %H:%M"),
}

caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), "modelo_titanic.pkl")
with open(caminho, "wb") as arquivo:
    pickle.dump(pacote, arquivo)

print(f"🌲 Random Forest treinado — acurácia no teste: {acuracia:.1%}")
print(f"💾 Modelo salvo em: {caminho}")
print("Próximo passo: python app.py")
