import requests
import csv
import io
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Link do CSV da aba "Sorteio" publicada na web
URL_PLANILHA = "SUA_URL_DO_CSV_AQUI"

def pegar_nomes_google():
    try:
        response = requests.get(URL_PLANILHA)
        response.raise_for_status()
        content = response.content.decode('utf-8')
        reader = csv.reader(io.StringIO(content))
        
        # Pula o cabeçalho "Nome" e pega o resto
        nomes = [row[0].strip() for row in reader if row and row[0].strip() != "Nome"]
        return nomes
    except Exception as e:
        print(f"Erro ao acessar Google Sheets: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    nomes_inseridos = ""
    
    if request.method == 'POST':
        origem = request.form.get('origem')
        
        if origem == 'google':
            lista = pegar_nomes_google()
            nomes_inseridos = "; ".join(lista)
        else:
            nomes_inseridos = request.form.get('nomes', '')
            lista = [n.strip() for n in nomes_inseridos.split(';') if n.strip()]

        if lista:
            resultado = random.choice(lista)
            
    return render_template('index.html', resultado=resultado, nomes=nomes_inseridos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
