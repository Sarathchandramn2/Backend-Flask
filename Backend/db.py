import mysql.connector

mydb = mysql.connector.connect(

    host = "localhost",

    user = "root",

    password = "",

    database = "indproject"

)
mydb_Create_Table_Query = """CREATE TABLE movie
( movie_id int(10) not null auto_increment ,
  movie_name varchar(50) not null,
  movie_genre varchar(50) not null,
  director  varchar(50) not null,
  language varchar(50) not null,
  CONSTRAINT movie_pk PRIMARY KEY (movie_id)
)"""




# mydb_Create_Table_Query= """CREATE TABLE user
# (
#    user_id int(100) auto_increment not null,
#    yourname varchar(50) not null,
#   username varchar(50) not null,
#   password varchar(50) not null,
#   CONSTRAINT user_pk PRIMARY KEY (user_id)
  
  
#    )"""





cursor = mydb.cursor()

result = cursor.execute(mydb_Create_Table_Query)

print(" Table created successfully ")
