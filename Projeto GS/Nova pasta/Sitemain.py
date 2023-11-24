import requests
import streamlit as st
import pandas as pd

try:
  n=int(st.text_input(f'Quantidade dos últimos resultados a serem exibidos:'))
except:
  n = 1

def pegarValores(n):
  urlDados = f'https://api.thingspeak.com/channels/2351899/feeds.json?api_key=EML880RS0PWF585C&results=2{n}'
  respostaDados = requests.get(urlDados)
  
  if respostaDados.status_code == 200:
    return [respostaDados.json()]
  else:
    print('Erro na requisição')
    return {}

valores = pegarValores(0)
if len(valores) > 1:
    max = valores[1]['channel']['last_entry_id']
else:
    print("Deu ruim")

dados = pegarValores(n)[0]

st.title('Valores da ultima corrida')

st.markdown(f'''<h6 style ="height: 0rem; color: #808080; ">Digite um número de 1 a {max}</h6>
                  <h6 style ="height: 0rem; color: #808080; ">Exibindo o ultimo resultado mais recente</h6>''', unsafe_allow_html=True)

valores_passos = []
for aux in range(0, n):
  try:
    Calorias = str(dados['feeds'][aux]['field4'])
    Distancia = str(dados['feeds'][aux]['field3'])
    Passos = str(dados['feeds'][aux]['field2'])
    Coração = str(dados['feeds'][aux]['field1'])
    O2 = str(dados['feeds'][aux]['field5'])
    Velocidade = str(dados['feeds'][aux]['field7'])
    tempo = str(dados['feeds'][aux]['field6'])
    valores_passos.append([Calorias, Distancia, Passos, Coração, O2,Velocidade,tempo])
  except:
    valores_passos.append([0, 0, 0, 0])

# Criando um DataFrame com os valores
df = pd.DataFrame(valores_passos, columns=['Calorias', 'Distância', 'Passos','Coração','O2','tempo','Velocidade'])

# Exibindo a tabela
st.table(df)