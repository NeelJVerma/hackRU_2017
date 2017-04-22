#it imports app from app.py file under app/
#locally run the test server at port 8080.
#debug=True to run the applicaiton in debug mode
from app import app
app.run(host='0.0.0.0', port=8080, debug=True)