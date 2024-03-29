from django.shortcuts import redirect,render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from myapp.EmailBackEnd import EmailBackEnd
from myapp.models import*
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required

# from .forms import AuthorLoginForm
# from myapp.custom_auth_backends import AuthorBackend

def register(request):
  
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')


            # check email
        if User.objects.filter(email=email).exists():
           messages.warning(request,'Email are Already Exists !')
           return redirect('register')

        # check username
        if User.objects.filter(username=username).exists():
           messages.warning(request,'Username are Already exists !')
           return redirect('register')
        
        user=User(
            username=username,
            email=email,
        )

        user.set_password(password)
        user.save()
        user_role = UserProfile.objects.create(user=user, role=role , email = email)
        user_role.save()
        if role == 'Tutor':
            author = Author(user = user,
                            name = user)
            author.save()
        # print("hii/n")
        return redirect('login')


    return render(request,'registration/register.html')


def dologin(request):

    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        user = EmailBackEnd.authenticate(request,
                                     username=email,
                                     password=password)
        # user = User.objects.get(email=email)

        if user!=None:
           login(request,user)
           try:
                    user_profile = UserProfile.objects.get(user=user)
                    if user_profile.role == 'Tutor':
                        return redirect('instructor_home')
                    else:
                        return redirect('home')
           except UserProfile.DoesNotExist:
                    print("except is running...................")
                    # Handle case if UserProfile does not exist
                    pass
        #    return redirect('home')
        else:
           messages.error(request,'Email and Password Are Invalid !')
           return redirect('login')
        
    return render(request,'registration/login.html')
        

def log_out(request):
    logout(request)
    return redirect('home')      


def home(request):

    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('id')[0:3]
    course_author = Course.objects.all()

    instructor  = Author.objects.all()
    # print(author)
    
    context={
       "category":category,
       "course":course,
       "instructor": instructor,
       "course_author":course_author
   }
    return render(request,'main/home.html',context) 



# custom_auth_backends.py


# def author_login(request):
#     if request.method == 'POST':
#         form = AuthorLoginForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data['email']
#             password = form.cleaned_data['password']
#             author = authenticate(request, email=email, password=password,)
#             if author is not None:
#                 # login( request,author)
#                 # Redirect to a success page
#                 return redirect('home')
#             else:
#                 messages.error(request,'Email and Password Are Invalid !')
#                 return redirect('instructor_login')
#     else:
#         form = AuthorLoginForm()
#     return render(request,'instructor_register/login.html',{'form': form})
def free(request):
    return render(request,'instructor/instructor_base.html')

@login_required
def profile(request):
    return render(request,'registration/profile.html')

@login_required
def profile_update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        user_id = request.user.id

        user = User.objects.get(id=user_id)
        user.first_name = first_name
        user.last_name = last_name
        user.username = username
        user.email=email

  

        if password != None and password != "":
            user.set_password(password)
        user.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return render(request,'registration/profile.html')
    
