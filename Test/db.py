from socket import fromshare
import mysql.connector
from app import app

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="newdb"
)
#Creating table for movies
movies_table_query = """CREATE TABLE movies
(
  movieid int(100) not null auto_increment PRIMARY KEY,
  moviename varchar(50) not null,
  moviegenre varchar(50) not null,
  director varchar(100) not null,
  language varchar(50) not null
)"""

#Creating Tables for role

# role_table_query = """CREATE TABLE role
# (
#     roleid int(100) not null auto_increment,
#     role varchar(50) not null,
#     CONSTRAINT role_pk PRIMARY KEY (roleid)
#  )"""


#creating table for user

# user_table_query = """CREATE TABLE user
# (
#   userid int(100) not null auto_increment PRIMARY KEY,
#   fullname varchar(50) not null,
#   username varchar(50) not null,
#   password varchar(50) not null,
#   usertype int(100) not null,
#   FOREIGN KEY (usertype) REFERENCES role(roleid)
#  )"""

cursor = mydb.cursor()
result = cursor.execute(movies_table_query)
print(" Movies table created successfully ")
# result = cursor.execute(role_table_query)
# print(" Role table created successfully ")
# result = cursor.execute(user_table_query)
# print(" User table created successfully ")
