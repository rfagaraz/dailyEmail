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

# Componente de horóscopo que será concatenado na mensagem
def getHoroscopo(signo):
    url = 'http://babi.hefesto.io/signo/' + signo + '/dia'
    pedidoHoroscopo = requests.get(url)
    json_pedidoHoroscopo = json.loads(pedidoHoroscopo.text)
    horoscopo = json_pedidoHoroscopo['texto']
    print('Horoscopo Carregado!')
    return horoscopo

# Componente de previsão da temperatura que será concatenado na mensagem
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

# Função responsavel pelo envio da mensagem, identificação do servidor, etc...
# Em casos de customização não esqueça de alterar os dados abaixo
def sendEmail (msg, fulanoMail):
    message = MIMEMultipart()
    message['From'] = 'dailynewsdbmgpbr@gmail.com' # E-mail de envio
    message['To'] = fulanoMail 
    message['Subject'] = 'Daily News DBM GPBR' # Subject do email
    message['Body'] = msg
    smtpObj = smtplib.SMTP('smtp.gmail.com', 587) # SMTP padrão do gmail, caso use algum outro e-mail, altere os parametros.
    type(smtpObj)
    smtpObj.ehlo()
    smtpObj.starttls()
    smtpObj.login('YOUR-EMAIL', 'YOUR-PASSWORD') #Informações de login e senha do e-mail
    smtpObj.sendmail(message['From'], message['To'], message['Body'])
    print('E-mail enviado!')



# Functions para obter informações do envio atráves do "DataBase"
def getSigno (i):
    signo = dbsigno[i]
    return signo

def getFulano(i):
    fulano = dbnome[i]
    return fulano

def getFulanoMail(i):
    fulanoMail = dbmail[i]
    return fulanoMail


# Variáveis simulam um database para envio de cada e-mail
dbnome = ['John Doe', 'Jackin']
dbsigno = ['peixes', 'touro']
dbmail = ['example@gmail.com', 'freezer@gmail.com']
          

    
    
# Para manter o script o mais simples possivel, em um unico arquivo, você pode usar o campo abaixo para gerar um teste unitário ao seu
# e-mail pessoal, confirmando as construções da mensagem.
'''
##teste unitário####################
dbnome = []
dbsigno = []
dbmail = []
####################################
'''


# Run script
# previsao é uma constante nos e-mails, por tanto apenas uma chamada para agilizar a execução          
previsao = getWeather()
# Loop de execução envia um e-mail para cada registro nos arrays do "DataBase"
for i in range(len(dbnome)):
    sendEmail(generateMsg(getHoroscopo(getSigno(i)), getFulano(i), previsao), getFulanoMail(i))

print('Finalizado!')
