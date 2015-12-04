from django.shortcuts import render

# Create your views here.

from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader
from .models import Problem, Tag, News, Submission

# form .models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.core.urlresolvers import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Permission
from django.db import connection
import random

def index(request):
    problem_list = Problem.objects.order_by('id')[:10]
    User_list = User.objects.order_by('id')
    Tag_list = Tag.objects.order_by('id')
    News_list = News.objects.order_by('id')

    if not request.session.get('member_id', None):
        return HttpResponseRedirect('/polls/login')
        request.session['member_id'] = 0

    member_id = request.session['member_id']
    
    add_Tag = False;

    user = User.objects.get(id = member_id)
    if user is not None:
        add_Tag = user.has_perm("add_Tag")

    context = {'problem_list': problem_list,
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
    top_rank_list = get_rank(0)
    return render(request, 'polls/problem.html', {'problem': problem, 'member_id': member_id, 'top_rank_list':top_rank_list})


def user(request, user_id):
    user = get_object_or_404(User, id = user_id)
    member_id = request.session['member_id']
    top_rank_list = get_rank(0)
    return render(request, 'polls/user.html', {'user': user, 'member_id': member_id, 'top_rank_list': top_rank_list})


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

'''
for i in range(1, 100000):
    name = "problem " + str(i)
    st = "statement"
    i = "input"
    o = "output"
    t = 1.0
    e = "extraInformation"
    a = Problem(problemName = name, problemStatement = st, timelimit = float(t), input = i, output = o, extraInformation = e)
    a.save()

for i in range(2, 100):
    p = Problem.objects.get(id = random.randint(10, 100))
    u = User.objects.get(id = random.randint(2, 105))
    x = random.randint(1, 100)
    st = 'WA'
    if (x < 50): st = "TLE"
    if (x == 1): st = "AC"
    Submission(user = u, problem = p, status = st)
    Submission.save()    
'''

def get_rank(n):
    def dictfetchall(cursor): 
        desc = cursor.description 
        return [
            dict(zip([col[0] for col in desc], row)) 
            for row in cursor.fetchall()
        ]

    cursor = connection.cursor()
    if n != 0:
        cursor.execute("SELECT * FROM rank1")
    else:
        cursor.execute("SELECT * FROM rank1 LIMIT 10")
    result = dictfetchall(cursor)
    return result


def rank(request):
    result = get_rank(1)

    if not request.session.get('member_id', None):
        request.session['member_id'] = 0
    member_id = request.session['member_id']

    context = {'rank_list': result, 'member_id': member_id}
    
    return render(request, 'polls/rank.html', context)


def submit(request):
    top_rank_list = get_rank(0)
    return render(request, 'polls/submit.html', {'member_id': request.session['member_id'], 'top_rank_list': top_rank_list})

def submitAction(request):

    user = User.objects.get(id = request.session['member_id'])

    problemId = request.POST['problemId']
    problem = Problem.objects.get(id = problemId)
    l = request.POST['lang']
    
    ran = random.randint(1, 3)
    status = "Accepted";
    if ran == 2:
        status = 'Time limit exceeded'
    if ran == 3:
        status = 'Wrong answer'

    a = Submission(user = user, problem = problem, Language = l, status = status)
    a.save()
    
    return HttpResponseRedirect('/polls/home')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

def problems(request, page):
    problem_list = Problem.objects.order_by('id')
    paginator = Paginator(problem_list, 20) 

    if not request.session.get('member_id', None):
        request.session['member_id'] = 0
    member_id = request.session['member_id']

    try:
        problem_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        problem_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        problem_list = paginator.page(paginator.num_pages)

    pTag = []
    for x in problem_list:
        pTag.append(x.tag.all())

    pages = []
    for i in range(1, problem_list.paginator.num_pages + 1):
        if problem_list.paginator.num_pages == problem_list.number and i == problem_list.number - 1:
            pages.append(0)            
        elif 1 == problem_list.number and i == problem_list.number + 2:
            pages.append(0)
        if i <= 2: 
            pages.append(i)
        elif problem_list.paginator.num_pages - i <= 1:
            pages.append(i)
        elif abs(i - problem_list.number) <= 1:
            if problem_list.number - i == 1 and problem_list.number - 2 != 2:
                pages.append(0)
            pages.append(i)
            if i - problem_list.number == 1 and problem_list.number != problem_list.paginator.num_pages - 3:
                pages.append(0)

    list = zip(problem_list.object_list, pTag)
    return render(request, 'polls/problems.html', {'list': list, 'pTag': pTag, 'member_id': request.session['member_id'], 'top_rank_list': get_rank(0), "problem_list": problem_list, "pages": pages})


def tag(request, tag_id, page):
    t = Tag.objects.filter(id = tag_id)
    problem_list = Problem.objects.filter(tag = t)
    paginator = Paginator(problem_list, 20) 

    if not request.session.get('member_id', None):
        request.session['member_id'] = 0
    member_id = request.session['member_id']

    try:
        problem_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        problem_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        problem_list = paginator.page(paginator.num_pages)

    pTag = []
    for x in problem_list:
        pTag.append(x.tag.all())

    pages = []
    for i in range(1, problem_list.paginator.num_pages + 1):
        if problem_list.paginator.num_pages == problem_list.number and i == problem_list.number - 1:
            pages.append(0)            
        elif 1 == problem_list.number and i == problem_list.number + 2:
            pages.append(0)
        if i <= 2: 
            pages.append(i)
        elif problem_list.paginator.num_pages - i <= 1:
            pages.append(i)
        elif abs(i - problem_list.number) <= 1:
            if problem_list.number - i == 1 and problem_list.number - 2 != 2:
                pages.append(0)
            pages.append(i)
            if i - problem_list.number == 1 and problem_list.number != problem_list.paginator.num_pages - 3:
                pages.append(0)

    list = zip(problem_list.object_list, pTag)
    return render(request, 'polls/tag.html', {'tag_id': tag_id, 'list': list, 'pTag': pTag, 'member_id': request.session['member_id'], 'top_rank_list': get_rank(0), "problem_list": problem_list, "pages": pages})


def level(request, l, page):
    problem_list = Problem.objects.filter(level = l)
    paginator = Paginator(problem_list, 20)

    if not request.session.get('member_id', None):
        request.session['member_id'] = 0
    member_id = request.session['member_id']

    try:
        problem_list = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        problem_list = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        problem_list = paginator.page(paginator.num_pages)

    pTag = []
    for x in problem_list:
        pTag.append(x.tag.all())

    pages = []
    for i in range(1, problem_list.paginator.num_pages + 1):
        if problem_list.paginator.num_pages == problem_list.number and i == problem_list.number - 1:
            pages.append(0)            
        elif 1 == problem_list.number and i == problem_list.number + 2:
            pages.append(0)
        if i <= 2: 
            pages.append(i)
        elif problem_list.paginator.num_pages - i <= 1:
            pages.append(i)
        elif abs(i - problem_list.number) <= 1:
            if problem_list.number - i == 1 and problem_list.number - 2 != 2:
                pages.append(0)
            pages.append(i)
            if i - problem_list.number == 1 and problem_list.number != problem_list.paginator.num_pages - 3:
                pages.append(0)

    list = zip(problem_list.object_list, pTag)
    return render(request, 'polls/level.html', {'level_id': l, 'list': list, 'pTag': pTag, 'member_id': request.session['member_id'], 'top_rank_list': get_rank(0), "problem_list": problem_list, "pages": pages})
