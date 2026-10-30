# Aula 20 — O Oráculo do Titanic como API 🚢

A Aula 20 tem **duas etapas**:

| Etapa | Onde | O que acontece |
|-------|------|----------------|
| **1. Treinar e exportar** | 📓 [Notebook no Colab](https://colab.research.google.com/github/FIAPON/fiap-graduacao-iachatbot/blob/main/Aula_20_Pratica_API_Flask_Titanic.ipynb) | Treina o Random Forest e baixa o `modelo_titanic.pkl` |
| **2. Servir o modelo** | 💻 Esta pasta, no seu computador | A API Flask carrega o `.pkl` e responde às requisições |

| Arquivo | Papel no restaurante 🍽️ |
|---------|--------------------------|
| `modelo_titanic.pkl` | A receita pronta: vem do notebook (não está no GitHub — você gera) |
| `app.py` | O garçom: a API Flask que recebe pedidos e devolve previsões |
| `requisicoes.py` | Demonstração: dispara os pedidos um a um (ótimo para a aula) |
| `cliente.py` | O cliente: um mini-chatbot de terminal que consulta a API |

## Passo a passo

**1. No Colab:** rode o notebook até o fim. A última parte baixa o `modelo_titanic.pkl`
e mostra a versão do scikit-learn usada.

**2. No seu computador:** baixe esta pasta (ou clone o repositório) e coloque o
`modelo_titanic.pkl` **dentro dela**, ao lado do `app.py`.

**3. Instale as bibliotecas** — use a **mesma versão do scikit-learn** mostrada no notebook:

```bash
pip install -r requirements.txt
pip install scikit-learn==X.Y.Z    # troque pela versão que o notebook mostrou
```

**4. Ligue a API** — terminal 1 (deixe aberto):

```bash
python app.py
```

**5. Faça as requisições** — terminal 2:

```bash
python requisicoes.py    # demonstração: um pedido a cada Enter
python cliente.py        # mini-chatbot: pergunta seus dados e consulta o Oráculo
```

## 🎬 Para mostrar em sala

Deixe os **dois terminais lado a lado**. A cada Enter no `requisicoes.py`, o pedido sai
de um lado e aparece uma linha nova no terminal do `app.py`, com o método, a rota e o status:

```
127.0.0.1 - - [30/Oct/2026 14:20:01] "POST /prever HTTP/1.1" 200 -
127.0.0.1 - - [30/Oct/2026 14:20:09] "POST /prever HTTP/1.1" 400 -
127.0.0.1 - - [30/Oct/2026 14:20:15] "GET /cozinha HTTP/1.1" 404 -
```

Com o servidor ligado, as rotas GET também abrem direto no **navegador**:

- http://127.0.0.1:5000/ — boas-vindas
- http://127.0.0.1:5000/info — informações do modelo

E dá para fazer um POST "na mão", sem Python:

```powershell
# Windows (PowerShell)
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:5000/prever -ContentType "application/json" `
  -Body '{"pclass": 3, "sex": "male", "age": 20, "sibsp": 0, "parch": 0, "fare": 7.75}'
```

```bash
# macOS / Linux
curl -X POST http://127.0.0.1:5000/prever -H "Content-Type: application/json" \
     -d '{"pclass": 3, "sex": "male", "age": 20, "sibsp": 0, "parch": 0, "fare": 7.75}'
```

## Rotas da API

| Método | Rota | O que faz |
|--------|------|-----------|
| GET | `/` | Boas-vindas (serve para checar se a API está no ar) |
| GET | `/info` | Modelo usado, acurácia e campos esperados |
| POST | `/prever` | Recebe um passageiro em JSON e devolve a previsão |

## 🛠️ Adaptando para o seu trabalho

O `app.py` foi escrito para ser reaproveitado. Para servir o **seu** modelo:

1. **No seu notebook**, salve um pacote com o modelo e a lista de features, igual à Parte 2
   do notebook da aula (e o scaler, se o seu modelo precisar de normalização!).
2. **No `app.py`**, mexa só no bloco `✏️ ADAPTE AQUI`:
   - `ARQUIVO_MODELO` → o nome do seu `.pkl`
   - `CAMPOS_OBRIGATORIOS` → os campos que o cliente vai enviar
   - `preparar_passageiro()` → a **mesma preparação** que você fez no treino
   - `prever_passageiro()` → o formato da resposta (mensagens, probabilidade...)
3. **No `requisicoes.py`** (ou `cliente.py`), troque os exemplos pelos dados do seu problema.

O resto do `app.py` (carregar o modelo, rotas, tratamento de erros) continua igual.

## Problemas comuns

- **`ConnectionError` no `requisicoes.py`/`cliente.py`** → o `app.py` não está rodando.
  Ligue-o em outro terminal.
- **`Não encontrei 'modelo_titanic.pkl'`** → baixe o arquivo pelo notebook e coloque-o nesta pasta.
- **Erro ou aviso de versão ao abrir o `.pkl`** → instale a mesma versão do scikit-learn
  do Colab: `pip install scikit-learn==X.Y.Z`.
- **"Algo respondeu em http://127.0.0.1:5000, mas não é a nossa API"** → outro programa já usa
  a porta 5000. No Windows o Flask liga mesmo assim, sem avisar, e os pedidos vão para o
  programa errado. Feche o outro programa ou troque a porta (veja abaixo).
- **`Address already in use` (porta 5000 ocupada)** → já existe outro servidor aberto; feche-o.
  No macOS, a porta 5000 é usada pelo *AirPlay Receiver*: desative-o nas Configurações
  ou troque `5000` por `5001` no `app.py`, no `requisicoes.py` e no `cliente.py`.
