from sqlite3 import IntegrityError
from django.shortcuts import render, redirect

from .models import Posts, Habbits, HabbitsTracker, Motivations, UsersList, Comments, Likes
from django.contrib.sessions.backends.base import SessionBase
from django.db import connections

from datetime import datetime



# Create view
# Get and display Posts
session = SessionBase()
def checkLogin():
    if  'user_id' not in session or  'user_Name' not in session: 
        return False
    return True

# handling register
def register(request):
    context = {}
    if request.method =='POST':
        fname      = request.POST.get('fname')
        lname      = request.POST.get('lname')
        occupation = request.POST.get('occupation')
        uname      = request.POST.get('uname')
        email      = request.POST.get('email')
        password   = request.POST.get('password')

        try:
            add_user= UsersList(first_name = fname,last_name=lname,occupation = occupation,user_name = uname, email=email,password=password)
            add_user.save()
            return redirect(login)
        except IntegrityError:
            context = {'message':'Data is not saved!'}

    return render(request,'register.html',context)


def index(request):
    # Check Auth
    if not checkLogin():
        return redirect(login)
    user_id = session['user_id']

    posts_lists = Posts.objects.raw('''SELECT p.post_id, p.publish_date as post_date, p.content as post_content, u.user_name as post_user,l.like_value as like_value, li.number_of_likes as number_of_likes
                                            FROM posts as p
                                            left JOIN users_list as u ON p.user_id=u.user_id 
                                            left JOIN (SELECT post_id, user_id, like_value from likes where user_id=%s) as l on p.post_id=l.post_id
                                            LEFT JOIN (SELECT post_id, COUNT(like_value) as number_of_likes from likes WHERE like_value=1 group by post_id) as li on p.post_id=li.post_id
                                            ORDER BY p.publish_date DESC LIMIT 10''', [user_id])

    comments_lists = Comments.objects.raw('''SELECT c.comment_id, c.post_id, c.publish_date as comment_date, c.content as comment_content, u.user_name as comment_user
                                                FROM comments as c
                                                JOIN users_list as u ON c.user_id=u.user_id''')

    likes_lists = Likes.objects.raw('''SELECT * FROM likes WHERE user_id=%s''',[user_id])
    
    context = {'posts': posts_lists, 'comments': comments_lists, 'likes': likes_lists}
    return render(request,'habits/index.html',context)


# handling dislikes

def dislike(request, post_id):
    # Check Auth
    if not checkLogin():
        return redirect(login)

    user_id = session['user_id']
    cursor = connections['default'].cursor()
    #  update
    cursor.execute('''DELETE FROM likes
                        WHERE post_id=%s and user_id=%s''', [post_id, user_id])

    cursor.execute('''INSERT INTO likes (post_id, user_id, like_value)
                        VALUES (%s,%s,0)''', [post_id, user_id])
    return redirect(index)

# handling likes

def like(request, post_id):
    # Check Auth
    if not checkLogin():
        return redirect(login)

    user_id = session['user_id']
    cursor = connections['default'].cursor()
    #  update
    cursor.execute('''DELETE FROM likes
                        WHERE post_id=%s and user_id=%s''', [post_id, user_id])

    cursor.execute('''INSERT INTO likes (post_id, user_id, like_value)
                        VALUES (%s,%s,1)''', [post_id, user_id])

    return redirect(index)

# handling comments
def add_comment_submission(request):
     # Check Auth
    if not checkLogin():
        return redirect(login)

    if request.method == "POST":
        
        content = request.POST["content"]
        post_id = request.POST["post_id"]
        user_id = session['user_id']
        date = datetime.now().strftime("%Y-%m-%d %H:%M")

        cursor = connections['default'].cursor()
        # insert
        cursor.execute('''INSERT INTO comments (post_id, user_id, publish_date, content)
                        VALUES (%s, %s, %s, %s)''', [post_id, user_id, date, content])
        
    return redirect('/habits')

