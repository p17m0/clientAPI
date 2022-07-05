from random import randint

def detector(service):
    fraud_score = randint(0, 1)
    return fraud_score


def classificator():
    service_class = randint(1, 5)

    services = {1: 'консультация',
                2: 'лечение',
                3: 'стационар',
                4: 'диагностика',
                5: 'лаборатория'}
    service_name = services[service_class]
    return service_class, service_name
