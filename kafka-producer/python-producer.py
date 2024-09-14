import time
import schedule
from json import dumps
from faker import Faker
from kafka import KafkaProducer

kafka_nodes = "kafka:9092"
myTopic = "sentence"

def gen_data():
    faker = Faker()

    prod = KafkaProducer(bootstrap_servers=kafka_nodes,
                         value_serializer=lambda x:dumps(x).encode('utf-8'))
    
    my_data = {'sentence': faker.sentence()}
    print(my_data)
    prod.send(topic=myTopic, value=my_data)

    prod.flush()


if __name__=="__main__":
    schedule.every(5).seconds.do(gen_data)

    while True:
        schedule.run_pending()
        time.sleep(0.5)
