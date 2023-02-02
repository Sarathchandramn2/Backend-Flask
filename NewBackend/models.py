
# creating the moive class
class Movie:
    def __init__(self,movieid: str, moviename: str, moviegenre: str, director: str, language: int):
        self.movieid = movieid
        self.moviename = moviename;
        self.moviegenre = moviegenre
        self.director = director
        self.language = language
        
# creating the  role class
class Role:
    def __init__(self, roleid: str, role: str):
        self.roleid = roleid
        self.role = role
        
#creating the user class
class User:
    def __init__(self, userid:str, fullname:str, username:str, password:str, usertype: str):
        self.userid = userid
        self.fullname = fullname
        self.username = username
        self.password = password
        self.usertype = usertype
        
#creating the genre class
class Genre:
    def __init__(self, genreid: str, genre: str):
        self.genreid = genreid
        self.genre = genre
#Creating the Rating class        
class Rating:
    def __init__(self,rateid:str,userid:str,movieid:str,rating:str):
        self.rateid=rateid
        self.userid=userid
        self.movieid=movieid
        self.rating=rating