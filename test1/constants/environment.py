from typing import TypedDict

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
    'host': "192.168.193.126", 
    'port': 5358,
}

#para el fog BACK UP
PROXY_BACKUP_SOCKET: Socket = {
    'host': "", 
    'port': 5101,
}

#informacion del broker principal
BrokerSocket = TypedDict('BrokerSocket', {
    'host': str,
    'sub_port': int,
    'pub_port': int,
})
BROKER_SOCKET: BrokerSocket = {
    'host': "192.168.193.126", 
    'sub_port': 5006,
    'pub_port': 5086,
}


#para el aspersor
ASPERSOR: Socket = {
    'host': "192.168.193.126", 
    'port': 5081,
}

#para el SC
SC_EDGE: Socket = {
    'host': "192.168.193.126", 
    'port': 5091,
}

#para el SC
SC_FOG: Socket = {
    'host': "192.168.193.126", 
    'port': 5092,
}

SC_CLOUD: Socket = {
    'host': "192.168.193.126", 
    'port': 5093,
}

CLOUD: Socket = {
    'host': "192.168.193.126", 
    'port': 5253,
}

HealthCheck = TypedDict('HealthCheck', {
    'host': str,
    'port_1': int,
    'port_2': int,
})

HEALTH_CHECK: HealthCheck = {
    'host': "192.168.193.126", 
    'port_1': 5999,
    'port_2': 5989
}

MONGODB = {
    'uri': 'mongodb+srv://sophie:hEh3mnqukd9t73Ca@proyectodistribuidos.by5tqz6.mongodb.net/?retryWrites=true&w=majority&appName=ProyectoDistribuidos',
    'database': 'ProyectoDistribuidos',
    'collection_sensor': 'SensorData',
    'collection_calc': 'CalculationData',
    'collection_alerta': 'AlertData',
}