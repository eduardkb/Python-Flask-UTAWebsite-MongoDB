# Python Flask - UTA Website with MongoDB

## Description

    - CRUD website with MongoDB database
    - API with create, change and delete users
        (for API to work line 33 on file __init__.js
        has to be uncommented)

## Run Project:

    - create venv inside project dir
        python -m venv venv
    - activate venv
        Win:
            .\venv\Scripts\activate
        Linux:
            source venv/bin/activate
            deactivate (to deactivate)
    - install requirements
        pip install -r requirements.txt
    - Change IP address and DB data
	change public IP address of the MongoDB server 
	on file application/__init__.py
    - initiate flask server
        flask run
        or
        flask run -h localhost -p 3000

## WebPage User ID and pass

    - john:john1234
