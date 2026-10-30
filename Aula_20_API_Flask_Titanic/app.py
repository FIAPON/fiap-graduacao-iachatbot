"""
Aula 20 — A API do Oráculo do Titanic 🚢

Antes de rodar:
  1. Rode o notebook da Aula 20 no Colab e baixe o arquivo modelo_titanic.pkl
  2. Coloque o modelo_titanic.pkl nesta mesma pasta, ao lado deste app.py
  3. pip install -r requirements.txt

Uso:  python app.py     (deixe este terminal aberto: o servidor fica esperando pedidos)
"""
import os
import pickle
import sys

import pandas as pd
import sklearn
from flask import Flask, jsonify, request

# ══ ✏️ ADAPTE AQUI para o seu trabalho ════════════════════════════════════════
ARQUIVO_MODELO = "modelo_titanic.pkl"

# Campos que o cliente precisa enviar (dados "crus", como o usuário conhece)
CAMPOS_OBRIGATORIOS = ["pclass", "sex", "age", "sibsp", "parch", "fare"]


def preparar_passageiro(dados):
    """Repete exatamente a mesma preparação feita no treino (Aula 03)."""
    faltando = [campo for campo in CAMPOS_OBRIGATORIOS if campo not in dados]
    if faltando:
        raise ValueError(f"Campos obrigatórios faltando: {faltando}")

    sexo = str(dados["sex"]).strip().lower()         # aceita "Female", "MALE"...
    if sexo not in ("male", "female"):               # ...e recusa "mulher"
        raise ValueError("O campo 'sex' precisa ser 'male' ou 'female'.")

    try:
        passageiro = {
            "pclass": int(dados["pclass"]),
            "sex_enc": 1 if sexo == "female" else 0,
            "age": float(dados["age"]),
            "tamanho_familia": int(dados["sibsp"]) + int(dados["parch"]) + 1,
            "fare": float(dados["fare"]),
        }
    except (ValueError, TypeError):
        raise ValueError("pclass, age, sibsp, parch e fare precisam ser números.") from None

    return pd.DataFrame([passageiro])[FEATURES]      # mesma ordem de colunas do treino


def prever_passageiro(dados):
    """Dados crus → previsão, já no formato da resposta da API."""
    X = preparar_passageiro(dados)
    sobreviveu = int(modelo.predict(X)[0])
    probabilidade = float(modelo.predict_proba(X)[0, 1])
    return {
        "sobreviveu": sobreviveu,
        "probabilidade_sobrevivencia": round(probabilidade, 4),
        "mensagem": "🛟 Conseguiu um lugar no bote!" if sobreviveu else "🧊 Não resistiu ao naufrágio...",
    }
# ══════════════════════════════════════════════════════════════════════════════


# ── 1. Carrega o modelo UMA VEZ, quando o servidor liga (não a cada pedido!) ──
caminho = os.path.join(os.path.dirname(os.path.abspath(__file__)), ARQUIVO_MODELO)
if not os.path.exists(caminho):
    sys.exit(f"🔴 Não encontrei '{ARQUIVO_MODELO}' nesta pasta.\n"
             "   Rode o notebook da Aula 20 no Colab, baixe o arquivo e coloque-o ao lado do app.py.")

try:
    with open(caminho, "rb") as arquivo:
        pacote = pickle.load(arquivo)
except Exception as erro:
    sys.exit(f"🔴 Não consegui abrir '{ARQUIVO_MODELO}': {erro}\n"
             "   Causa mais comum: versão do scikit-learn diferente da usada no Colab.\n"
             "   Instale a mesma versão mostrada no final do notebook: pip install scikit-learn==X.Y.Z")

modelo = pacote["modelo"]
FEATURES = pacote["features"]

if pacote.get("versao_sklearn") != sklearn.__version__:
    print(f"⚠️  Modelo treinado com scikit-learn {pacote.get('versao_sklearn')}, "
          f"mas aqui está instalado o {sklearn.__version__}.\n"
          f"   Se as previsões derem erro: pip install scikit-learn=={pacote.get('versao_sklearn')}")

app = Flask(__name__)


# ── 2. As rotas (o "cardápio" da API) ─────────────────────────────────────────
@app.route("/")
def home():
    return jsonify({"mensagem": "🚢 Bem-vindo ao Oráculo do Titanic! Use POST /prever para consultar."})


@app.route("/info")
def info():
    return jsonify({
        "modelo": type(modelo).__name__,
        "acuracia_teste": pacote["acuracia_teste"],
        "treinado_em": pacote["treinado_em"],
        "campos_esperados": CAMPOS_OBRIGATORIOS,
    })


@app.route("/prever", methods=["POST"])
def prever():
    dados = request.get_json(silent=True)
    if dados is None:
        return jsonify({"erro": "Envie os dados do passageiro em formato JSON."}), 400

    try:
        resultado = prever_passageiro(dados)
    except ValueError as erro:                       # pedido mal feito → culpa do cliente
        return jsonify({"erro": str(erro)}), 400

    return jsonify(resultado)


if __name__ == "__main__":
    print(f"🟢 Oráculo do Titanic no ar! Modelo: {type(modelo).__name__} "
          f"(acurácia {pacote['acuracia_teste']:.1%})")
    app.run(host="127.0.0.1", port=5000)
