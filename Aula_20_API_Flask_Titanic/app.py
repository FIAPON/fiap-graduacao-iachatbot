"""
Aula 20 — Passo 2: a API do Oráculo do Titanic (versão final, com a Missão 5 resolvida)

Uso:  python app.py        (deixe este terminal aberto — o servidor fica esperando pedidos)
"""
import os
import pickle

import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)

# ── 1. Carrega o modelo UMA VEZ, quando o servidor liga (não a cada pedido!) ──
PASTA = os.path.dirname(os.path.abspath(__file__))
with open(os.path.join(PASTA, "modelo_titanic.pkl"), "rb") as arquivo:
    pacote = pickle.load(arquivo)

modelo = pacote["modelo"]
FEATURES = pacote["features"]

# Campos que o cliente precisa enviar (dados "crus", como o usuário conhece)
CAMPOS_OBRIGATORIOS = ["pclass", "sex", "age", "sibsp", "parch", "fare"]


def preparar_passageiro(dados):
    """Repete na API exatamente a mesma preparação feita no treino."""
    passageiro = {
        "pclass": int(dados["pclass"]),
        "sex_enc": 1 if dados["sex"] == "female" else 0,
        "age": float(dados["age"]),
        "tamanho_familia": int(dados["sibsp"]) + int(dados["parch"]) + 1,
        "fare": float(dados["fare"]),
    }
    return pd.DataFrame([passageiro])[FEATURES]   # mesma ordem de colunas do treino


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

    # ── 2. Validação: o pedido veio completo e correto? ──
    if dados is None:
        return jsonify({"erro": "Envie os dados do passageiro em formato JSON."}), 400

    faltando = [campo for campo in CAMPOS_OBRIGATORIOS if campo not in dados]
    if faltando:
        return jsonify({"erro": f"Campos obrigatórios faltando: {faltando}"}), 400

    # Missão 5: aceita "Female"/"MALE" e recusa valores inválidos como "mulher"
    dados["sex"] = str(dados["sex"]).strip().lower()
    if dados["sex"] not in ("male", "female"):
        return jsonify({"erro": "O campo 'sex' precisa ser 'male' ou 'female'."}), 400

    try:
        X = preparar_passageiro(dados)
    except (ValueError, TypeError):
        return jsonify({"erro": "pclass, age, sibsp, parch e fare precisam ser números."}), 400

    # ── 3. Previsão ──
    sobreviveu = int(modelo.predict(X)[0])
    probabilidade = float(modelo.predict_proba(X)[0, 1])

    return jsonify({
        "sobreviveu": sobreviveu,
        "probabilidade_sobrevivencia": round(probabilidade, 4),
        "mensagem": "🛟 Conseguiu um lugar no bote!" if sobreviveu else "🧊 Não resistiu ao naufrágio...",
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000)
