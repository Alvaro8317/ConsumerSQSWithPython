import boto3
from dotenv import load_dotenv
import json
from datetime import date
load_dotenv()
sqs = boto3.resource("sqs")
s3 = boto3.resource("s3")


def list_buckets():
    for bucket in s3.buckets.all():
        print(bucket.name)


def write_into_a_file(file, message):
    with open(file, 'a') as file_to_modify:
        today = date.today()
        file_to_modify.write(f'\nTime: {today}: Details: {message}\n')

def init_queue(option_by_user: bool = False):
    try:
        queue = sqs.create_queue(QueueName="demo_s3", Attributes={"DelaySeconds": "10"})
        if option_by_user:
            print(queue) 
            print(queue.url)
            print(queue.attributes.get("DelaySeconds"))
        return queue
    except Exception as e:
        queue = sqs.get_queue_by_name(QueueName="demo_s3")
        return queue


def list_queues():
    for queue in sqs.queues.all():
        print(queue)


def send_message(queue, message: str = "test"):
    message_to_send = queue.send_message(
        MessageBody=message,
        MessageAttributes={
            "Author": {"StringValue": "Alvaro Garzón", "DataType": "String"}
        },
    )
    return message_to_send


def consume_messages(queue):
    messages = queue.receive_messages(MaxNumberOfMessages=10, WaitTimeSeconds=20)
    try:
      for message in messages:
        info_to_add = message.body
        write_into_a_file('consumed/info.txt', info_to_add)
        test = message.delete()
        print(test)
    except Exception as e:
        print(e)


def purge_queue(queue):
    while True:
        messages = queue.receive_messages(
            MaxNumberOfMessages=10,  # solicita hasta 10 mensajes en una llamada
            WaitTimeSeconds=10,  # espera hasta 10 segundos por mensajes
        )

        # Si no hay mensajes, la cola está vacía y podemos salir del bucle
        if not messages:
            break

        # Elimina los mensajes recibidos
        for message in messages:
            message.delete()


if __name__ == "__main__":
    print("""Hello there!""")
    while True:
        print(
            "1. List the name of the buckets\n2. Create the queue\n3. List the queues\n4. Send a message to the queue\n5. Consume the messages\nOr send a letter to exit"
        )
        option_from_user = input("Choose an option, write only the number please: ")
        queue = init_queue(False)
        match option_from_user:
            case "1":
                list_buckets()
            case "2":
                init_queue(True)
            case "3":
                list_queues()
            case "4":
                message = input("What message do you want to send? ")
                result = send_message(queue, message)
                if result["ResponseMetadata"]["HTTPStatusCode"] == 200:
                    print("\nMessage sent successfully\n")
            case "5":
                consume_messages(queue)
            case "6":
                purge_queue(queue)
            case _:
                break
