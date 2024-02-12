eksctl create cluster \
--name task30 \
--version 1.28 \
--region eu-west-2 \
--nodegroup-name k8s-nodes \
--node-type t3.medium \
--nodes 2 \
--nodes-min 2 \
--nodes-max 3
