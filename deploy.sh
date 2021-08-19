#!/bin/bash

kubectl apply -f secret.yaml
kubectl apply -f config.yaml
kubectl apply -f mongo.yaml
kubectl apply -f server-depl.yaml
kubectl apply -f client-depl.yaml
