import boto3
import paramiko
from datetime import datetime, timedelta
import time

aws_access_key = ''
aws_secret_key = ''
aws_region = 'us-east-1'

global_private_key_path = 'C:\\Users\\GGWP\\.ssh\\id_rsa\\task10.pem' 
global_new_key_path = 'C:\\Users\\GGWP\\.ssh\\id_rsa\\private_task10key2' #сменить без расширения
global_local_new_key_path = 'C:\\Users\\GGWP\\.ssh\\id_rsa\\public_task10key2.pub'

ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key, region_name=aws_region)

instance_id = None
public_ip = None

#Определение функции для создания EC2 инстанса.
def create_instance():    
    response = ec2.run_instances(                                #Запуск инстанса с описанными параметрами.
        ImageId='ami-0fc5d935ebf8bc3bc', 
        MinCount=1, 
        MaxCount=1,
        InstanceType='t2.micro',
        KeyName='task10',
        SecurityGroupIds=['sg-0970efc2c02864c2d'], 
        
        TagSpecifications =[
            {
                'ResourceType':'instance',                       #Создание тегов. 
                'Tags':[
                    {
                        'Key':'Name',
                        'Value':'task10_python'
                    },
                ]
            }
        ]
    )

    global instance_id                                                                              #Глобальная переменная.
    instance_id = response['Instances'][0]['InstanceId']                                            #Сохраняет идентификатор созданного экземпляра из ответа в переменную instance_id.
    ec2.get_waiter('instance_running').wait(InstanceIds=[instance_id])                              #Ожидает, пока экземпляр будет запущен и готов к использованию.

    instance_details = ec2.describe_instances(InstanceIds=[instance_id])                            #Получает дополнительные сведения о созданном экземпляре с использованием его идентификатора.
    global public_ip                                                                                #Глобальная переменная 
    public_ip = instance_details['Reservations'][0]['Instances'][0].get('PublicIpAddress', 'N/A')   #Извлекает публичный IP-адрес созданного экземпляра или "N/A", если IP-адрес отсутствует, сохраняя значение в переменной public_ip.

    instance_type = instance_details['Reservations'][0]['Instances'][0]['InstanceType']             #Сохраняет тип созданного экземпляра в переменной instance_type.
    private_ip = instance_details['Reservations'][0]['Instances'][0]['PrivateIpAddress']            #Сохраняет приватный IP-адрес созданного экземпляра в переменной private_ip.
    os_type = instance_details['Reservations'][0]['Instances'][0].get('PlatformDetails', 'Linux')   #Извлекает сведения о типе операционной системы созданного экземпляра или устанавливает значение "Linux" по умолчанию и сохраняет в переменную os_type.

    print(f'Запущен инстанс с ID: {instance_id}')                                                   #Здесь и далее вывод информации об инстансе
    print(f'Тип инстанса: {instance_type}')
    print(f'Public IP: {public_ip}')
    print(f'Private IP: {private_ip}')
    print(f'ОС: {os_type}')

#Смена SSH-key
def change_authorized_keys():
        
    global global_private_key_path
    global global_local_new_key_path
            
    hostname = public_ip
    username = 'ubuntu'
    
    client = paramiko.SSHClient()                                                                   #Создает экземпляр класса `SSHClient` из библиотеки Paramiko, который используется для выполнения операций SSH.
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())                                    #Устанавливает политику автоматического добавления отсутствующих ключей хоста.
    
    private_key = paramiko.RSAKey(filename=global_private_key_path)                                  #Загружает приватный ключ из локального файла.
    
    client.connect(hostname, username=username, pkey=private_key)                                   #Устанавливает SSH-соединение с удаленным сервером, используя заданный адрес, имя пользователя и приватный ключ.
    
    sftp = client.open_sftp()                                                                       #Открывает подсоединение SFTP через установленное SSH-соединение.
    sftp.put(global_local_new_key_path, '.ssh/authorized_keys')                                            #Копирует новый открытый ключ на удаленный сервер в файл `authorized_keys` в папке `.ssh` пользователя.
    sftp.close()
    
    print('Ключ заменен.')
  
  
