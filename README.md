REST API for warehouse inventory management built with FastAPI. 
This API has 2 routes
1) Product route
This route is reponsible for creating products, deleting product, updating product and Checkinh product
2) Order route
This route is about creating orders and updating orders status by id


how to run locally
First clone this repo by using following command

git clone https://github.com/marklenin/warehouse-api-fastapi.git

then


cd cd warehouse-api-fastapi

Then install fastapp using all flag like


pip install fastapi[all]


Then go this repo folder in your local computer run follwoing command


uvicorn main:app --reload

Then you can use following link to use the API


http://127.0.0.1:8000/docs 

After run this API you need a database in postgres
Create a database in postgres then create a file name .env and write the following things in you file

DATABASE_HOSTNAME = localhost
DATABASE_PORT = 5432
DATABASE_PASSWORD = passward_that_you_set
DATABASE_NAME = name_of_database
DATABASE_USERNAME = User_name
