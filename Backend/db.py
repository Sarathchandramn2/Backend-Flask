import mysql.connector

mydb = mysql.connector.connect(

    host = "localhost",
    user = "root",
    password = "",
    database = "indproject"

)
mydb_Create_Table_Query = """CREATE TABLE movie
( movieId int(10) not null auto_increment ,
  movieName varchar(50) not null,
  movieGenre varchar(50) not null,
  director  varchar(50) not null,
  language varchar(50) not null,
  CONSTRAINT movie_pk PRIMARY KEY (movieId)
)"""




mydb_Create_Table_Query= """CREATE TABLE user
(
   userId int(100) auto_increment not null,
   yourname varchar(50) not null,
   username varchar(50) not null,
   password varchar(50) not null,
   CONSTRAINT user_pk PRIMARY KEY (user_id)
  
  
   )"""





cursor = mydb.cursor()
result = cursor.execute(mydb_Create_Table_Query)
print(" Table created successfully ")
