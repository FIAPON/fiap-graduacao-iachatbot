"""
Aula 20 — O cliente: um mini-chatbot de terminal que consulta a API 🤖

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
    print(f"🟢 Conectado ao Oráculo ({modelo}, acurácia {acuracia:.1%})\n")

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
