#!/bin/bash

# Atualiza os pacotes
sudo dnf upgrade -y

# Instala Apache e PHP
sudo dnf install -y httpd wget php-fpm php-mysqli php-json php php-devel

# Instala MariaDB (adicionado -y para não travar a automação)
sudo dnf install mariadb105-server -y

# Configura e inicia o Apache
sudo systemctl start httpd
sudo systemctl enable httpd

# Ajusta permissões de pastas
sudo usermod -a -G apache ec2-user
sudo chown -R ec2-user:apache /var/www
sudo chmod 2775 /var/www && find /var/www -type d -exec sudo chmod 2775 {} \;
find /var/www -type f -exec sudo chmod 0664 {} \;

# Inicia o MariaDB para podermos configurá-lo
sudo systemctl start mariadb

# --- INÍCIO DA AUTOMAÇÃO DO mysql_secure_installation ---
# Define a senha do root como "aluno123"
sudo mysql -e "ALTER USER 'root'@'localhost' IDENTIFIED BY 'aluno123';"
# Remove usuários anônimos
sudo mysql -e "DELETE FROM mysql.user WHERE User='';"
# Bloqueia acesso remoto do root
sudo mysql -e "DELETE FROM mysql.user WHERE User='root' AND Host NOT IN ('localhost', '127.0.0.1', '::1');"
# Remove o banco de dados de teste
sudo mysql -e "DROP DATABASE IF EXISTS test;"
sudo mysql -e "DELETE FROM mysql.db WHERE Db='test' OR Db='test\\_%';"
# Recarrega os privilégios
sudo mysql -e "FLUSH PRIVILEGES;"
# --- FIM DA AUTOMAÇÃO ---

# Habilita o MariaDB para iniciar com a máquina
sudo systemctl enable mariadb

# Instala extensões extras do PHP para o phpMyAdmin
sudo dnf install php-mbstring php-xml -y

# Reinicia os serviços
sudo systemctl restart httpd
sudo systemctl restart php-fpm

# Baixa e configura o phpMyAdmin
cd /var/www/html
wget https://www.phpmyadmin.net/downloads/phpMyAdmin-latest-all-languages.tar.gz
mkdir phpMyAdmin && tar -xvzf phpMyAdmin-latest-all-languages.tar.gz -C phpMyAdmin --strip-components 1
rm phpMyAdmin-latest-all-languages.tar.gz

# Garante que o MariaDB está rodando no final do processo
sudo systemctl start mariadb