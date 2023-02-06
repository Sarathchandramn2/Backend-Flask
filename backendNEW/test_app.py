import unittest
from flask import Flask, request
from views.admin.movie import demo

app = Flask(__name__)

class TestDemo(unittest.TestCase):
    def setUp(self):
        self.movieid = 1
        self.moviename = "The Shawshank Redemption"
        self.moviegenre = "Drama"
        self.language = "English"
        self.director = "Frank Darabont"
        self.app = app.test_client()
        

    def test_demo_success(self):
        response = self.app.post('/admin/movie', data=dict(
            movieid=self.movieid,
            moviename=self.moviename,
            moviegenre=self.moviegenre,
            language=self.language,
            director=self.director
        ))
        response = demo(self.movieid, self.moviename, self.moviegenre, self.language, self.director,self.request)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json(), {"message": "movie added successfully!"})

    def test_demo_missing_params(self):
        response = self.app.post('/admin/movie', data=dict(
            movieid=self.movieid,
            moviename="",
            moviegenre="",
            language="",
            director=""
        ))
        response = demo(self.movieid, self.moviename, self.moviegenre, self.language, self.director,self.request)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.get_json(), {"message": "All fields are required"})

if __name__ == '__main__':
    unittest.main()
