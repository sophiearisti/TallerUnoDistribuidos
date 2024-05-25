from typing import TypedDict


CLOUD_PORT = 5001
ASPERSOR_PORT = 5001
SC_PROXY_PORT = 5557
SC_EDGE_PORT = 5007
SC_CLOUD_PORT = 5007

IP_CLOUD = ""
IP_SC_PROXY = ""
IP_SC_EDGE = ""
IP_SC_CLOUD = ""
IP_ASPERSOR = ""

CANT_SENSORES = 10
SENSOR_PORT = 5001
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
    'host': "192.168.193.148", 
    'port': 5558,
}

#para el fog BACK UP
PROXY_BACKUP_SOCKET: Socket = {
    'host': "", 
    'port': 5001,
}

#informacion del broker principal
BrokerSocket = TypedDict('BrokerSocket', {
    'host': str,
    'sub_port': int,
    'pub_port': int,
})
BROKER_SOCKET: BrokerSocket = {
    'host': "192.168.193.148", 
    'sub_port': 5006,
    'pub_port': 5086,
}


#para el aspersor
ASPERSOR: Socket = {
    'host': "192.168.193.148", 
    'port': 5011,
}

#para el SC
SC_EDGE: Socket = {
    'host': "192.168.193.148", 
    'port': 5091,
}

#para el SC
SC_FOG: Socket = {
    'host': "192.168.193.148", 
    'port': 5092,
}

SC_CLOUD: Socket = {
    'host': "192.168.193.148", 
    'port': 5093,
}

CLOUD: Socket = {
    'host': "192.168.193.148", 
    'port': 5223,
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

MONGODB = {
    'uri': 'mongodb+srv://admin:admin@proyectodistribuidos.by5tqz6.mongodb.net/?retryWrites=true&w=majority&appName=ProyectoDistribuidos',
    'database': 'ProyectoDistribuidos',
    'collection': 'SensorData',
}