from django.shortcuts import render, redirect
from .models import User, Article, PostImage, category, Comment, Replies, securityQuestion
from django.contrib import messages
from django.contrib.auth import authenticate, login as authlogin, logout
from django.contrib.auth.decorators import login_required
import random, math
from django.http import JsonResponse
from pathlib import Path
import os
from django.contrib.auth.hashers import make_password
from django.db.models import Q
import json

def Home(request):

    allactiveposts = Article.objects.filter(is_active = True)
    techdata = Article.objects.filter(is_active = True, cat__title = "tech").all()
    businessdata = Article.objects.filter(is_active = True, cat__title = "business").all()

    
    if len(allactiveposts) == 0:
        latestpost = []
        frontpost = []
        business = []
        techdata= []
        businessdata = []
        first_tech = None
        last_tech = None
        othertech = []
        
        
    
        banner = None

    else:
        latestpost = allactiveposts.latest("dateCreated")
        frontpost = allactiveposts.exclude(id=latestpost.id)[:6]
        business = allactiveposts.filter(cat=5)[:3]
        banner = allactiveposts[ math.floor(random.random() * len(allactiveposts)) ]

       

        if len(techdata) == 0:
            techdata = []
            first_tech = None
            last_tech = None
            othertech = []
         
        
        elif len(techdata) == 1:
            first_tech = techdata[0]
            last_tech = None
            othertech = []
          
            

        elif len(techdata) > 1:
            first_tech = techdata[0]
            last_tech = techdata[len(techdata)-1]
            othertech = techdata[1:len(techdata) - 1]
           

        

        
    if request.user.is_anonymous:
        user = None
    else:
        user = request.user
    
    

    context = {
        "auth": user,
        "singlepost": latestpost,
        "frontpost": frontpost,
        "business": business,
        "businessdata": businessdata,
        "tech": techdata,
        "first_tech": first_tech,
        "last_tech": last_tech,
        'othertech': othertech,
        'banner': banner,
       
    }



    
    return render(request, 'index.html', context )

def login(request):
    if request.method == 'POST':
       
        email = request.POST.get('email')
        password = request.POST.get('password')

        user_auth = authenticate(email=email, password=password)

        print(user_auth)

        if user_auth is not None:
            authlogin(request, user_auth)
            return JsonResponse("login successful", safe=False, status=200)
        else:
            return JsonResponse("invalid credentials", safe=False, status=400)
    return render(request, 'login.html')

def register(request):

    question = securityQuestion.objects.all()

    if request.method == 'POST':
        fname = request.POST.get('first_name')
        lname = request.POST.get('last_name')
        email = request.POST.get('email')
        username = request.POST.get('username')
        password = request.POST.get('password')
        question = request.POST.get('question')
        answer = request.POST.get('answer')
       


        if fname == "" or lname == ""  or email == "" or username == "" or password == "":
             return JsonResponse("all input fields must be provided", safe=False, status=400)

        elif User.objects.filter(username=username).exists():
            return JsonResponse("username already exists", safe=False, status=400)

        elif User.objects.filter(email=request.POST['email']).exists():
             return JsonResponse("email already exists", safe=False, status=400)

        else:
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=fname,
                last_name=lname,
                question = question,
                answer = answer
            )

            user_auth = authenticate(email=email, password=password)

            authlogin(request, user_auth)

            return JsonResponse("account created successfully", safe=False, status=200)
    
    return render(request, 'register.html', context={"question": question} )

def updateprofile(request, pk):

    user = User.objects.filter(id = pk).first()
    auth = request.user

    if auth is None:
          return render(request, 'update-profile.html', {"auth": None})
    
    elif user.id != auth.id:
        return redirect("/login")
    
    elif request.method == 'POST':
    
        if request.FILES.get('uimg') is not None:
            img = request.FILES.get('uimg')

            
            if user.image != "":
            
                if user.image != "profile/user.webp":
                    print("confirm")
                    os.remove('media/'+str(user.image))
                    user.image = img
                    user.save()
                    return redirect('/')
                else:
                    
                    user.image = img
                    user.save()
                    return redirect('/')

            # else:
            #     user.image = img
            #     user.save()
            return render(request, 'update-profile.html', {"auth": auth})
        elif request.POST['username'] or request.POST['first_name'] or request.POST['last_name']:
            
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            username = request.POST['username']
            oldusername = request.POST['oldusername']

            check_user = User.objects.filter(username = username).first()

            if check_user is None:

                user.first_name = first_name
                user.last_name = last_name
                user.username = username

                user.save()

                return JsonResponse("success", safe=False, status=200)
            
            elif check_user.username == oldusername:
                user.first_name = first_name
                user.last_name = last_name

                user.save()
            
                return JsonResponse("success", safe=False, status=200)
            
            elif check_user.username != oldusername:
                
                return JsonResponse("username already exists", safe=False, status=400)
    
    else:
        return render(request, 'update-profile.html', {"auth": auth})
    
   
