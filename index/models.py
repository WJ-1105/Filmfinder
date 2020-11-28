from django.db import models


# Create your models here.


class User(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.login


class User_Movie_rate(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    rate = models.FloatField(default=0)
    integer_rate = models.IntegerField(default=0)


class Movie(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    average_rate = models.FloatField(default=0)
    description = models.TextField()
    genre = models.CharField(max_length=50)
    cast = models.CharField(max_length=50)
    director_name = models.CharField(max_length=50)
    movie_image = models.FileField(upload_to='movie_image/', default='movie_image/default.jpg')

    def __str__(self):
        return self.name


class Review(models.Model):
    id = models.AutoField(primary_key=True)
    movie_id = models.IntegerField()
    user_id = models.IntegerField()
    user_name = models.CharField(max_length=50, default="None")
    rate = models.IntegerField(default=0)
    review_detail = models.TextField()

    def __str__(self):
        return str(self.user_id)


class Bannedlist(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    banneduser_id = models.IntegerField()

    def __str__(self):
        return str(self.user_id)


class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    movie_name = models.CharField(max_length=50, default="None")

    def __str__(self):
        return str(self.user_id)

class History(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField()
    movie_id = models.IntegerField()
    view_time = models.DateTimeField(auto_now = True)

    def __str__(self):
        return str(self.user_id)


class Director(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class Admin(models.Model):
    id = models.AutoField(primary_key=True)
    login = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    email = models.CharField(max_length=50)

    def __str__(self):
        return self.login

## here is one example of creating movie item to database manually
## items can be edited by admin through Django admin derictly and updated 
## to the platform simultaneously

## manually add some movie items in 
'''

m1 = dict(name="Assassin's Creed",average_rate="4.3",
            description="Callum Lynch explores the memories of his ancestor Aguilar de Nerha and gains the skills of a Master Assassin, before taking on the secret Templar society.",
            genre="Action",cast="Michael Fassbender",
            director_name="Justin Kurzel",
            movie_image = "movie_image/Lost.jpg")
mm1 = Movie.objects.get_or_create(**m1)



m2 = dict(name="Ironman",average_rate="4.1",
            description="A simple act of kindness always sparks another, even in a frozen, faraway place. When Smeerensburg's new postman, Jesper, befriends toymaker Klaus, their gifts melt an age-old feud and deliver a sleigh full of holiday traditions.",
            genre="Action",cast="Jason Schwartzman",
            director_name="Sergio Pablos",
            movie_image = "movie_image/ironman.jpeg")
mm2 = Movie.objects.get_or_create(**m2)

m2 = dict(name="Ironman",average_rate="0",
            description="A simple act of kindness always sparks another, even in a frozen, faraway place. When Smeerensburg's new postman, Jesper, befriends toymaker Klaus, their gifts melt an age-old feud and deliver a sleigh full of holiday traditions.",
            genre="Action",cast="Jason Schwartzman",
            director_name="Sergio Pablos",
            movie_image = "movie_image/ironman.jpeg")
mm2 = Movie.objects.get_or_create(**m2)

m3 = dict(name="Ahlat Agaci",average_rate="0",
            description="An unpublished writer returns to his hometown after graduating, where he seeks sponsors to publish his book while dealing with his father's deteriorating indulgence into gambling.",
            genre="Drama",cast="Dogu Demirkol",
            director_name="Nuri Bilge Ceylan",
            movie_image = "movie_image/Green Book.jpg")
mm3 = Movie.objects.get_or_create(**m3)

m4 = dict(name="Booksmart",average_rate="0",
            description="On the eve of their high school graduation, two academic superstars and best friends realize they should have worked less and played more. Determined not to fall short of their peers, the girls try to cram four years of fun into one night.",
            genre="Action",cast="Kaitlyn Dever",
            director_name="Olivia Wilde",
            movie_image = "movie_image/Little_Woman.jpg")
mm4 = Movie.objects.get_or_create(**m4)

'''


