# Vantagens de usar MySQL:
# Better concurrency -> Significa que pode aguentar muitos users simultaneamente
# Better for bigger data
# Support for more data types
# in-built authentication
# Multiple databases users(SQLite não têm esta opção)

# Para user MySQL, primeiro vamos ter que instalá-lo.
# Instalei o mysql community server neste site: https://dev.mysql.com/downloads/mysql/
# Primeiramente, fui ao ambiente de variáveis e dps system variables, path, clico em edit, new, e tenho que descobrir o
# path do mysql bin, que é: C:\Program Files\MySQL\MySQL Server 9.0\bin
# No Windows Powershell, escrevi: mysql -u root -p e coloquei a password do MySQL. Onde u significa user e p de password

# Posso usar o command line/terminal do pycharm!!
# cd C:\Users\cmmon\
# mysql -u root -p
# password
# SHOW DATABASES;
# CREATE DATABASE school;
# SHOW TABLES FROM school;
# USE school;
# CREATE TABLE students(
#   id INT AUTO_INCREMENT PRIMARY KEY,
#   name VARCHAR(255), -> 255 é o length máximo
#   course VARCHAR(255),
#   mobile VARCHAR(25)
#   );
# SHOW TABLES;
# SELECT * FROM students;
# INSERT INTO students(name,course,mobile)
#   VALUES()

