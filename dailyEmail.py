import smtplib
import json
import requests
from email.mime.multipart import MIMEMultipart

# Função para concatenar as informações e compor o Body da mensagem
def generateMsg (horoscopo, fulano, previsao):
    msg = 'Subject: Daily News DBM GPBR\n\nBom dia,\n' + fulano + ', comece bem o dia com algumas informações.\n' + '\nAcompanhe as influências diárias do seu signo:\n\n'
    msg = msg + horoscopo + '\n\n'
    msg = msg + previsao
    msg = msg + '\nNão se esqueça de beber água.\nPowered by DBM-GPBR. Recuse imitações.'
    msg = msg.encode("utf-8", errors="ignore")
    print('Mensagem Concatenada!')
    return msg

# Componente da mensagem em generateMsg
def getHoroscopo(signo):
    #get horoscopo do dia using date
    url = 'http://babi.hefesto.io/signo/' + signo + '/dia'
    pedidoHoroscopo = requests.get(url)
    json_pedidoHoroscopo = json.loads(pedidoHoroscopo.text)
    horoscopo = json_pedidoHoroscopo['texto']
    print('Horoscopo Carregado!')
    return horoscopo

def getWeather():
    def toCelsiusString(temp):
        temp = str(int(temp - 273.15)) + 'º'
        return temp

    json_weather = requests.get(
        'http://api.openweathermap.org/data/2.5/weather?id=3448439&appid=5033e78def0a6db803cdd70fc5753c24')
    raw_weather = json.loads(json_weather.text)
    temp_min = raw_weather['main']['temp_min']
    temp_max = raw_weather['main']['temp_max']

    temp_min = toCelsiusString(temp_min)
    temp_max = toCelsiusString(temp_max)

    temp_min = 'Temperatura mínima: ' + temp_min
    temp_max = 'Temperatura máxima: ' + temp_max

    previsao = 'Previsão de temperatura para a cidade de São Paulo:\n' + temp_min + '\n' + temp_max + '\n'

    return previsao

# Módulo de envio da mensagem, identificação do servidor, etc...
def sendEmail (msg, fulanoMail):
    message = MIMEMultipart()
    message['From'] = 'dailynewsdbmgpbr@gmail.com'
    message['To'] = fulanoMail
    message['Subject'] = 'Daily News DBM GPBR'
    message['Body'] = msg
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587)
    type(smtpObj)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('dailynewsdbmgpbr@gmail.com', 'daily153!')
    smtpObj.sendmail(message['From'], message['To'], message['Body'])
    print('E-mail enviado!')

#def getCotation():


# Functions para obter informações do envio
def getSigno (i):
    signo = dbsigno[i]
    return signo

def getFulano(i):
    fulano = dbnome[i]
    return fulano

def getFulanoMail(i):
    fulanoMail = dbmail[i]
    return fulanoMail


dbnome = ['Marieli', 'Vagner Dias dos Santos', 'Flávia', 'Shindi', 'Roberta', 'Rafael', 'Eliana', 'Danilo Alves', 'Marcella', 'Renato Fagaraz', 'Isadora']
dbsigno = ['peixes', 'libra', 'virgem', 'cancer', 'aries', 'aries', 'aries', 'touro', 'touro', 'cancer', 'cancer']
dbmail = ['mari.dgm@hotmail.com', 'vsantos@greenpeace.org', 'flaviasouza1144@gmail.com', 'amiashir@greenpeace.org', 'roberta.ita@greenpeace.org', 'rafael.ferraz@greenpeace.org', 'eliana.goncalves@greenpeace.org', 'danilo.alves@greenpeace.org', 'marcella.ferreira@greenpeace.org', 'rfagaraz@greenpeace.org', 'isadora.nascimento@greenpeace.org']
'''
##teste unitário####################
dbnome = ['Mariellen']
dbsigno = ['peixes']
dbmail = ['mari.dgm@hotmail.com']
####################################
'''


# Run script

previsao = getWeather()


for i in range(len(dbnome)):
    sendEmail(generateMsg(getHoroscopo(getSigno(i)), getFulano(i), previsao), getFulanoMail(i))

print('Finalizado!')