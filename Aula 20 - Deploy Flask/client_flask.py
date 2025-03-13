import requests
import json

def make_prediction(data):
    url = 'http://127.0.0.1:5000/predict'
    headers = {'Content-type': 'application/json'}
    
    # Enviar a solicitação POST com os dados da nova amostra
    response = requests.post(url, data=json.dumps(data), headers=headers)
    
    # Verificar se a solicitação foi bem-sucedida
    if response.status_code == 200:
        result = response.json()
        prediction = result['prediction']
        print(f"Previsão para a nova amostra: {prediction}")
    else:
        print("Erro ao fazer a previsão.")

if __name__ == '__main__':
    # Dados da nova amostra
    nova_amostra = {
        'sepal length (cm)': 6.7,
        'sepal width (cm)': 3.0,
        'petal length (cm)': 5.4,
        'petal width (cm)': 2.2
    }
    # Fazer a previsão usando o cliente
    make_prediction(nova_amostra)
