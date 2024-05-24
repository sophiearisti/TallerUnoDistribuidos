from typing import TypedDict

PROXY_PORT = 5558
SENSOR_PORT = 5001
CLOUD_PORT = 5001
ASPERSOR_PORT = 5001
PROXY_BACKUP_PORT = 5001
SC_PROXY_PORT = 5557
SC_EDGE_PORT = 5007
SC_CLOUD_PORT = 5007
BROKER_PUB_PORT = 5002
BROKER_SUB_PORT = 5003

IP_PROXY = "192.168.193.126"
IP_PROXY_BACKUP = ""
IP_CLOUD = ""
IP_SC_PROXY = ""
IP_SC_EDGE = ""
IP_SC_CLOUD = ""
IP_ASPERSOR = ""
IP_BROKER = "192.168.193.148"

CANT_SENSORES = 10

SENSOR_HUMO = "humo"
SENSOR_HUMEDAD = "humedad"
SENSOR_TEMPERATURA = "temperatura"

ARCHIVO_HUMO = "files/humo.txt"
ARCHIVO_HUMEDAD = "files/humedad.txt"
ARCHIVO_TEMPERATURA = "files/temperatura.txt"

TIPO_RESULTADO_MUESTRA = "Muestra"
TIPO_RESULTADO_ALERTA = "Alerta"
TIPO_RESULTADO_ERROR = "Error"

MAX_HUMO = True
MIN_HUMO = False
TIEMPO_HUMO = 5

MAX_HUMEDAD = 100
MIN_HUMEDAD = 70
TIEMPO_HUMEDAD = 5

MAX_TEMPERATURA = 29.4
MIN_TEMPERATURA = 11
TIEMPO_TEMPERATURA = 6

HealthCheckSocket = TypedDict('HealthCheckSocket', {
    'host': str,
    'port_res': int,
    'port_health_check': int,
})

Socket = TypedDict('Socket', {
    'host': str,
    'port': int,
})

#para el fog informacion
PROXY_SOCKET: Socket = {
    'host': IP_PROXY, 
    'port': PROXY_PORT,
}

#para el fog BACK UP
PROXY_BACKUP_SOCKET: Socket = {
    'host': IP_PROXY_BACKUP, 
    'port': PROXY_BACKUP_PORT,
}

#informacion del broker principal
BrokerSocket = TypedDict('BrokerSocket', {
    'host': str,
    'sub_port': int,
    'pub_port': int,
})

BROKER_SOCKET: BrokerSocket = {
    'host': IP_BROKER, 
    'sub_port': BROKER_SUB_PORT,
    'pub_port': BROKER_PUB_PORT,
}


# DB_SOCKET: Socket = {
#     'host': '172.29.84.70', # TODO: Change this to the IP of the database server
#     'port': 5558,
# }

# HEALTH_CHECK_SOCKET: HealthCheckSocket = {
#     'host': '172.29.84.70', # TODO: Change this to the IP of the health check server
#     'port_res': 5559,
#     'port_health_check': 5560,
# }