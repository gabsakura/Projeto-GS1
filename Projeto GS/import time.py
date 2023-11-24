import time
from pushbullet import Pushbullet

# Substitua 'o seu token' pelo seu token de acesso da API Pushbullet
pb = Pushbullet('o.rqGKGsNPLx8hbeV8OYZt5genPGqqBHut')

def enviar_notificacao():
    push = pb.push_note("Lembrete para beber água", "Por favor, beba água agora!")

while True:
    enviar_notificacao()
    # Aguarda duas horas (7200 segundos) antes de enviar a próxima notificação
    time.sleep(7200)
