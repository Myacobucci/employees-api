# Employees Api Project

## Description

This is a project that provides a web app with read-only JSON apis for 3 resources:
employees, departments and offices.

There is not a database for the data of these resources. The employees information is read
from an external endpoint, and the departments and offices are read from json files, one for each.

The external api for the employees data must accept limit and offset parameters and
also be able to get consecutive ids. So the next 2 examples are valid:

- http:/www.myexternalapi.com/employees?limit=10&offset=0
- http:/www.myexternalapi.com/employees?id=2&id=3

The json files for departments and offices must be a list of objects with the respective information.

The api endpoints provided by this app accepts "limit" and "offset" as parameters, and also "expand". With the expand parameter it's possible to expand information inside the resources.

This project is implemented using Python, Flask, Flask RestX, Webargs and Docker.

## Intallation steps

1. Clone this project
2. Put the **departments.json** and **offices.json** files in the directory _employees-server/resources_
3. Paste the company resources url in the corresponding variable inside _employees-server/settings.py_ (remember that you don't have to specify the employees path)
4. Run `docker build -t employees_api_docker:latest .`
5. Run `docker run -p 5000:5000 employees_api_docker:latest`

So now the server is running on http://0.0.0.0:5000/

In this URL you can find the Swagger documentation of all the endpoints supported by this app.

To run the unit tests execute `./run_tests.sh`
