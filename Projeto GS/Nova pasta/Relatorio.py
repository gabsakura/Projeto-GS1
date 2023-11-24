import reportlab
from reportlab.pdfgen import canvas 
from reportlab.lib.pagesizes import A4
import requests
import streamlit as sl
from datetime import date

dia = date.today()
xti= 40
cnv = canvas.Canvas(f'Relatorio_Da_Caminhada.pdf', pagesize=A4)
cnv .setTitle(f'Relatorio {dia}')
cnv.setLineWidth(1)
cnv.drawCentredString(280, 800,f'Relatório Caminhada')
z=0
y = 0
Ytitulo = 760

sl.title('Faça o download do relatório')


try:
  n=int(sl.text_input(f'Quantidade dos últimos resultados a serem exibidos:'))
except:
  n = 15

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
    print("The list returned by pegarValores(0) has less than two elements.")

dados = pegarValores(n)[0]


for aux in range(0, n):
  y = y+20
  z= z+20
  data_somente = dados['feeds'][aux]['created_at'][:10]
  dataBR = dados['feeds'][aux]['created_at']
  dia = dataBR[8:10]
  mes = dataBR[5:7]
  ano = dataBR[:4]
  if n ==1:
    cnv.drawString(30, 780, f'Feedback da sua caminhada!')
  else:
    cnv.drawString(30, 780, f'Esses são os {n} últimos valores pegos da sua jornada!')
  cnv.drawString(xti, Ytitulo, "Data:")
  cnv.drawString(xti+75, Ytitulo, " Calorias:")
  cnv.drawString(xti+75*2, Ytitulo, ' Distancia:')
  cnv.drawString(xti+75*3, Ytitulo, ' Passos:')
  cnv.drawString(xti+75*4, Ytitulo, ' Oxigenio:')
  cnv.drawString(xti+75*5, Ytitulo, ' Tempo:')
  cnv.drawString(xti+75*6, Ytitulo, ' Velocidade:')
  cnv.line(20, 745-z, 550,745 - z)  # Ponto de início (50, A4[1] - 50) e ponto final (A4[0] - 50, 50
  hora = str(int(dataBR[11:13])-1) + dataBR[13:19]
  Calorias = str(round(float(dados['feeds'][aux]['field4'])))
  Distancia = str(round(float(dados['feeds'][aux]['field3'])))
  Passos = str(round(float(dados['feeds'][aux]['field2'])))
  Coração = str(round(float(dados['feeds'][aux]['field1'])))
  O2 = str(round(float(dados['feeds'][aux]['field5'])))
  Tempo = str(round(float(dados['feeds'][aux]['field6'])))
  VelocidadeM = str(round(float(dados['feeds'][aux]['field7']), 2))
  cnv.drawString(30,750-y, data_somente)
  cnv.drawString(xti+80, 750- y, Calorias )
  cnv.drawString(xti+80*2, 750- y, Distancia )
  cnv.drawString(xti+80*3, 750- y, Passos)
  cnv.drawString(xti+80*4, 750- y, O2 )
  cnv.drawString(xti+80*5, 750- y, Tempo)
  cnv.drawString(xti+80*6, 750- y, VelocidadeM)
  print(Tempo)
  print(VelocidadeM)
  print(Calorias)
  print(Distancia)
  print(Passos)
  print(dataBR)
  # if aux == 36:
  # descobrir como fazer uma segunda pagina  ----->, a cada 36 "linhas"

cnv.showPage()
cnv.save()
with open(f"Relatorio_Da_Caminhada.pdf", "rb") as pdf_file:
    PDFbyte = pdf_file.read()
    if sl.download_button(
                          label='Baixe seu pdf aqui!!',
                          data=PDFbyte,
                          file_name=f'Relatorio_Da_Caminhada.pdf',
                          mime='text/pdf',):
      sl.text(f'Download feito em {dia} com sucesso!!')
