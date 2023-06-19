### Title 
UltraXpert Solution

### Description
UltraXpert is a upcoming business model. It is a digital and big platform where a person who is highly qualified and knowledgeable will register themselves and sell their knowledge as a services to the indigent people. If any customer like and want to get their services, he/she also have to register and book their service by own and the expert will provide their service using meeting module.

### UltraXpert as a monetary tool for Experts.
In UltraXpert if any ualified or knowledgeable person want to sell their services. He/ She has register themselves after clearing a test. After registering he/she will be the Xpert of our platform. After becoming an expert he/she is able to create their service and sell on their prescribed prices. Expert can sell their services by creating time slots using meetiong module along with this he/she is also able to check their daily progress report. Expert also able to share their knowledge and skills by writing blogs using blog module. 

### UltraXpert as a helpful tool for Customer.
UltraXpert is very helpful for customers because customer is able to find expert as per their requirement and choice. After finding expert of their choice he/she able to book their time slots and service using booking module. Expert and customer will connect using meeting module. Customer is also able to read blogs as per their interest and also able to giving their advice by rating and reviews. Customer is also able to put their queries in the form of comments and take help from experts.

### Repository overview
```ultraxpert/
┣ .github/
┃ ┗ workflows/
┃   ┗ deploye.yml
┣ apis/
┃ ┣ admin.py
┃ ┣ api_base_url.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ blogs/
┃ ┣ migrations/
┃ ┃ ┗ __init__.py
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ serializers.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ booking/
┃ ┣ migrations/
┃ ┃ ┗ __init__.py
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ chat/
┃ ┣ migrations/
┃ ┃ ┗ __init__.py
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ serializers.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ constants/
┃ ┣ constants.py
┃ ┣ constants_prod.py
┃ ┗ __init__.py
┣ customers/
┃ ┣ migrations/
┃ ┃ ┗ __init__.py
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ serializers.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ enterprises/
┃ ┣ migrations/
┃ ┃ ┗ __init__.py
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ serializers.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ experts/
┃ ┣ migrations/
┃ ┃ ┗ __init__.py
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ serializers.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ help_function/
┃ ┣ aws_main.py
┃ ┣ main.py
┃ ┗ __init__.py
┣ inspections/
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ serializers.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ meetings/
┃ ┣ migrations/
┃ ┃ ┗ __init__.py
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ payments/
┃ ┣ migrations/
┃ ┃ ┗ __init__.py
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ serializers.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ static/
┃ ┣ css/
┃ ┃ ┗ main.css
┃ ┗ js/
┃   ┗ main.js
┣ structure/
┃ ┣ collages.json
┃ ┣ collage_structure.json
┃ ┣ cources.json
┃ ┣ education.json
┃ ┣ emoji.json
┃ ┗ state.json
┣ templates/
┃ ┣ componets/
┃ ┃ ┣ forms.html
┃ ┃ ┗ navbar.html
┃ ┣ emails/
┃ ┃ ┣ otp_verify.html
┃ ┃ ┗ welcome.html
┃ ┣ base.html
┃ ┗ index.html
┣ ultraxpert/
┃ ┣ asgi.py
┃ ┣ settings.py
┃ ┣ sitemaps.py
┃ ┣ urls.py
┃ ┣ wsgi.py
┃ ┗ __init__.py
┣ useraccounts/
┃ ┣ migrations/
┃ ┃ ┗ __init__.py
┃ ┣ adapter.py
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ authenticate.py
┃ ┣ manager.py
┃ ┣ models.py
┃ ┣ refercode.py
┃ ┣ serializers.py
┃ ┣ tests.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ wallet/
┃ ┣ migrations/
┃ ┃ ┗ __init__.py
┃ ┣ admin.py
┃ ┣ apps.py
┃ ┣ models.py
┃ ┣ serializers.py
┃ ┣ tests.py
┃ ┣ urls.py
┃ ┣ views.py
┃ ┗ __init__.py
┣ .dockerignore
┣ .gitignore
┣ docker-compose-prod.yml
┣ docker-compose.yml
┣ Dockerfile
┣ manage.py
┣ README.md
┗ requirements.txt
```
### To run UltraXpert Solution on a local system.
Requirements to run UltraXpert Solution
> System Requirements - System must have I3 processor with 8 GB Ram.
> Software Requirements - System must have Docker, WSL and a browser - Chrome to run the project locally and VS Code editor to edit the code.

> First you have to install Docker, WSL and VS code in your system. You can easily download docker and wsl using this link- ***WSL*** https://docs.docker.com/desktop/windows/wsl/. and VS Code as per your os using this link- ***VS Code*** https://code.visualstudio.com/download

> After downloading required softwares first open VS code and then clone the project using a git command - git clone- https://github.com/UltraCreation-IT-Solution/ultraxpert  

> After cloning project in your local system, you have to ask for .env file which has all the requirements.

> After getting .env file open terminal in vs code and run command - ```docker-compose-f"docker-compose.yml"``` up to create and run the docker container.

> After creating docker container successfully. You have to start container and open docker shell using "Attach Shell" option by right clicking on ultraxpert container

> After opening shell first you have to make migrations by using command - ```python manage.py makemigrations```

> After making migrations you have to migrate using this command -  ```python manage.py migrate```

> Now you are ready to run the ultraxpert project in you local system by using "Open in browser" option which is appearing by right click on "ultraxper-web"  docker container.


