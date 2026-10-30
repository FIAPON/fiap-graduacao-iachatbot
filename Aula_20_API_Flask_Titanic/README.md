# Aula 20 — O Oráculo do Titanic como API 🚢

Versão "para levar para casa" da Aula 20: os mesmos códigos do notebook, separados em arquivos
para você rodar no seu computador, como em um projeto de verdade.

| Arquivo | Papel no restaurante 🍽️ |
|---------|--------------------------|
| `treinar_modelo.py` | A cozinha se prepara: treina o Random Forest e salva `modelo_titanic.pkl` |
| `app.py` | O garçom: a API Flask que recebe pedidos e devolve previsões |
| `cliente.py` | O cliente: um mini-chatbot de terminal que consulta a API |

## Como rodar

```bash
pip install -r requirements.txt

python treinar_modelo.py   # 1. gera o modelo_titanic.pkl (só precisa uma vez)
python app.py              # 2. TERMINAL 1: liga o servidor e deixa aberto
python cliente.py          # 3. TERMINAL 2: conversa com o Oráculo
```

Com o servidor ligado, você também pode abrir no navegador:

- http://127.0.0.1:5000/ — mensagem de boas-vindas
- http://127.0.0.1:5000/info — informações do modelo

E testar pelo terminal com `curl`:

```bash
curl -X POST http://127.0.0.1:5000/prever -H "Content-Type: application/json" \
     -d '{"pclass": 3, "sex": "male", "age": 20, "sibsp": 0, "parch": 0, "fare": 7.75}'
```

## Rotas da API

| Método | Rota | O que faz |
|--------|------|-----------|
| GET | `/` | Boas-vindas (serve para checar se a API está no ar) |
| GET | `/info` | Modelo usado, acurácia e campos esperados |
| POST | `/prever` | Recebe um passageiro em JSON e devolve a previsão |

## Problemas comuns

- **`ConnectionError` no cliente** → o `app.py` não está rodando. Ligue-o em outro terminal.
- **`FileNotFoundError: modelo_titanic.pkl`** → rode `python treinar_modelo.py` antes.
- **`Address already in use` (porta 5000 ocupada)** → já existe outro servidor aberto; feche-o.
  No macOS, a porta 5000 é usada pelo *AirPlay Receiver*: desative-o nas Configurações
  ou troque `port=5000` por `port=5001` no `app.py` e no `cliente.py`.
