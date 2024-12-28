# RAG
Document Retrieval System

## for GCP setup

## Navigate to IAM & Admin:
->Open GCP Console in web

->In the left-hand menu, go to IAM & Admin > Service Accounts.

->Create a New Service Account:

->Click on + CREATE SERVICE ACCOUNT at the top.

->Enter a name and description for the service account, then click CREATE AND CONTINUE.

-Grant the Service Account Access to the Project:

->Assign the necessary roles to the service account. For example, you might need the Editor role or more specific roles depending on your use case.

->Click CONTINUE.

->Create a Key for the Service Account:

->Click + CREATE KEY.

->Select JSON as the key type and click CREATE.

->A JSON file will be downloaded to your computer. This is your service account key. rename it as credentials.json


## open command prompt and run the command

->export GOOGLE_APPLICATION_CREDENTIALS="path_to_credentials.json"

## to run code follow below command

1.pip install -r requirements.txt

2.python gcpcheck.py

3.python refreshtok.py

4.python export.py

5.streamlit run app.py
