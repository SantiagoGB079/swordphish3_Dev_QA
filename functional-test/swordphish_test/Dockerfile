#FROM maven:3.6.0-jdk-11-slim
FROM maven:3-jdk-8-alpine
COPY src /home/app/src
COPY pom.xml /home/app
RUN mvn -f /home/app/pom.xml compile
COPY target /home/app
ENTRYPOINT ["mvn", "-f", "/home/app/pom.xml", "verify"]


