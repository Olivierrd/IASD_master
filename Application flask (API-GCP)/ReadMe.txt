Ce dossier permet de créer une api depuis GCP. Une boite mail peut être connectée pour envoyer des mails d'erreurs

1. id_mail est construit à partir de gmail. Des accès génériques doivent être paramétrées lorsque la double authentification est activée
   https://www.twilio.com/blog/2018/03/send-email-programmatically-with-gmail-python-and-flask.html

2. Pour accéder à GCP il faut mettre les crédentials : Application flask (API-GCP)\setup\credentials. Il faut mettre à jour le fichier key_prod.json
   https://cloud.google.com/docs/authentication/getting-started

3. Enfin, l'objectif est de lancer un job que l on place dans le dossier apps : my_apps.py 
   import apps 
   from apps import my_apps
   test_function()
   
   