# BucketList-Application-API  [![Coverage Status](https://coveralls.io/repos/andela-sjames/BucketList-Application-API/badge.svg?branch=devdesign&service=github)](https://coveralls.io/github/andela-sjames/BucketList-Application-API?branch=devdesign)  
#####Demonstrating The Power Of Django and Django Rest Framework.

####__Life is but for a moment, best to take advantage of it with Moments Bucketlist.__  

__Moments buckelist is a simple Web App that allows you to create and record moments of your life dreams and prospects, pending when YOU have accomplished them.__  

__In addition to the Web App, an Application Programmable Interface **(API)** is also available for developers to build on and take advantage of the cool features the Web-service provides.__    

#####What cool features ?  

##API Documentation  
You can search for buckelists that contains any particular "string" you pass as query parameters  
__example__: ``` GET /api/buckelists/?q=boy```  
  
You can also paginate your view via page style.  
__example__: ``` GET /api/buckecketlists/?page=3```   
  
You can also paginate your view via limits and offset style  
__example__:``` GET /api/bucketlists/?limit=5&offset=3```  

You can also decide to combine your search and pagination or not!  
__example__: ``` GET /api/bucketlists/?q=andela&page=2&limit=5&offset=1```  

Have it your way!  
  
For other methods available and how to use them please view
our api documentation  
via this link [API Docs](https://moments-bucketlist.herokuapp.com/docs/)  

## The Project  
This Project is hosted live on herokuapp where you can signup and begin your moments. [Sign Up](https://moments-bucketlist.herokuapp.com/) 

Built using Django and Django Rest framework, frameworks of Python programmimg Language shows how powerful the language can be if used effectively.  

##Application Explained.  

* User Sign's up for a wonderful experience.  
* User Sign's in after Sign up.  
* User Creates a bucketlist and a bucketlist item.  
* User Can choose to add an item to an existing bucketlist.  
* User can view existing buckelist.  
* User can Edit existing bucketlist.  
* User can view existing buckelist items.    
* User can Edit existing bucketlist items.  
* User can Update or delete existing buckelist.  
* User can Update or delete existing buckelist items.    
* User can search for bucketlist.  
* User can mark a bucketlist item as done if he/she has done it.  

