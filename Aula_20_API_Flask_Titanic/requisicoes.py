"""
Aula 20 — Demonstração em sala: as requisições, uma a uma 🎬

Uso:  python requisicoes.py    (em OUTRO terminal, com o app.py já rodando)

Dica para a aula: deixe os dois terminais lado a lado. A cada Enter, um pedido
sai daqui e aparece uma linha nova no terminal do app.py, com o status code.
"""
import json

import requests

URL = "http://127.0.0.1:5000"

jack = {"pclass": 3, "sex": "male",   "age": 20, "sibsp": 0, "parch": 0, "fare": 7.75}
rose = {"pclass": 1, "sex": "female", "age": 17, "sibsp": 0, "parch": 1, "fare": 151.55}

# (descrição, método, rota, corpo JSON)
PEDIDOS = [
    ("A API está no ar?",                   "GET",  "/",           None),
    ("O 'cardápio': o que a API espera?",   "GET",  "/info",       None),
    ("Jack, 3ª classe 🃏",                  "POST", "/prever",     jack),
    ("Rose, 1ª classe 💎",                  "POST", "/prever",     rose),
    ("Rose com 'Female' (F maiúsculo)",     "POST", "/prever",     {**rose, "sex": "Female"}),
    ("Esqueceu a idade",                    "POST", "/prever",     {k: v for k, v in jack.items() if k != "age"}),
    ("Idade por extenso",                   "POST", "/prever",     {**jack, "age": "vinte"}),
    ("Sexo inválido",                       "POST", "/prever",     {**rose, "sex": "mulher"}),
    ("Uma rota que não existe",             "GET",  "/cozinha",    None),
]


def mostrar_json(dados):
    return json.dumps(dados, ensure_ascii=False)


def conferir_api():
    """Confere se quem responde na porta é mesmo a nossa API (e não outro programa)."""
    try:
        resposta = requests.get(f"{URL}/info", timeout=2)
    except requests.exceptions.ConnectionError:
        raise SystemExit("🔴 Não encontrei a API. Ela está rodando? "
                         "Abra outro terminal e rode: python app.py")
    try:
        info = resposta.json()
        return info["modelo"], info["acuracia_teste"]
    except (ValueError, KeyError):
        raise SystemExit(f"🔴 Algo respondeu em {URL}, mas não é a nossa API.\n"
                         "   Outro programa deve estar usando a porta 5000: feche-o "
                         "ou troque a porta no app.py e aqui.") from None


if __name__ == "__main__":
    modelo, acuracia = conferir_api()
    print(f"🟢 Conectado ao Oráculo ({modelo}, acurácia {acuracia:.1%})")

    for numero, (descricao, metodo, rota, corpo) in enumerate(PEDIDOS, start=1):
        input(f"\n⏎  Enter para o pedido {numero}/{len(PEDIDOS)}: {descricao}")

        print(f"  ➡️  {metodo} {URL}{rota}")
        if corpo is not None:
            print(f"      corpo: {mostrar_json(corpo)}")

        resposta = requests.request(metodo, f"{URL}{rota}", json=corpo, timeout=5)

        try:
            conteudo = mostrar_json(resposta.json())
        except ValueError:                           # a resposta não é JSON (ex.: página 404)
            conteudo = "(página de erro do Flask, sem JSON)"
        icone = "✅" if resposta.ok else "❌"
        print(f"  ⬅️  {icone} [{resposta.status_code}] {conteudo}")

    print("\n🏁 Fim da demonstração! Agora experimente o mini-chatbot: python cliente.py")
