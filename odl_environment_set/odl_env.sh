#!/bin/bash -e

user=jeremy
path=/home/${user}
maven_path=${path}/files
#make sure only root can run the script
if [ "$(id -u)" != "0" ];then
	echo "You need to be 'root' dude!"
	exit 1
fi

apt-get -y install openjdk-7-jdk
#set the JAVA environment
cd /etc/profile.d
echo "export JAVA_HOME=/usr/lib/jvm/java-7-openjdk-amd64" >> java.sh
echo "export JRE_HOME=\${JAVA_HOME}/jre" >> java.sh
echo "export CLASSPATH=.:\${JAVA_HOME}/lib:\${JRE_HOME}/lib" >> java.sh
echo "export PATH=\${JAVA_HOME}/bin:\${JRE_HOME}/bin:\$PATH" >> java.sh

#unzip maven
#move the maven.zip to anywhere you want to locate
cd maven_path
tar -zxvf apache-maven-3.3.9-bin.tar.gz
cd /etc/profile.d
echo "export MAVEN_HOME=\${maven_path}/apache-maven-3.3.9" >> maven.sh
echo "export PATH=${PATH}:${MAVEN_HOME}/bin" >> maven.sh