def ssh_connect():
    
    global_private_key_path                                                                         # Глобальная переменная, содержащая путь к приватному ключу SSH.
    
    key = paramiko.RSAKey.from_private_key_file(global_private_key_path)                            # Загружаем приватный ключ SSH из файла.
    ssh = paramiko.SSHClient()                                                                      # Создаем экземпляр клиента SSH из библиотеки Paramiko.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())                                       # Устанавливаем политику автоматического добавления отсутствующих ключей хоста.

    try:
        ssh.connect(public_ip, username='ubuntu', pkey=key)                                         # Устанавливаем SSH-соединение с удаленным сервером, используя публичный IP, имя пользователя 'ubuntu' и приватный ключ.
        print("SSH соединение установлено.")
        ssh.close()
    except Exception as fail:
        print(f"SSH соединение сброшено: {str(fail)}")                                              # Выводим сообщение об ошибке, если не удается установить соединение.

def terminate_instance():
    global instance_id                                                                              # Глобальная переменная инстанс айди
    if instance_id:
        ec2.terminate_instances(InstanceIds=[instance_id])                                          # Запускаем процесс завершения инстанса по его идентификатору.                                    
        ec2.get_waiter('instance_terminated').wait(InstanceIds=[instance_id])                       # Ожидаем, пока инстанс будет полностью завершен.
        print(f'Они убили инстанс: {instance_id} . Сволочи!.')                                      # Сообщение об успешном убиении инстанса 
        if public_ip:
            print(f'Public IP: {public_ip}')                                                        #Выводим публичный IP-адрес завершенного инстанса, если он доступен.
            
def ssh_connect_newkey():
    
    global_new_key_path                                                                             # Глобальная переменная нового ключа инстанса 
    
    key2 = paramiko.RSAKey.from_private_key_file(global_new_key_path)                               # Загружаем новый приватный ключ.
    ssh = paramiko.SSHClient()                                                                      # Создаем экземпляр класса `SSHClient` для установки SSH-соединения.
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())                                       # Устанавливаем политику автоматического добавления отсутствующих ключей хоста.

    try:
        ssh.connect(public_ip, username='ubuntu', pkey=key2)                                        # Устанавливаем SSH-соединение с использованием нового ключа.
        print("SSH соединение установлено.")
        ssh.close()
    except Exception as fail:
        print(f"SSH соединение сброшено: {str(fail)}")                                              # Выводим сообщение об ошибке, если соединение не удалось установить.

def metrics():
    client = boto3.client(
        'cloudwatch',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key,
        region_name=aws_region
    )
    response = client.get_metric_data(
        MetricDataQueries=[
            {
                'Id': 'm1',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'AWS/EC2',
                        'MetricName': 'CPUUtilization',
                        'Dimensions': [
                            {
                                'Name': 'InstanceId',
                                'Value': instance_id
                            },
                        ]
                    },
                    'Period': 300,  # 5 minutes (300 seconds)
                    'Stat': 'Average',
                },
                'ReturnData': True,
            },
            {
                'Id': 'm2',
                'MetricStat': {
                    'Metric': {
                        'Namespace': 'CWAgent',
                        'MetricName': 'mem_used_percent',
                        'Dimensions': [
                            {
                                'Name': 'InstanceId',
                                'Value': instance_id
                            },
                        ]
                    },
                    'Period': 300,  # 5 minutes (300 seconds)
                    'Stat': 'Average',
                },
                'ReturnData': True,
            }
        ],
        StartTime=datetime.utcnow() - timedelta(minutes=10),
        EndTime=datetime.utcnow()
    )

    print("Метрики загрузки CPU и RAM (за последние 10 минут):")
    print("CPU Utilization (%):", response['MetricDataResults'][0]['Values'][0])
    print("RAM Used Percent (%):", response['MetricDataResults'][1]['Values'][0])


while True:
    print("Выберите действие:")
    print("1 - Создать инстанс и вывести статистику.")
    print("2 - Попробовать установить SSH коннект.")
    print("3 - Убить инстанс.")
    print("4 - Сменить ключ.")
    print("5 - Установить соединение по новому ключу ")
    print("6 - Собрать загруженность CPU (Сходи за кофе, надо ждать)")
    choice = input("Выберите ваш вариант: ")

    if choice == '1':
        create_instance()
    elif choice == '2':
        if public_ip:
            ssh_connect()
    elif choice == '3':
        terminate_instance()
    elif choice == '4':
        change_authorized_keys()
    elif choice == '5':
        ssh_connect_newkey()
    elif choice == '6':
        metrics()

