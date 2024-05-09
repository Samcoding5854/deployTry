from flask import Flask

# Create an instance of Flask
app = Flask(__name__)

# Define a route for the home page
@app.route('/')
def home():
    return 'Hello, this is the home page!'

# Define a route for another page
@app.route('/about')
def about():
    return 'This is the about page.'

# Define a route that takes a parameter
@app.route('/user/<username>')
def user_profile(username):
    return 'Hello, {}!'.format(username)

# Run the application if the script is executed directly
if __name__ == '__main__':
    app.run(debug=True)
