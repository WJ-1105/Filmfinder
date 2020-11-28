from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.http import HttpResponse
from index.models import Movie, Review ,Bannedlist , User_Movie_rate,Wishlist, History
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, Q
from django.utils.datastructures import MultiValueDictKeyError

import numpy as np




# Create your views here.

def index(request):
    Movie_list = Movie.objects.all()

    rate_integer = []
    for each_movie in Movie_list:
        rate_integer.append(int(each_movie.average_rate))
    # Do something for anonymous users.
    context = {'value': Movie_list,'rate_integer' : rate_integer}
    return render(request, 'index/home.html', context)



@login_required
def profile(request, profile_user):
    own_profile = 0
    if request.user.username == profile_user:
        own_profile = 1


    #######Banlist
    ban = Bannedlist.objects.filter(user_id=request.user.id)
    already_banned = 0
    profile_user_id = User.objects.get(username=profile_user).id

    for each_banned_user in ban:
        if each_banned_user.banneduser_id == profile_user_id:
            already_banned = 1

    ###### WishList
    wish = Wishlist.objects.filter(user_id=request.user.id)


    if request.method == 'GET':
        profile_user_ban_list = Bannedlist.objects.filter(user_id=profile_user_id)
        profile_user_ban_list_name = []
        for each_user in profile_user_ban_list:
            name = User.objects.get(id=each_user.banneduser_id).username
            profile_user_ban_list_name.append(name)
        return render(request, 'index/profile.html',{"current_user":request.user, "profile_user" : profile_user,
                                                     "check_if_own_profile" : own_profile,"check_already_banned": already_banned,
                                                     "profile_user_ban_list":profile_user_ban_list_name,
                                                     "profile_user_id":profile_user_id,"wish":wish})
    elif request.method == 'POST':

        if already_banned == 0:
            ban_user = request.POST['ban_user']
            # ban_user = request.POST.get('ban_user', False)
            Bannedlist_tuple = Bannedlist()
            Bannedlist_tuple.user_id = request.user.id
            Bannedlist_tuple.banneduser_id = ban_user
            Bannedlist_tuple.save()


            profile_user_ban_list = Bannedlist.objects.filter(user_id=profile_user_id)
            profile_user_ban_list_name = []
            for each_user in profile_user_ban_list:
                name = User.objects.get(id=each_user.banneduser_id).username
                profile_user_ban_list_name.append(name)

            return render(request, 'index/profile.html', {"current_user": request.user, "profile_user": profile_user,
                                                          "check_if_own_profile": own_profile,
                                                          "check_already_banned": 1,
                                                          "profile_user_ban_list": profile_user_ban_list_name,
                                                          "profile_user_id":profile_user_id,"wish":wish})
        elif already_banned == 1:
            banned_user = request.POST['ban_user']
            # banned_user = request.POST.get('ban_user', False)

            ban_list = Bannedlist.objects.filter( user_id = request.user.id, banneduser_id=banned_user)
            for each in ban_list:
                each.delete()
            # already_banned = 0

            profile_user_ban_list = Bannedlist.objects.filter(user_id=profile_user_id)
            profile_user_ban_list_name = []
            for each_user in profile_user_ban_list:
                name = User.objects.get(id=each_user.banneduser_id).username
                profile_user_ban_list_name.append(name)

            return render(request, 'index/profile.html', {"current_user": request.user, "profile_user": profile_user,
                                                          "check_if_own_profile": own_profile,
                                                          "check_already_banned": 0,
                                                          "profile_user_ban_list": profile_user_ban_list_name,
                                                          "profile_user_id":profile_user_id,"wish":wish})

