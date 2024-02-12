1. helm repo add prometheus-community  https://prometheus-community.github.io/helm-charts
2. kubectl create ns monitoring
3. helm install prom prometheus-community/kube-prometheus-stack -n monitoring 
4. helm repo add grafana https://grafana.github.io/helm-charts
5. helm upgrade --install loki grafana/loki -n monitoring --set service.type=LoadBalancer -f loki.yaml
6. helm upgrade --install promtail grafana/promtail -f promtail-values.yaml -n monitoring


9. kubectl patch service/prom-grafana -n monitroing --type='json' -p '[{"op":"replace","path":"/spec/type","value":"NodePort"}]'


10. cred Garafana 
        Username: admin
        Password: prom-operator

11. helm install nginx-app chart/
12. kubectl apply -f pv-storage-loki-0.yaml
