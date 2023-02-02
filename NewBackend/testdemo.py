
# class TestCreateMovie(unittest.TestCase):
#     def test_create_movie_success(self):
#         # arrange
#         url = "http://localhost:5000/movie"
#         headers = {'Content-Type': 'application/json'}
#         data = {
#             "moviename": "kgf",
#             "moviegenre": "Action",
#             "language": "Malayalam",
#             "director": "Lal"
#         }

#         # act
#         response = requests.post(url, headers=headers, json=data)

#         # assert
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.json(), {"message": "movie added successfully!"})

#     def test_create_movie_missing_fields(self):
#         # arrange
#         url = "http://localhost:5000/movie"
#         headers = {'Content-Type': 'application/json'}
#         data = {
#             "moviename": "kgf",
#             "moviegenre": "Action",
#         }

#         # act
#         response = requests.post(url, headers=headers, json=data)

#         # assert
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json(), {"message": "Some Columns are missing or Mispelled the Column name"})

#     def test_create_movie_empty_fields(self):
#         # arrange
#         url = "http://localhost:5000/movie"
#         headers = {'Content-Type': 'application/json'}
#         data = {
#             "moviename": "",
#             "moviegenre": "Action",
#             "language": "Malayalam",
#             "director": "Lal"
#         }

#         # act
#         response = requests.post(url, headers=headers, json=data)

#         # assert
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json(), {"message": "Field cannot be empty"})

#     def test_create_movie_duplicate(self):
#         # arrange
#         url = "http://localhost:5000/movie"
#         headers = {'Content-Type': 'application/json'}
#         data = {
#             "moviename": "kgf",
#             "moviegenre": "Action",
#             "language": "Malayalam",
#             "director": "Lal"
#         }

#         # act
#         response = requests.post(url, headers=headers, json=data)

#         # assert
#         self.assertEqual(response.status_code, 400)
#         self.assertEqual(response.json(), {"message": "Movie already exists with the same name"})

import unittest
import httplib2
import json

class TestCreateMovie(unittest.TestCase):
    def test_create_movie_success(self):
        # arrange
        url = "http://localhost:5000/movie"
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({
            "moviename": "kgf",
            "moviegenre": "Action",
            "language": "Malayalam",
            "director": "Lal"
        })

        # act
        http = httplib2.Http()
        response, content = http.request(url, method='POST', body=data, headers=headers)

        # assert
        self.assertEqual(response.status, 200)
        self.assertEqual(json.loads(content), {"message": "movie added successfully!"})

    def test_create_movie_missing_fields(self):
        # arrange
        url = "http://localhost:5000/movie"
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({
            "moviename": "kgf",
            "moviegenre": "Action",
        })

        # act
        http = httplib2.Http()
        response, content = http.request(url, method='POST', body=data, headers=headers)

        # assert
        self.assertEqual(response.status, 400)
        self.assertEqual(json.loads(content), {"message": "Some Columns are missing or Mispelled the Column name"})

    def test_create_movie_empty_fields(self):
        # arrange
        url = "http://localhost:5000/movie"
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({
            "moviename": "",
            "moviegenre": "Action",
            "language": "Malayalam",
            "director": "Lal"
        })

        # act
        http = httplib2.Http()
        response, content = http.request(url, method='POST', body=data, headers=headers)

        # assert
        self.assertEqual(response.status, 400)
        self.assertEqual(json.loads(content), {"message": "Field cannot be empty"})

    def test_create_movie_duplicate(self):
        # arrange
        url = "http://localhost:5000/movie"
        headers = {'Content-Type': 'application/json'}
        data = json.dumps({
            "moviename": "kgf",
            "moviegenre": "Action",
            "language": "Malayalam",
            "director": "Lal"
        })

        # act
        http = httplib2.Http()
        response, content = http.request(url, method='POST', body=data, headers=headers)

        # assert
        self.assertEqual(response.status, 400)
        self.assertEqual(json.loads(content), {"message": "Movie already exists with the same name"})
