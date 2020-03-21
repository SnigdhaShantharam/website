# App name: website

# Step 1: Clone this repository and
   $ cd website
# Step 2: Build Docker image        
        #make sure you navigate to the project directory where the dockerfile is present     
   $ docker build .
          (or)
   $ sudo docker build .
# Step 3: Build the docker image the docker-compose configuration
   $ docker-compose build
          (or)
   $ sudo docker-compose build
# Step 4: Creating a Django project using the docker image
   
   # Running commands using docker-compose
   $ docker-compose run website sh -c "django-admin.py startproject website ."
                        (or)
   $ sudo docker-compose run website sh -c "django-admin.py startproject website ."
