from app import app, db
from app.models import User

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User':User, 'Post':Post}

#The flask shell command is another very useful tool in the flask umbrella of commands. 
# The shell command is the second "core" command implemented by Flask, after run. The purpose of this command is to 
# start a Python interpreter in the context of the application. What does that mean? See the following example: 
# With a regular interpreter session, the app symbol is not known unless it is explicitly imported, but when using flask shell, 
# the command pre-imports the application instance. The nice thing about flask shell is not that it pre-imports app, but that 
# you can configure a "shell context", which is a list of other symbols to pre-import.
# The following function in microblog.py creates a shell context that adds the database instance 
# and models to the shell session:
# The app.shell_context_processor decorator registers the function as a shell context function. 
# When the flask shell command runs, it will invoke this function and register the items returned by it in the shell session.
# The reason the function returns a dictionary and not a list is that for each item you have to also provide a name under 
# which it will be referenced in the shell, which is given by the dictionary keys.
# After you add the shell context processor function you can work with database entities without having to import them:
# If you try the above and get NameError exceptions when you access db, User and Post, then the make_shell_context() function is not
# being registered with Flask. The most likely cause of this is that you have not set FLASK_APP=microblog.py in the environment. 
# In that case, go back to Chapter 1 and review how to set the FLASK_APP environment variable. If you often forget to set this variable when you open new terminal
# windows, you may consider adding a .flaskenv file to your project, as described at the end of that chapter.