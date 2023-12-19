import boto3
import paramiko
from datetime import datetime, timedelta
import os
from dotenv import load_dotenv

# Загрузка переменных окружения из файла .env

load_dotenv('C:\\Users\\GGWP\\Desktop\\DevOps\\confs\\task10\\key.env')

aws_access_key = os.getenv('AWS_ACCESS_KEY_ID')
aws_secret_key = os.getenv('AWS_SECRET_ACCESS_KEY')

aws_region = 'us-east-1'

private_key_path = 'C:\\Users\\GGWP\\.ssh\\id_rsa\\task10.pem'
new_key_path = 'C:\\Users\\GGWP\\.ssh\\id_rsa\\private_task10key2'
local_new_key_path = 'C:\\Users\\GGWP\\.ssh\\id_rsa\\public_task10key2.pub'

ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

def create_instance():
    try:
        response = ec2.run_instances(
            ImageId='ami-0fc5d935ebf8bc3bc',
            MinCount=1,
            MaxCount=1,
            InstanceType='t2.micro',
            KeyName='task10',
            SecurityGroupIds=['sg-0970efc2c02864c2d'],
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': 'task10_python'}
                    ]
                }
            ]
        )
        instance_id = response['Instances'][0]['InstanceId']
        ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])

        instance_details = ec2.describe_instances(InstanceIds=[instance_id])
        public_ip = instance_details['Reservations'][0]['Instances'][0].get('PublicIpAddress', 'N/A')

        print(f'Запущен инстанс с ID: {instance_id}')
        print(f'Public IP: {public_ip}')

        return instance_id, public_ip
    except Exception as e:
        print(f"Произошла ошибка при создании инстанса: {e}")
        return None, None

def ssh_connect(ip_address, key_path):
    if ip_address:
        key = paramiko.RSAKey.from_private_key_file(key_path)
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        try:
            ssh.connect(ip_address, username='ubuntu', pkey=key)
            print("SSH соединение установлено.")
            ssh.close()
        except paramiko.SSHException as e:
            print(f"SSH соединение сброшено: {e}")
    else:
        print("Неверный IP-адрес. Убедитесь, что инстанс был успешно создан.")

def terminate_instance(instance_id):
    if instance_id:
        try:
            ec2.terminate_instances(InstanceIds=[instance_id])
            ec2.get_waiter('instance_terminated').wait(InstanceIds=[instance_id])
            print(f'Они убили инстанс: {instance_id} . Сволочи!.')
        except Exception as e:
            print(f"Произошла ошибка при остановке инстанса: {e}")
    else:
        print("Неверный ID инстанса. Убедитесь, что инстанс был успешно создан.")

def change_authorized_keys(ip_address, private_key_path, local_new_key_path):
    if ip_address:
        hostname = ip_address
        username = 'ubuntu'

        try:
            client = paramiko.SSHClient()
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            private_key = paramiko.RSAKey(filename=private_key_path)

            client.connect(hostname, username=username, pkey=private_key)

            sftp = client.open_sftp()
            sftp.put(local_new_key_path, '.ssh/authorized_keys')
            sftp.close()

            print('Ключ заменен.')
        except Exception as e:
            print(f"Произошла ошибка при смене ключа: {e}")
    else:
        print("Неверный IP-адрес. Убедитесь, что инстанс был успешно создан.")

def metrics(instance_id):
    if instance_id:
        client = boto3.client('cloudwatch', region_name='us-east-1')
        response = client.get_metric_data(
            MetricDataQueries=[
                {
                    'Id': 'a1',
                    'MetricStat': {
                        'Metric': {
                            'Namespace': 'AWS/EC2',
                            'MetricName': 'CPUUtilization',
                            'Dimensions': [
                                {'Name': 'InstanceId', 'Value': instance_id},
                            ]
                        },
                        'Period': 300,
                        'Stat': 'Average',
                    },
                    'ReturnData': True,
                }
            ],
            StartTime=datetime.utcnow() - timedelta(minutes=10),
            EndTime=datetime.utcnow()
        )
        return response
            
    else:
        print("Неверный ID инстанса. Убедитесь, что инстанс был успешно создан.")

while True:
    print("Выберите действие:")
    print("1 - Создать инстанс и вывести статистику.")
    print("2 - Попробовать установить SSH коннект.")
    print("3 - Убить инстанс.")
    print("4 - Сменить ключ.")
    print("5 - Установить соединение по новому ключу.")
    print("6 - Собрать загруженность CPU (Сходи за кофе, надо ждать)")
    choice = input("Выберите ваш вариант: ")

    if choice == '1':
        instance_id, public_ip = create_instance()
    elif choice == '2':
        ssh_connect(public_ip, private_key_path)
    elif choice == '3':
        terminate_instance(instance_id)
    elif choice == '4':
        change_authorized_keys(public_ip, private_key_path, local_new_key_path)
    elif choice == '5':
        ssh_connect(public_ip, new_key_path)
    elif choice == '6':
        print(metrics(instance_id))