@login_required
def detail(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    review = Review.objects.filter(movie_id=movie_id)
    rate = User_Movie_rate.objects.filter(user_id=request.user.id, movie_id=movie_id)[:1]
    genre = Movie.objects.get(id = movie_id).genre
    director = Movie.objects.get(id = movie_id).director_name

    ####### recodmandation
    user_history = History.objects.filter(user_id=request.user.id)
    history_movie_id_list = []
    for each_history in user_history:
        history_movie_id_list.append(each_history.movie_id)

    all_same_genre = Movie.objects.filter(genre = genre)
    reviewed_same_genre = all_same_genre.filter(id__in = history_movie_id_list)[:8]

    all_same_director = Movie.objects.filter(director_name = director)
    reviewed_same_director = all_same_director.filter(id__in = history_movie_id_list)[:8]




    ########### wish list##########

    wish = Wishlist.objects.filter(user_id=request.user.id)
    already_wished = 0

    for each_wish in wish:
        if each_wish.movie_id == int(movie_id):
            already_wished = 1
            break

    banlistuser = Bannedlist.objects.filter(user_id=request.user.id)
    banlistuserarray = []

    for each_user in banlistuser:
        banlistuserarray.append(each_user.banneduser_id)

    filtered_review = review.exclude(user_id__in = banlistuserarray)

    #########Some popular movie######
    some_popular_movie = Movie.objects.all().order_by('-average_rate')[:5]


    if request.method == 'GET':
        # movie = get_object_or_404(Movie, pk=movie_id)
        # review = Review.objects.filter(movie_id=movie_id)
        # if request.user.is_authenticated():
        # Do something for authenticated users.

        # else   (????????????detail????????detail???????????? ????????)

        allhistory = History.objects.filter(user_id=request.user.id , movie_id = movie_id)
        if allhistory.count() == 0:
            history_tuple = History()
            history_tuple.user_id = request.user.id
            history_tuple.movie_id = movie_id
            history_tuple.save()
        else:
            update_history_tuple = History.objects.get(user_id=request.user.id , movie_id = movie_id)
            update_history_tuple.user_id = request.user.id
            update_history_tuple.movie_id = movie_id
            update_history_tuple.save()

        return render(request, 'index/detail.html', {"movie": movie, "review": filtered_review,
                                                     "current_user": request.user, "rates":rate,"already_wished":already_wished,
                                                     'reviewed_same_genre':reviewed_same_genre,
                                                     'reviewed_same_director':reviewed_same_director,
                                                     'some_popular_movie' : some_popular_movie})
    elif request.method == 'POST':
        if 1 < 2:
            if 'rating' in request.POST and 'review' in request.POST:
                user_rating = request.POST['rating']
                user_review = request.POST['review']
                review_tuple = Review()
                review_tuple.user_id = request.user.id
                review_tuple.user_name = request.user.username
                review_tuple.movie_id = movie_id
                review_tuple.rate = user_rating
                review_tuple.review_detail = user_review
                review_tuple.save()

                ### Update average_rate of movie
                avg = Review.objects.filter(movie_id=movie_id, user_id=request.user.id).aggregate(Avg('rate'))
                Movie.objects.filter(id=movie_id).update(average_rate = avg['rate__avg'])
                result, integer_result, all_movie_sequence = update_private_average_rate(Movie.objects.all(),request.user.id)
                banlistuser = Bannedlist.objects.filter(user_id=request.user.id)
                banlistuserarray = []

                for each_user in banlistuser:
                    banlistuserarray.append(each_user.banneduser_id)

                filtered_review = review.exclude(user_id__in=banlistuserarray)
                return render(request, 'index/detail.html', {"movie": movie, "review": filtered_review, "current_user": request.user,
                                                             "review_success": "Thank you for your review", "rates":rate,
                                                             "already_wished":already_wished,
                                                            'some_popular_movie' : some_popular_movie})

            # result, integer_result, all_movie_sequence = update_private_average_rate(Movie.objects.all(),request.user.id)
            # all_movie_sequence_list = list(all_movie_sequence)
            # temp = all_movie_sequence_list.index(movie_id)


            ############ Handle wish List##########
            if 'wish_movie' in request.POST:
                if already_wished == 0:
                    movie_idd = request.POST['wish_movie']
                    # ban_user = request.POST.get('ban_user', False)
                    wishlist_tuple = Wishlist()
                    wishlist_tuple.user_id = request.user.id
                    wishlist_tuple.movie_id = movie_id
                    wishlist_tuple.movie_name = Movie.objects.get(id=movie_id).name
                    wishlist_tuple.save()

                    return render(request, 'index/detail.html', {"movie": movie, "review": filtered_review,
                                                                 "current_user": request.user, "rates": rate,
                                                                 "already_wished": 1,
                                                                  'some_popular_movie' : some_popular_movie})
                elif already_wished == 1:
                    # banned_user = request.POST['ban_user']
                    # banned_user = request.POST.get('ban_user', False)

                    wished_list = Wishlist.objects.filter(user_id=request.user.id, movie_id=movie_id)
                    for each in wished_list:
                        each.delete()
                    # already_banned = 0


                    return render(request, 'index/detail.html', {"movie": movie, "review": filtered_review,
                                                                 "current_user": request.user, "rates": rate,
                                                                 "already_wished": 0,
                                                                'some_popular_movie' : some_popular_movie})

def login(request):
    if request.method == 'GET':
        return render(request, 'index/login.html')
    elif request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=user_name, password=password)
        if user is None:
            return render(request, 'index/login.html', {'error': 'The username or password is wrong'})
        else:
            auth.login(request, user)
            # Movie_list = Movie.objects.all()
            # context = {'value': Movie_list,'you': user_name }

            #####这里需要改成reverse
            # return render(request, 'index/homeLogin.html', context)
            # return redirect('homelogin_page')
            homelogin_page = reverse('homelogin_page', kwargs={'you': user_name})
            return redirect(homelogin_page)


