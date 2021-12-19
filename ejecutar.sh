#!/bin/bash
#Script de ejecución de la práctica
#Diseño y Mantenimiento del Software
#Autores: María Alonso Peláez, Álvaro Manjón Vara y Pablo Ahíta del Barrio

if [[ "$(docker ps --format "{{.Names}}")" =~ "dms2122auth" || "$(docker ps --format "{{.Names}}")" =~ "dms2122backend" || "$(docker ps --format "{{.Names}}")" =~ "dms2122frontend" ]]; then
  docker-compose -f docker/config/dev.yml rm -sfv
fi

docker-compose -f docker/config/dev.yml up -d
