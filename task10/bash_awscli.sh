#!/bin/bash

export $(grep -v '^#' key.env | xargs)
DEFAULT_REGION="us-east-1"
OUTPUT_FORMAT="json"

if [[ "$OSTYPE" == "linux-gnu" ]]; then
    source /etc/os-release
    echo "$ID"
    if [[ "$ID" == "rhel" ]]; then
        sudo yum update
        sudo subscription-manager register
        sudo yum install -y epel-release
        sudo yum install -y unzip
        curl "https://awscli.amazonaws.com/awscli-exe-linux-x86_64.zip" -o "awscliv2.zip"
        unzip awscliv2.zip
        sudo ./aws/install
        export PATH=$PATH:/usr/local/aws-cli/v2/2.15.2/bin
        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
        aws configure set default.region $DEFAULT_REGION
        aws configure set default.output $OUTPUT_FORMAT
        echo "+++++++++++++++ Запущенные инстансы +++++++++++++++"
        aws ec2 describe-instances --output table
    fi

    if [[ "$ID" == "ubuntu" ]]; then
        sudo apt update
        sudo apt install awscli -y
        aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
        aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
        aws configure set default.region $DEFAULT_REGION
        aws configure set default.output $OUTPUT_FORMAT
        echo "+++++++++++++++ Запущенные инстансы +++++++++++++++"
        aws ec2 describe-instances --output table
    fi

elif [[ "$OSTYPE" == "darwin"* ]]; then
    curl "https://awscli.amazonaws.com/AWSCLIV2.pkg" -o "AWSCLIV2.pkg"
    sudo installer -pkg AWSCLIV2.pkg -target /
    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    aws configure set default.region $DEFAULT_REGION
    aws configure set default.output $OUTPUT_FORMAT
    echo "+++++++++++++++ Запущенные инстансы +++++++++++++++"
    aws ec2 describe-instances --output table

elif [[ "$OSTYPE" == "msys" ]]; then
    powershell ./s.ps1
    aws configure set aws_access_key_id $AWS_ACCESS_KEY_ID
    aws configure set aws_secret_access_key $AWS_SECRET_ACCESS_KEY
    aws configure set default.region $DEFAULT_REGION
    aws configure set default.output $OUTPUT_FORMAT
    echo "+++++++++++++++ Запущенные инстансы +++++++++++++++"
    aws ec2 describe-instances --output table
fi