# handling login
def login(request):
    context = {}
    if request.method =='POST':
        email    = request.POST.get('email')
        password = request.POST.get('password')
        users = UsersList.objects.filter(email=email, password=password).first()
      
        if not users:
            context = {'message':'wrong email or password'}
        else:
            session['user_id']   = users.user_id
            session['user_Name'] = users.user_name
           
            print(session)
            print( session['user_Name'])
            return redirect(index)
    
    return render(request, 'login.html',context)

# handling logout
def logout(request):
    session.clear()
    return redirect(login)

# Track habbits progress
def add_progress(request):
     # Check Auth
    if not checkLogin():
        return redirect(login)

    user_id = session['user_id']
    habits_list = Habbits.objects.raw('''SELECT * FROM habbits WHERE user_id = %s''',[user_id])
    context = {'habits': habits_list}
    return render(request, 'habits/add_progress.html', context)

# handling logging habbits
def add_progress_submission(request):
     # Check Auth
    if not checkLogin():
        return redirect(login)

    if request.method == "POST":
        
        habit_id = request.POST["selected_habit"]
        amount = request.POST["amount"]
        date = request.POST["date"]

        cursor = connections['default'].cursor()
        # insert
        cursor.execute('''INSERT INTO habbits_tracker (habbit_id, habbit_type, date, yes_no_value, success_amount_value)
                        VALUES (%s, %s, %s, %s, %s)''', [habit_id, 1, date, None, amount])


        # adding post to the database
        if request.POST["post"] is not None:
            content = request.POST["post"]
            user_id = session['user_id']
            date = datetime.now().strftime("%Y-%m-%d %H:%M")

            cursor = connections['default'].cursor()
            # insert
            cursor.execute('''INSERT INTO posts (user_id, publish_date, content)
                            VALUES (%s, %s, %s)''', [user_id, date, content])
        

        return redirect('/habits')
    return redirect('/habits/add_progress')


# My Habits page
def my_habits(request):
     # Check Auth
    if not checkLogin():
        return redirect(login)

    user_id = session['user_id']
    habits_list = Habbits.objects.raw('''SELECT * FROM habbits WHERE user_id = %s''',[user_id])
    context = {'habits': habits_list}
    return render(request, 'habits/my_habits.html',context)

# Motivations page
def motivations(request):
    # Check Auth
    if not checkLogin():
        return redirect(login)

    user_id = session['user_id']
    motivations_list = Motivations.objects.raw('''SELECT * FROM motivations WHERE user_id = %s''',[user_id])
    context = {'motivations': motivations_list}
    return render(request,'habits/motivations.html',context)

# handling new motivations
def add_motivation_submission(request):
    # Check Auth
    if not checkLogin():
        return redirect(login)

    if request.method == "POST":
        
        user_id = session["user_id"]
        motivation_desc = request.POST["motivation"]

        cursor = connections['default'].cursor()
        # get next id
        cursor.execute('''INSERT INTO motivations (user_id, motivation_desc)
                        VALUES (%s,%s)''', [user_id, motivation_desc])
        
    return redirect('/habits/motivations')

# Adding habits
def add_habit(request):
    # Check Auth
    if not checkLogin():
        return redirect(login)

    return render(request, 'habits/add_habit.html')

# Handle adding habits
def add_habit_submission(request):
     # Check Auth
    if not checkLogin():
        return redirect(login)

    if request.method == "POST":
        
        user_id = session["user_id"]
        habit_desc = request.POST["habit_desc"]
        habit_name = request.POST["habit_name"]
        success_activity = request.POST["success_activity"]
        success_range = request.POST["success_range"]
        success_amount = request.POST["success_amount"]
        success_unit = request.POST["success_unit"]
        habit_days_target = request.POST["habit_days_target"]

        cursor = connections['default'].cursor()
        # insert
        cursor.execute('''INSERT INTO habbits (user_id, habbit_type, habbit_desc, habbit_name, 
                                                        habbit_days_target, success_activity, success_range, 
                                                        success_amount, success_unit)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)''', [user_id, 1, habit_desc, habit_name, 
                                                                                habit_days_target, success_activity, success_range,
                                                                                success_amount, success_unit])
        
        return redirect('/habits')
    return redirect('/habits/add_habit')

