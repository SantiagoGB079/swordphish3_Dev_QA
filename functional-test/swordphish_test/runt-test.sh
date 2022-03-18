#mvn clean verify

sudo docker build -f Dockerfile . -t testsw:1.0.0
sudo docker-compose up -d
