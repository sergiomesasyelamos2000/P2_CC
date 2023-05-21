#!/bin/bash

minikube start &&
kubectl rollout status -n openfaas deploy/gateway &&
kubectl port-forward -n openfaas svc/gateway 8080:8080 &
sleep 5
faas-cli up -f ejercicio.yml &&
curl -d "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCdio_Sf9aON6NjLHo5fXjG1HNZzWCaTsUjQ" http://127.0.0.1:8080/function/ejercicio -o salida.html &&
faas-cli up -f testdnn.yml &&
curl -d "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSCdio_Sf9aON6NjLHo5fXjG1HNZzWCaTsUjQ" http://127.0.0.1:8080/function/testdnn -o testdnn.html
