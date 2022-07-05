import random


def detector(service):
    fraud_score = round(random.random(), 1)
    return fraud_score


def classificator(service):
    service_class = random.randint(1, 5)

    services = {1: 'консультация',
                2: 'лечение',
                3: 'стационар',
                4: 'диагностика',
                5: 'лаборатория'}
    service_name = services[service_class]
    return service_class, service_name