def changePassword(request):
   
    if request.method == 'POST':
        if request.POST.get('email'):
            email = request.POST['email']

            if email == "":
                return JsonResponse("field cannot be empty", safe=False, status=400)
            else:

                user = User.objects.filter(email=email).first()
                # question_pick = User.objects.filter(question=question, answer=answer).first()
                if user is None:
                    return JsonResponse("no email not found", safe=False, status=400)
                else:
                    return JsonResponse(user.question, safe=False, status=200)
                
        elif request.POST.get('answer'):
            answer = request.POST['answer']
            email = request.POST['useremail']

            chk = User.objects.filter(email = email, answer = answer).first()

            if chk is None:
                return JsonResponse("invalid answer", safe=False, status=400)
            else:
                return JsonResponse("success", safe=False, status=200)
        
        elif request.POST.get('newpassword'):
            password = request.POST['newpassword']
            email = request.POST['emailType']

            user = User.objects.filter(email= email).first()
            epwd = make_password(password)

            user.password = epwd
            user.save()

            return JsonResponse("success", safe=False, status=200)
            
      
    return render(request, 'forgetpassword.html')

def signout(request):
    logout(request)
    return redirect('/login')
    


def delete(request):
    if request.method == "GET":
        id = request.GET['id']

        user = User.objects.filter(id = id).first()

        if user is None:
            return JsonResponse("No user found", safe=False, status=400)
        else:
            user.delete()
            return JsonResponse("success", safe=False, status=200)



def postArticle(request):

    cat = category.objects.all()
    

    if request.user.is_anonymous:
        user = None
    else:
        user = request.user
    

    context = {
        'categories': cat,
        'auth': user
    }

    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('desc')
        id = request.POST.get('cat')
        images = request.FILES.getlist('images')

        if request.user.is_anonymous:
            user = None
        else:
            user = request.user
    


        if user.is_anonymous:
            
            return redirect("/login")
        
        else:


            if title == "" or desc == "":
                messages.warning(request, "fill all fields")

            elif id == "":
                messages.warning(request, "select a category")


            elif Article.objects.filter(title = title).exists():
                 messages.warning(request, "this title already exists")
            
            else:
                cats = category.objects.filter(id = id).first()
                new_article = Article.objects.create(
                    user = user,
                    title = title,
                    desc = desc,
                    cat = cats
                )

                if len(images) > 0:
                     for img in images:
                         newarticle_img = PostImage.objects.create(image = img)
                         new_article.image.add(newarticle_img)
                        


                new_article.save()

                messages.success(request, "Article saved successfully")

        

    return render(request, 'postarticle.html', context)



def blogDetails(request, pk):

    otherarticle = Article.objects.exclude(is_active = True, id = pk)

    result = None
    error = None

    if request.user.is_anonymous:
        user = None
    else:
        user = request.user
    
    

    articlefetch = Article.objects.filter(id=pk).first()

    if articlefetch is not None:
        result = articlefetch
        error = None
        fetchcomments = Comment.objects.filter(article = articlefetch).all().order_by("-id")
        if request.user.is_anonymous:
            user = None
        else:
            user = request.user
    

    else:
        result = None
        error = None
        fetchcomments = None
        if request.user.is_anonymous:
            user = None
        else:
            user = request.user
    
    
    if request.method == "POST":
        if request.POST.get("message") is not None:
            message = request.POST['message']

            if request.user.is_anonymous:
               user = None
               return redirect("/login")

            else:
                user = request.user
                
                newcomment = Comment.objects.create(
                    user = user,
                    message = message,
                    article = articlefetch
                )

                messages.success(request, "comment added")

                redirect("blogdetails/"+str(pk))

        elif request.POST['reply'] is not None:

            if request.user.is_anonymous:
                user = None
                return redirect("/login")
            else:
                user = request.user
                reply = request.POST['reply']
                comment_id = request.POST['comment']


                if reply == "":
                    error = "Enter message"
                    messages.warning(request, "please enter your comment")

                else:
                    new_reply = Replies.objects.create(
                        user = user,
                        message = reply
                    )

                    comment = Comment.objects.filter(id=comment_id).first()

                    if comment is None:
                       return redirect("/")
                    else:
                        comment.replies.add(new_reply)

                        redirect("blogdetails/"+str(pk))
            



    
    context = {
        "data": result,
        "error": error,
        "comments": fetchcomments,
        "auth": user,
        "otherarticle": otherarticle

    }



    return render(request, 'single-post.html', context)


def deleteReply(request):
    if request.method == "GET":

        id = request.GET.get("id")
        comment = request.GET.get("comment")

        chk = Comment.objects.filter(id=comment).first()
        
        if chk is not None:
           chk_rpl = chk.replies.filter(id=id).first()
           chk_rpl.delete()

           return JsonResponse("success", safe=False, status=200)
           

        return JsonResponse("error", safe=False, status=400)

        

def deleteComment(request):
    if request.method == "GET":

        comment = request.GET.get("comment")

        chk = Comment.objects.filter(id=comment).first()
        
        if chk is not None:
           
           chk.delete()

           return JsonResponse("success", safe=False, status=200)
           

        return JsonResponse("error", safe=False, status=400)


def search(request):
    if request.method == "GET":
        text = request.GET.get("text")

        result = Article.objects.filter(Q(title__icontains=text) | Q(desc__icontains=text))

        others = Article.objects.exclude(Q(title__icontains=text) | Q(desc__icontains=text))


        if request.user.is_anonymous:
            user = None
        else:
            user = request.user

        
        return render(request, "search-result.html", context={"results": result, "others": others, 'auth': user})
       



