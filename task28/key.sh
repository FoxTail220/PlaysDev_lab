#!/bin/bash

# Указываем имя секрета Kubernetes
SECRET_NAME="htpasswd"

# Указываем путь в SSM Parameter Store
PREVIOUS_VALUE=""


while :; do
    sleep 10
    PARAMETER_VALUE=$(aws ssm get-parameters --name webserver_passwd --region eu-west-2 --with-decryption --output text --query Parameters[].Value )
    BASE64_ENCODED_VALUE=$(echo -n "$PARAMETER_VALUE" )
    if [ "$BASE64_ENCODED_VALUE" = "$PREVIOUS_VALUE" ]; then
        echo "all ok"
    else
        kubectl create secret generic "$SECRET_NAME" \
        --from-literal=username="$BASE64_ENCODED_VALUE" \
        --dry-run=client --namespace default -o yaml | kubectl apply -f -

	kubectl apply -f /home/ubuntu/nginxapache-deployment/deployment.yaml
        PREVIOUS_VALUE=$BASE64_ENCODED_VALUE
        echo "Secret updated successfully."
    fi
done
