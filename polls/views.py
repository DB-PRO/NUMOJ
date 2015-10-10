from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .models import Problem, Tag, News

# form .models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.db import connection

def index(request):
    latest_problem_list = Problem.objects.order_by('id')
    User_list = User.objects.order_by('id')
    Tag_list = Tag.objects.order_by('id')
    News_list = News.objects.order_by('id')
    member_id = request.session['member_id']
    
    add_Tag = False;

    user = User.objects.get(id = member_id)
    if user is not None:
        add_Tag = user.has_perm("add_Tag")

    context = {'latest_problem_list': latest_problem_list,
               'User_list': User_list, 'Tag_list': Tag_list, 
               'member_id': member_id, 'News_list': News_list,
               'add_Tag': add_Tag}
    

    return render(request, 'polls/home.html', context)


def view_login(request):
    flag = False
    
    request.session['member_id'] = 0
    logout(request)

    if request.method == 'POST':
        username = request.POST['name']
        password = request.POST['password']
        user = authenticate(username=username, password = password)
        user1 = user
        if user is not None:
            login(request, user)
            request.session['member_id'] = user.id
            return HttpResponseRedirect('/polls/home')
        
        else:
            flag = True;
            request.session['member_id'] = 0

    request.session['member_id'] = 0;
    context = {'flag': flag, 'member_id': 0}
    return render(request, 'polls/login.html', context)


def problem(request, problem_id):
    member_id = request.session['member_id']
    problem = get_object_or_404(Problem, id = problem_id)
    return render(request, 'polls/problem.html', {'problem': problem, 'member_id': member_id})


def user(request, user_id):
    user = get_object_or_404(User, id = user_id)
    return render(request, 'polls/user_submission.html', {'user': user})


def createTag(request):
    return render(request, 'polls/createTag.html', {})


def createTagAction(request):
    name = request.POST['TagName']
    a = Tag(tagName = name)
    a.save()

    Tag_list = Tag.objects.order_by('id')
    context = {'Tag_list': Tag_list, 'name': name}
    
    return render(request, 'polls/createdTagResult.html', context)


def createUser(request):
    return render(request, 'polls/createUser.html', {})


def createUserAction(request):
    fname = request.POST['firstName']
    lname = request.POST['lastName']
    pword = request.POST['password']
    e = request.POST['email']
    s = request.POST['sex']
    
    a = User(firstName = fname, lastName = lname, password = pword,
             email = e, sex = s)
    a.save()
    
    User_list = User.objects.order_by('id')
    context = {'User_list': User_list, 'fname': fname}
    
    return render(request, 'polls/createdUserResult.html', context)


def createProblem(request):
    return render(request, 'polls/createProblem.html', {})


def createProblemAction(request):
    name = request.POST['name']
    st = request.POST['statement']
    i = request.POST['input']
    o = request.POST['output']
    t = request.POST['timelimit']
    e = request.POST['extra']
    a = Problem(problemName = name, problemStatement = st, timelimit = float(t), input = i, output = o,
                extraInformation = e)
    a.save()
    
    problem_list = Problem.objects.order_by('id')
    context = {'Problem_list': problem_list, 'problemName': name}
    
    return render(request, 'polls/createdProblemResult.html', context)


def problems(request):
    latest_problem_list = Problem.objects.order_by('id')
    member_id = request.session['member_id']
    user = User.objects.get(id = member_id)
    add_problem = False
    if user is not None:
        add_problem = user.has_perm("add_problem")
    context = {'latest_problem_list': latest_problem_list, 'member_id': member_id, 'add_problem': add_problem}
    
    return render(request, 'polls/problems.html', context)


def rank(request):
    def dictfetchall(cursor): 
        "Returns all rows from a cursor as a dict" 
        desc = cursor.description 
        return [
                dict(zip([col[0] for col in desc], row)) 
                for row in cursor.fetchall() 
        ]

    cursor = connection.cursor()
    cursor.execute("select * from rank")
    result = dictfetchall(cursor)
    member_id = request.session['member_id']

    context = {'rank_list': result, 'member_id': member_id}
    
    return render(request, 'polls/rank.html', context)


def submit(request):
    return render(request, 'polls/submit.html', {'member_id': member_id})


def submitAction(request):
    fname = request.POST['firstName']
    lname = request.POST['lastName']
    pword = request.POST['password']
    e = request.POST['email']
    s = request.POST['sex']
    
    a = User(firstName = fname, lastName = lname, password = pword,
             email = e, sex = s)
    a.save()
    
    User_list = User.objects.order_by('id')
    context = {'User_list': User_list, 'fname': fname}
    
    return render(request, 'polls/createdUserResult.html', context)
