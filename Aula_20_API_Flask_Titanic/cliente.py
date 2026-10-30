"""
Aula 20 — Passo 3: o cliente — um mini-chatbot de terminal que consulta a API

Uso:  python cliente.py    (em OUTRO terminal, com o app.py já rodando)
"""
import requests

URL = "http://127.0.0.1:5000"


def consultar_oraculo(passageiro):
    """Envia os dados do passageiro para a API e devolve a resposta em dicionário."""
    resposta = requests.post(f"{URL}/prever", json=passageiro, timeout=5)
    if resposta.status_code != 200:
        print(f"⚠️  A API recusou o pedido ({resposta.status_code}): {resposta.json()['erro']}")
        return None
    return resposta.json()


def mostrar(nome, resultado):
    if resultado:
        print(f"  {nome:<6} → {resultado['mensagem']}  "
              f"(probabilidade: {resultado['probabilidade_sobrevivencia']:.0%})")


def perguntar(texto, tipo=str):
    while True:
        try:
            return tipo(input(f"  🤖 {texto} "))
        except ValueError:
            print("     Hmm, não entendi. Pode digitar só o número?")


if __name__ == "__main__":
    try:
        info = requests.get(f"{URL}/info", timeout=2).json()
    except requests.exceptions.ConnectionError:
        print("🔴 Não encontrei a API. Ela está rodando? Abra outro terminal e rode: python app.py")
        raise SystemExit(1)

    print(f"🟢 Conectado ao Oráculo ({info['modelo']}, acurácia {info['acuracia_teste']:.1%})\n")

    print("🎬 Os protagonistas do filme:")
    jack = {"pclass": 3, "sex": "male",   "age": 20, "sibsp": 0, "parch": 0, "fare": 7.75}
    rose = {"pclass": 1, "sex": "female", "age": 17, "sibsp": 0, "parch": 1, "fare": 151.55}
    mostrar("Jack", consultar_oraculo(jack))
    mostrar("Rose", consultar_oraculo(rose))

    print("\n🎟️  Agora é a sua vez de embarcar!")
    voce = {
        "pclass": perguntar("Em qual classe você viajaria? (1, 2 ou 3)", int),
        "sex":    perguntar("Sexo (male/female):"),
        "age":    perguntar("Quantos anos você tem?", float),
        "sibsp":  perguntar("Quantos irmãos/cônjuge viajariam com você?", int),
        "parch":  perguntar("Quantos pais/filhos viajariam com você?", int),
        "fare":   perguntar("Quanto pagaria na passagem? (1ª ~ 62, 2ª ~ 19, 3ª ~ 8)", float),
    }
    print()
    mostrar("Você", consultar_oraculo(voce))
