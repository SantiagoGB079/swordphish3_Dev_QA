echo 'COMPILANDO'
echo 'CREANDO IMAGEN DOCKER'
docker build -t swtestsjar:1.0.0 ./functional-test/swordphish_test/
echo 'IMAGE CREATED SUCCESSFULLY'
docker-compose -f ./functional-test/swordphish_test/docker-compose.yml up -d
echo 'CONTAINERS UP'
