from threading import Thread
import paho.mqtt.client as mqtt
import ssl
import json

def salva_estado(estado):
    with open("estado.json", "w") as arq:
        json.dump(estado, arq, indent=4)


def estado_atual():
    try:
        with open("estado.json", "r") as arq:
            settings = json.load(arq)
        return settings
    except (json.JSONDecodeError, FileNotFoundError):
        return None


def config_atual():
    try:
        with open("settings.json", "r") as arq:
            settings = json.load(arq)
        return settings
    except (json.JSONDecodeError, FileNotFoundError):
        return None

cliente = None

def on_connect(client, userdata, flags, rc):
    print(rc)
    if rc == 0:
        print("Conectado")
        client.subscribe("/home/#")
    else:
        print(f"Erro ao se conectar, código: {rc}")


def on_subscribe(client, userdata, mid, granted_qos):
    print('Cliente inscrito')
    print(f'QOS: {granted_qos}')


def on_message(client, userdata, message):
    print('Mensagem recebida')
    estado = estado_atual()
    mensagem = message.payload.decode()
    topico = message.topic
    print(f'Tópico: {message.topic}, Mensagem: {mensagem}')
    if topico=="/home/janela":
        novo = "fechada" if mensagem == "fechada" else "aberta"
        if estado is not None:
            estado[2]["janela"] = novo
            salva_estado(estado)
            print(f"Janela {novo}")
    elif "Luz" in topico:
        luz = topico.split("/")[-1]
        print(luz)
        novo = "apagada" if mensagem == "apagada" else "acesa"
        if estado is not None:
            estado[0]["luzes"][0][luz] = novo
            salva_estado(estado)
            print(f"{luz} {novo}")
    elif topico=="/home/temperatura":
        if estado is not None:
            mensagem = float(mensagem)
            temp_atual = estado[1]["temperatura"]
            acao = "aumentada" if temp_atual < mensagem else "diminuída"
            estado[1]["temperatura"] = mensagem
            salva_estado(estado)
            print(f"Temperatura {acao} para {mensagem}")
    elif topico=="/home/modo":
        novo = "auto" if mensagem == "auto" else "manual"
        if estado is not None:
            estado[3]["modo"] = novo
            salva_estado(estado)
            print(f"Modo {novo}")

def on_disconnect(client, userdata, rc):
    if rc != 0:
        print(f"Desconectado, retorno: {rc}")
        client.reconnect()


def on_publish(client, userdata, mid):
    print(f'Mensagem publicada')


def setup_cliente():
    cliente = mqtt.Client(client_id="1234", protocol=mqtt.MQTTv311)
    cliente.on_connect = on_connect
    cliente.on_subscribe = on_subscribe
    cliente.on_message = on_message
    cliente.on_disconnect = on_disconnect
    cliente.on_publish = on_publish
    cliente.tls_set(tls_version=ssl.PROTOCOL_TLS)
    cliente.tls_insecure_set(False)
    #cliente.username_pw_set(username="projetomicro", password="projetoMicro1")
    print("Tentando conectar")
    #cliente.connect("6e487c2bb3b0422392bae2d3405c8e5f.s1.eu.hivemq.cloud", port=8883, keepalive=60)
    cliente.connect("broker.hivemq.com",port=8883, keepalive=60)
    return cliente


def publish_message(client, topic, payload):
    if client:
        result = client.publish(topic, payload)
        print(client)
        if result.rc == mqtt.MQTT_ERR_SUCCESS:
            print(f"Mensagem '{payload}' no tópico '{topic}'")
        else:
            print(f"Falha ao publicar a mensagem '{payload}' no tópico '{topic}', erro: {result.rc}")
    else:
        print("Cliente MQTT não está conectado")


def disconnect_cliente():
    global cliente
    if cliente:
        cliente.disconnect()
        cliente.loop_stop()
        cliente = None
        print("Cliente desconectado")
    else:
        print("Cliente não conectado")


def load_settings():
    try:
        with open("mqtt/settings.json", "r") as file:
            settings = json.load(file)
        return settings
    except (FileNotFoundError, json.JSONDecodeError):
        return None
