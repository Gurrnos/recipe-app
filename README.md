# Recipe app
Recipe app with functionality

# Installation
Create a .env file in the backend folder with the format below.  
DB_USER=(your db user here)  
DB_HOST=(your db host here)  
DB_PORT=(your db port here)  
DB_PASSWORD=(your db password here)  
DATABASE=(your database here)  
   
JWT_SECRET=(your secret token here) | You can use the following command in a linux terminal to generate a string:  
openssl rand -hex 32
  

Create a virtual environment and install the required pip packages, details below.  
<ins>Create a virtual environment:</ins> python -m venv ./venv  
<ins>Activate the venv:</ins> venv/Scripts/activate  
<ins>Install the required packages:</ins> pip install mysql-connector-python python-dotenv "fastapi[standard]" bcrypt pyjwt  
<ins>Run the program:</ins> python main.py  
  
For the frontend, make sure you have node, then simply run <ins>npm i</ins> to install the required packages  
Then run <ins>npm run dev</ins> to start the frontend  

  

# Changelog
