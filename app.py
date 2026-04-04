import requests
import csv
import io
import random
from flask import Flask, render_template, request

app = Flask(__name__)

# Link do CSV da aba "Sorteio" publicada na web
URL_PLANILHA = "https://docs.google.com/spreadsheets/d/e/2PACX-1vQblQOdI0C7djSivXnkd4Y-zz9LhqdMCLdoPCp7uZtku_VVIOcKE7FvFTi9PDVENg7pIwksYhnTBpCH/pub?gid=1156694142&single=true&output=csv"

def pegar_nomes_google(modalidade_alvo):
    try:
        response = requests.get(URL_PLANILHA)
        response.raise_for_status()
        content = response.content.decode('utf-8')
        reader = csv.reader(io.StringIO(content))
        
        # Pula a primeira linha (cabeçalho)
        next(reader, None)
        
        nomes_filtrados = []
        for row in reader:
            if len(row) >= 2:
                nome = row[0].strip()
                modalidade = row[1].strip()
                
                # O filtro agora compara com "Remoto" ou "Presencial"
                if modalidade == modalidade_alvo:
                    nomes_filtrados.append(nome)
                    
        return nomes_filtrados
    except Exception as e:
        print(f"Erro ao acessar Google Sheets: {e}")
        return []

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    nomes_exibidos = ""
    
    if request.method == 'POST':
        origem = request.form.get('origem')
        
        if origem in ['Presencial', 'Remoto']:
            lista = pegar_nomes_google(origem)
            nomes_exibidos = "; ".join(lista)
        else:
            # Sorteio Manual
            nomes_exibidos = request.form.get('nomes', '')
            lista = [n.strip() for n in nomes_exibidos.split(';') if n.strip()]

        if lista:
            resultado = random.choice(lista)
            
    return render_template('index.html', resultado=resultado, nomes=nomes_exibidos)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
