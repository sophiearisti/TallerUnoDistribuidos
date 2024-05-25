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
    'host': "192.168.193.126", 
    'sub_port': 5006,
    'pub_port': 5086,
}


#para el aspersor
ASPERSOR: Socket = {
    'host': "192.168.193.126", 
    'port': 5011,
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
    'port': 5223,
}

MONGODB = {
    'uri': 'mongodb+srv://saristizabal1017:2ieC9pQ5Y1913x56@distribuidos.eguzenz.mongodb.net/?retryWrites=true&w=majority&tlsAllowInvalidCertificates=true',
    'database': 'distribuidos',
    'collection_sensor': 'SensorData',
    'collection_calculation': 'CalculationData',
    'collection_alert': 'AlertData',
}