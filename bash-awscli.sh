#!/bin/bash

AWS_ACCESS_KEY_ID=""
AWS_SECRET_ACCESS_KEY=""
DEFAULT_REGION="eu-east-1"
OUTPUT_FORMAT="json"


OS=$(lsb_release -a | awk '/Distributor ID:/ {print $3}')


if [ "$OS" = "RedHatEnterpriseServer" ]; then
    echo "Red Hat Enterprise Server, installing aws cli using yum."
    sudo yum install awscli -y
    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    aws configure set default.region $DEFAULT_REGION
    aws configure set default.output $OUTPUT_FORMAT
    echo "+++++++++++++++ Запущенные инстансы +++++++++++++++"
    aws ec2 describe-instances

elif [ "$OS" = "Ubuntu" ]; then
    echo "Ubuntu, installing aws cli using apt"
    sudo apt-get update
    sudo apt-get install awscli -y
    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    aws configure set default.region $DEFAULT_REGION
    aws configure set default.output $OUTPUT_FORMAT
    echo "+++++++++++++++ Запущенные инстансы +++++++++++++++"
    aws ec2 describe-instances

elif [ "$OS" = "Darwin" ]; then
    echo "MacOS, installing aws cli using Homebrew."
    brew install awscli
    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    aws configure set default.region $DEFAULT_REGION
    aws configure set default.output $OUTPUT_FORMAT
    echo "+++++++++++++++ Запущенные инстансы +++++++++++++++"
    aws ec2 describe-instances

elif [ "$OS" = "Microsoft" ]; then
    echo "You need to turn on WSL module and install ubuntu subsystem"
    echo "Windows, Please install aws cli using: bash current_script.sh"

else
    echo "Unsupported distribution: $OS"
fi
