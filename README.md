
The steps to build, setup, configure, and use your system and functionalities. 


1. Download the filmfinder folder to the Desktop.

2. Download Django:
pip install django==3.1.3

3. Enter into the project file.

4. Migrate database once changing environment/database by using:
python manage.py makemigrations 
python manage.py migrate

5. Run server and access into film finder website by using this command:
python manage.py runserver

6. Go to a browser (recommend to use google chrome if available) and enter the address http://127.0.0.1:8000/ (If a different port is used, change 8000 to correct corresponding port number, the default port is 8000).

7. There are two methods to add movie items in database:
  <1>. Add movies by using python shell through terminal following the command below:
       python manage.py shell 
       from index.models import *
  m1 = dict(name="Assassin's Creed",average_rate="0",
              description="Callum Lynch explores the memories of his ancestor Aguilar de Nerha and gains the skills of a Master Assassin, before taking on the secret Templar society.",
              genre="Action",cast="Michael Fassbender",
              director_name="Justin Kurzel",
              movie_image = "movie_image/Lost.jpg")
  mm1 = Movie.objects.get_or_create(**m1)

  m2 = dict(name="Ironman",average_rate="0",
              description="A simple act of kindness always sparks another, even in a frozen, faraway place. When Smeerensburg's new postman, Jesper, befriends toymaker Klaus, their gifts melt an age-old feud and deliver a sleigh full of holiday traditions.",
              genre="Action",cast="Jason Schwartzman",
              director_name="Sergio Pablos",
              movie_image = "movie_image/ironman.jpeg")
  mm2 = Movie.objects.get_or_create(**m2)

 
  <2>. Add movies in Django Administration through website directly
  python manage.py createsuperuser
  Then type http://127.0.0.1:8000/admin go to Django admin page, click the movies tuple under index section, press add button to add movie.









