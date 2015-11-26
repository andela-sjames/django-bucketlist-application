# BucketList-Application/API  [![Coverage Status](https://coveralls.io/repos/andela-sjames/BucketList-Application-API/badge.svg?branch=devdesign&service=github)](https://coveralls.io/github/andela-sjames/BucketList-Application-API?branch=devdesign) [![Build Status](https://travis-ci.org/andela-sjames/BucketList-Application-API.svg?branch=devdesign)](https://travis-ci.org/andela-sjames/BucketList-Application-API)  
#####Demonstrating The Power Of Django and Django Rest Framework.

####__Life is but for a moment, best to take advantage of it with Moments Bucketlist.__  

Moments buckelist is a simple Web App that allows you to create and record moments of your life dreams and prospects, pending when YOU have accomplished them.  

In addition to the Web App, an Application Programmable Interface **(API)** is also available for developers to build on and take advantage of the cool features the Web-service provides.    

#####What cool features ?  

##API Documentation  
You can search for buckelists that contains any particular "string" you pass as query parameters  
__Example__: ``` GET /api/buckelists/?q=boy```  
  
You can also paginate your view via page style.  
__Example__: ``` GET /api/buckecketlists/?page=3```   
  
You can also paginate your view via limits and offset style  
__Example__:``` GET /api/bucketlists/?limit=5&offset=3```  

You can also decide to combine your search and pagination or not!  
__Example__: ``` GET /api/bucketlists/?q=andela&page=2&limit=5&offset=1```  

To register send to the endpoint below your  
```{'username':'myusername','email':'myemail', 'password':'mypassword'}```  
as a json data in the body of your request.  
__Example__: ```  POST /api/user/register/```

To login send to the end point below your request.  
```{'username':'myusername', 'password':'mypassword'}```   

__Example__: ``` POST /api/auth/login/```  
Get a Token and you make calls to the protected endpoints..   

__Note__: For clients to authenticate, the token key should be included in the ```Authorization``` HTTP header. The key should be prefixed by the string literal "Token", with whitespace separating the two strings.  
__For example__:```Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b ```  

Enjoy!  
  
For other methods available and how to use them please view
our api documentation  
via this link [API Docs](https://moments-bucketlist.herokuapp.com/docs/)  

## The Project  
This Project is hosted live on herokuapp where you can signup and begin your moments. [Sign Up](https://moments-bucketlist.herokuapp.com/) 

Built using Django and Django Rest framework, frameworks of Python programmimg Language shows how powerful the language can be if used effectively.  

##Application Explained.  

* User sign's up for a wonderful experience.  
* User sign's in after Sign up.  
* User creates a bucketlist and a bucketlist item.  
* User can choose to add an item to an existing bucketlist.  
* User can view existing buckelist.  
* User can Edit existing bucketlist.  
* User can view existing buckelist items.    
* User can Edit existing bucketlist items.  
* User can Update or delete existing buckelist.  
* User can Update or delete existing buckelist items.    
* User can search for bucketlist.  
* User can mark a bucketlist item as done if he/she has done it.  

##Build Locally  
To build this project you will need to have git and python  
installed on your local machine. [Python](https://www.python.org/downloads/), [Git](https://git-scm.com/downloads). Once insatlled  

1. Make a directory for the project. ``` mkdir project```  
2. Change directory to project ``` cd project``` and 
3. Clone this repository using ``` git clone [repo_url]```   
4. Get a virtual environment up using ``` virtualenv my_environment```  
5. Install all requirements needed for project to run ``` pip install -r requirements.txt```  
6. Change directory to project ``` cd BuckelistApp```  
7. Be sure to have a postgress database setup by creating a ```.env.yml``` file and add it to your ``` root``` file, have the following ```config``` in the ```.env.yml``` file.  
8. Set your Database name to : ```BucketlistApp``` on your pgAdmin
9. Be certain you are in the BucketlistApp dir and run ``` python manage.py runserver```.


__.env.yml format:__  

 ```
    SECRET_KEY:  
      'some-random-crazy-value'
    DB_USER:
      'Your Db username'
    DB_PASSWORD:
      'Your Db pssword'
```   
    


Have Fun!