def signup(request):
    if request.method == 'GET':
        return render(request, 'index/register.html')
    elif request.method == 'POST':
        user_name = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']
        try:
            User.objects.get(username=user_name)
            return render(request, 'index/register.html', {'error': 'username already exist'})
        except User.DoesNotExist:
            if password == password2:
                User.objects.create_user(username=user_name, password=password)
                return redirect('login_page')
            else:
                return render(request, 'index/register.html', {'password_different': 'Confirmed password incorrect'})


def update_private_average_rate(Movie_list,me):
    ban = Bannedlist.objects.filter(user_id=me)
    ban_list = []
    for each_banned_user in ban:
        ban_list.append(each_banned_user.banneduser_id)

    review_user = Review.objects.filter()
    all = []
    for each_user in review_user:
        all.append(each_user.user_id)

    not_bannned_list = list(set(ban_list) ^ set(all))
    re = []
    all_movie_sequence = []
    for each_movie in Movie_list:
        small_sum = 0
        small_count = 0
        all_movie_sequence.append(each_movie.id)
        for each_user in not_bannned_list:
            sum = Review.objects.filter(movie_id=each_movie.id, user_id=each_user).aggregate(Sum('rate'))
            count = Review.objects.filter(movie_id=each_movie.id, user_id=each_user).count()
            if sum['rate__sum'] is not None:
                small_sum = small_sum + sum['rate__sum']
            small_count = small_count + count

        re.append([small_sum, small_count])

    result = []
    for each in re:
        if each[1] == 0:
            result.append(0)
        else:
            temp = (each[0]) / each[1]
            result.append(temp)

    integer_result = []
    for each in result:
        integer_result.append(int(each))

    i = 0
    for each_movie in Movie_list:
        num_results = User_Movie_rate.objects.filter(user_id = me, movie_id = each_movie.id).count()
        if num_results == 0:
            User_Movie_rate_tuple = User_Movie_rate()
            User_Movie_rate_tuple.user_id = me
            User_Movie_rate_tuple.movie_id = each_movie.id
            User_Movie_rate_tuple.rate = result[i]
            User_Movie_rate_tuple.integer_rate = integer_result[i]
            User_Movie_rate_tuple.save()

        else:
            User_Movie_rate.objects.filter(user_id = me,movie_id = each_movie.id).update(rate = result[i])
            User_Movie_rate.objects.filter(user_id = me,movie_id = each_movie.id).update(integer_rate = integer_result[i])


        i = i + 1

    return result, integer_result,all_movie_sequence

@login_required
def homelogin(request, you):
    # userr = User.objects.get(username=you)
    Movie_list = Movie.objects.all()
    result ,integer_result,all_movie_sequence = update_private_average_rate(Movie_list,request.user.id)


    movie_list_array = []

    for each_movie in Movie_list:
        temp = []
        rate = User_Movie_rate.objects.get(user_id=request.user.id,movie_id=each_movie.id)
        temp.append(each_movie)
        temp.append(rate.rate)
        temp.append(rate.integer_rate)
        temp.append(Movie.objects.get(id=each_movie.id).name)
        movie_list_array.append(temp)
    movie_list_array = sorted(movie_list_array, key=lambda x: (-x[1], x[3]))


    if request.method == 'GET':
        return render(request, 'index/homeLogin.html', {"you": request.user, "movie_list_array":movie_list_array})


    elif request.method == 'POST':
        search_input = request.POST['search_input']
        name_result = Movie.objects.filter(name__icontains=search_input)
        genre_result = Movie.objects.filter(genre__icontains=search_input)
        description_result = Movie.objects.filter(description__icontains=search_input)
        director_result = Movie.objects.filter(director_name__icontains=search_input)
        if name_result.count() == 0 and genre_result.count() == 0 and description_result.count() == 0 and director_result.count() == 0:
            # Movie_list = Movie.objects.all()
            return render(request, 'index/homeLogin.html',{"you": request.user, "error":"No result found"})
        else:
            temp_result = set(name_result).union(set(genre_result))
            searched_result1 = set(temp_result).union(set(description_result))
            searched_result2 = set(searched_result1).union(set(director_result))
            searched_rate = []

            movie_list_array = []
            for each_movie in searched_result2:
                temp = []
                rate = User_Movie_rate.objects.get(user_id=request.user.id, movie_id=each_movie.id)
                temp.append(each_movie)
                temp.append(rate.rate)
                temp.append(rate.integer_rate)
                temp.append(Movie.objects.get(id=each_movie.id).name)
                movie_list_array.append(temp)

            movie_list_array = sorted(movie_list_array, key=lambda x: (-x[1], x[3]))


            # for each in searched_result2:
            #     all_movie_sequence_list = list(all_movie_sequence)
            #     temp = all_movie_sequence_list.index(each.id)
            #     searched_rate.append(result[temp])



            return render(request, 'index/homeLogin.html',{"you": request.user,'movie_list_array':movie_list_array})




def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return redirect('index_page')
