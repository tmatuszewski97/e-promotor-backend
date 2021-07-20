# :mortar_board: ePromotor - Backend (REST API)

REST API created with Django and Django REST framework. It's working with [this mobile application](https://github.com/tmatuszewski97/e-promotor-mobile-app) and supports the registrations process to academic supervisors at the University of Warmia and Mazury in Olsztyn at Faculty Of Mathematics And Computer Science.

## :link: Table of Contents
- [General Informations](#pill-general-informations)
- [Technologies Used](#wrench-technologies-used)
- [Features](#pencil-features)
- [Endpoints](#mag-endpoints)
- [Setup](#hammer-setup)
- [Usage](#page_facing_up-usage)

## :pill: General Informations

The project was made as a part of my Engineering Thesis. Created system takes care about correct conduct of promoter elections and accelerates this process. Moreover, the app offers other [features](#pencil-features), depending on role of logged user. The API uses TokenAuthentication included in Django REST framework.

## :wrench: Technologies Used

- [Python](https://www.python.org/) (version: 3.9.1)
- [Amazon S3](https://aws.amazon.com/s3/) (for storing users' files)
- [MySQL](https://www.mysql.com/) or [PostgreSQL](https://www.postgresql.org/) database system (for develop I used MySQL, for production - PostgreSQL
- [Django](https://www.djangoproject.com/) (version: 3.1.12)
- [Django REST framework](https://www.django-rest-framework.org/) (version: 3.12.2)
- [Django Cleanup](https://pypi.org/project/django-cleanup/) (version: 5.1.0)
- [Django Storages](https://django-storages.readthedocs.io/en/latest/) (version: 1.11.1)
- (...) and some other less important libraries (you can find all packages in [requirements.txt](requirements.txt) file)

## :pencil: Features

1. Main features:
   - Elections are divided into tours. If student will not be able to find a promoter in a given tour, he will go to the next one.
   - The whole process continues until assignment every student to promoter (or disqualification the inactive ones).

2. Features for all types of users:
   - Login / logout function.
   - Changing password.
   - Checking elections status.

3. Features for employees of a dean's office:
   - Registering promoters or students from .csv file.
   - Management of promoters' or students' accounts (edition/deletion).
   - Sharing files between specified user group (allowed groups: employees of dean's office / promoters / students).
   - Management of files belonging to logged user or his group.
   - Disqualification of inactive students.
   - Exporting final data to .csv file (the file contains list of students - associated with selected promoter or disqualified).
   - Changing informations about logged user.

4. Features for promoters:
   - Checking other promoters' profile pages.
   - Sharing files between specified user group (allowed groups: employees of dean's office / promoters / students).
   - Confirming or rejecting students' requests.
   - Changing informations about logged user.

5. Features for students:
   - Selecting other promoter for each of three preferences and sending requests.
   - Showing informations about logged user.

## :mag: Endpoints

   | Endpoint | HTTP Method | Result | Permissions|
   | :---: | :---: | --- | --- |
   | ```login/``` | POST | Return token associated with user, if he sent valid credentials. | |
   | ```user/``` | GET | Return informations about logged in user. | Only for logged in users. |
   | ```user/``` | PUT/PATCH | Change informations associated with logged in user. | Only for logged in users. |
   | ```user/change-password/``` | PUT | Change password associated with logged in account. | Only for logged in users. |
   | ```dean-worker/``` | GET | Return list of employees of a dean's office. | Only for administrators or employees of a dean's office. |
   | ```dean-worker/<int:pk>/``` | GET | Return informations about specified employee of a dean's office. | Only for administrators or employees of a dean's office. |
   | ```dean-worker/<int:pk>/``` | PUT/PATCH | Change informations associated with specified employee of a dean's office. | Only for administrators. |
   | ```dean-worker/<int:pk>/``` | DELETE | Delete specified employee of a dean's office. | Only for administrators. |
   | ```dean-worker/register/``` | POST | Create account for employee of a dean's office. | Only for administrators. |
   | ```promoter/``` | GET | Return list of promoters. | Only for logged in users. |
   | ```promoter/<int:pk>/``` | GET | Return informations about specified promoter and list of his files. | Only for logged in users. |
   | ```promoter/<int:pk>/``` | PUT/PATCH | Change informations associated with specified promoter. | Only for administrators or employees of a dean's office. |
   | ```promoter/<int:pk>/``` | DELETE | Delete specified promoter. | Only for administrators or employees of a dean's office. |
   | ```promoter/bulk-register/``` | POST | Create accounts for promoters based on attached .csv file. | Only for administrators or employees of a dean's office. |
   | ```promoter/bulk-delete/``` | POST | Delete specified promoters. | Only for administrators or employees of a dean's office. |
   | ```student/``` | GET | Return list of students. | Only for administrators or employees of a dean's office. |
   | ```student/<int:pk>/``` | GET | Return informations about specified student. | Only for administrators or employees of a dean's office. |
   | ```student/<int:pk>/``` | PUT/PATCH | Change informations associated with specified student. | Only for administrators or employees of a dean's office. |
   | ```student/<int:pk>/``` | DELETE | Delete specified student. | Only for administrators or employees of a dean's office. |
   | ```student/bulk-register/``` | POST | Create accounts for students based on attached .csv file. | Only for administrators or employees of a dean's office. |
   | ```student/bulk-delete/``` | POST | Delete specified students. | Only for administrators or employees of a dean's office. |
   | ```file/``` | GET | Return list of files associated with logged in user. | Only for logged in users. |
   | ```file/<int:pk>/``` | GET | Return informations about specified file. | Only for logged in users. |
   | ```file/<int:pk>/``` | PUT/PATCH | Change informations associated with specified file. | Only for administrators, employees of a dean's office or promoters. |
   | ```file/<int:pk>/``` | DELETE | Delete specified file. | Only for administrators, employees of a dean's office or promoters. |
   | ```record/summary/``` | GET | Return list of students with promoters assigned to them (if student was disqualified, user also see this information). | Only for administrators or employees of a dean's office. |
   | ```record/summary/csv/``` | GET | Export result from row above to .csv file and assign it to logged in user. | Only for administrators or employees of a dean's office. |
   | ```record/revoke/``` | PUT | Disqualify students who didn't send their requests to promoters in actual tour. | Only for administrators or employees of a dean's office. |
   | ```record/status/``` | GET | Return informations about actual status of promoters elections. | Only for logged in users. |
   | ```promoter/record/``` | GET | Return list of students' requests which were sent to promoter in actual tour.  | Only for promoters. |
   | ```promoter/record/<int:pk>/``` | GET | Return informations about specified student's request which was sent to promoter. | Only for promoters. |
   | ```promoter/record/<int:pk>/``` | PUT | Change informations associated with specified student's request (promoter can accept or reject the request).  | Only for promoters. |
   | ```student/record/``` | GET | Return list of requests belonging to student in actual tour. | Only for students. |
   | ```student/record/``` | POST | Send requests to promoters in preference order. | Only for students. |
   | ```student/record/<int:pk>/``` | PUT | Delete association between specified request and chosen promoter. | Only for students. |
   | ```student/record/<int:pk>/promoter/``` | GET | Return list of promoters who still have free places for new students. | Only for students. |
   | ```student/record/<int:pk>/promoter/<int:pk_2>/``` | GET | Return informations about specified promoter and list of his files shared for students. | Only for students. |
   | ```student/record/<int:pk>/promoter/<int:pk_2>/``` | POST | Create association between specified request and chosen promoter | Only for students. |
  
## :hammer: Setup

All you need to do is:
1. Download latest [Python 3.x](https://www.python.org/downloads/) and [Git](https://git-scm.com/) version if you want to get project by using clone command.
2. Open command line interface.
3. Clone this repo to your desktop with ```git clone https://github.com/tmatuszewski97/e-promotor-backend.git```.
4. Now go to the root directory of project and run ```python3 -m venv e-promotor-env``` to create your virtual environment (all necessary packages will be stored here). When you activate your environment by using ```./e-promotor-env/Scripts/activate``` command, you will be able to install project all requirements. Do that by typing ```pip install -r requirements.txt```.
5. Create database for your project. You may want to use free MySQL Community Server, which can be downloaded [here](https://dev.mysql.com/downloads/mysql/). 
6. Create .env file in root directory of project. Use [this sample](.env_dev_sample) and fill created file with all necessary informations.
7. Now type ```python manage.py runserver``` to run Django's development server.
8. That's all! API is ready for testing.

## :page_facing_up: Usage

API is working at this url: https://epromotor.herokuapp.com/
Choose which type of user you want to test and use specified credentials in login form:
- for employee of a dean's office:
  - email: anowak_dziekanat@uwm.pl
  - password: Nowak@123
- for promoter:
  - email: jandrzejczuk@uwm.pl
  - password: Andrzejczuk@4
- for student:
  - email: 145789@uwm.pl
  - password: $JacKot789

Save token received from server and send it in every request's header to authenticate the user. Now feel free to test every given [endpoint](#mag-endpoints).
