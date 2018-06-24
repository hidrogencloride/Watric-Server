# Watric-Server
Empezar a desarollar servidor
<h1> Repository Purpose </h1>
<p> This repository is the development environment for the watric server </p>

<h1> Documentation : </h1>
<ol>
  <li>
    <h2>Setting up envrionment:</h2>
    <ul>
      <li> Clone repository </li>
      <li> After downloading postgresql create local database at postgresql server at port 5432 named watric_dev </li>
      <li> activate virtual environment or install requirements locally:
            for venv activation in git bash in project directory
            $ source ./venv/Scripts/activate or from requirements.txt
            $ pip install -r requirements.txt --no-index --find-links file:///tmp/packages
       </li>
       <li> export the necessary environment variables using the instructions in envVars file </li>
       <li> Run the following command from project directory: python manage.py db upgrade   this will add the models to your db connection</li>
       <li> speak to administrator for instructions on how to push to heroku and to github </li>
    </ul>
  </li>
  <li>
    <h2> Altering db schema: </h2>
    <p> After creatig new table, altering one, etc.. in the models.py 
      run $ python manage.py db migrate  afterwards run $ python manage.py db upgrade to see the new changes </p>
      <p> Speak with admin for instrucions on how to alter the db in heroku
  </li>
  <li> 
    <h2> Developing the Server endpoints and Functionalities </h2>
        <p> All the server functionality can be found inside app package in the __init__.py file </p>
  </li>
  <li>
    <h2> Running and testing local changes: </h2>
      <p> to initiate server run on cmd: python run.py </p> 
  </li>
</ol>
