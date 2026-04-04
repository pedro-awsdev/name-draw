from flask import Flask, render_template, request
import random

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    resultado = None
    nomes_inseridos = ""
    
    if request.method == 'POST':
        nomes_inseridos = request.form.get('nomes', '')
        lista = [n.strip() for n in nomes_inseridos.split(';') if n.strip()]
        if lista:
            resultado = random.choice(lista)
            
    return render_template('index.html', resultado=resultado, nomes=nomes_inseridos)

if __name__ == '__main__':
    # Rodar na porta 80 exige sudo, mas facilita o acesso pelo DNS da AWS
    app.run(host='0.0.0.0', port=80)