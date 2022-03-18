echo 'CORRIENDO PRUEBAS'
#echo 'CREANDO IMAGEN DOCKER'
#docker build -t swtestsjar:1.0.0 ./swordphish_test/
#echo 'IMAGE CREATED SUCCESSFULLY'
#docker-compose -f ./swordphish_test/docker-compose.yml up -d
mvn clean -f ./swordphish_test/pom.xml verify
