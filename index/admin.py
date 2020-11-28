from django.contrib import admin

# Register your models here.
from .models import User, Movie, Review, Bannedlist, Wishlist, Director, Admin, User_Movie_rate, History


class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'login', 'password', 'email']


class MovieAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'average_rate', 'description', 'genre', 'cast', 'director_name', 'movie_image']


class ReviewAdmin(admin.ModelAdmin):
    list_display = ['id', 'movie_id', 'user_id','user_name', 'rate', 'review_detail']


class BannedlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'banneduser_id']


class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'movie_id']


class DirectorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class AdminAdmin(admin.ModelAdmin):
    list_display = ['id', 'login', 'password', 'email']

class User_Movie_rateAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'movie_id', 'rate']

class HistoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_id', 'movie_id', 'view_time']

admin.site.register(User, UserAdmin)
admin.site.register(Movie, MovieAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Bannedlist, BannedlistAdmin)
admin.site.register(Wishlist, WishlistAdmin)
admin.site.register(Director, DirectorAdmin)
admin.site.register(Admin, AdminAdmin)
admin.site.register(User_Movie_rate, User_Movie_rateAdmin)
admin.site.register(History, HistoryAdmin)
