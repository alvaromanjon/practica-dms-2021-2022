#Script de ejecución de la práctica
#Diseño y Mantenimiento del Software
#Autores: María Alonso Peláez, Álvaro Manjón Vara y Pablo Ahíta del Barrio

docker container ps -a>procesos.temp
wc -l procesos.temp>num_lineas.temp
numeros_hasta_espacio='[0-9]+\s'
numero_lineas=`grep -Po $numeros_hasta_espacio num_lineas.temp`
rm procesos.temp
rm num_lineas.temp
if [ $numero_lineas -eq 4 ]
then
    docker-compose -f docker/config/dev.yml rm -sfv
fi

docker-compose -f docker/config/dev.yml up -d
