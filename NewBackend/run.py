from app import app
from views.admin.movie import *
from views.admin.Genre import *
from views.admin.Role import *
from views.user.users import *
from views.user.Rating import *


if __name__ == "__main__":  
     app.run(debug=True)