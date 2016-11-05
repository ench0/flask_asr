from app import app, db # import our Flask app
import models
import views

if __name__ == '__main__':
#	app.run()
	app.run(host='0.0.0.0', port=5000) # accessible from outside
# We do not call app.run(debug=True) because we have already instructed Flask to
# run our app in the debug mode in the Configuration object.
