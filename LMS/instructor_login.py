from django.shortcuts import redirect,render,get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
# from myapp.EmailBackEnd import EmailBackEnd,EmailBackEnd1
from myapp.models import*
from django.contrib.auth import login,logout
# from .forms import AuthorLoginForm,CourseForm
from myapp.auth_backends import AuthorBackend
from .forms import CourseForm, WhatYouLearnFormSet, RequirementsFormSet,VideoFormSet
from django.urls import reverse

# from myapp.custom_auth_backends import AuthorBackend

# def register(request):
  
#     if request.method == 'POST':
#         name = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')

#             # check email
#         if Author.objects.filter(email=email).exists():
#            messages.warning(request,'Email are Already Exists !')
#            return redirect('instructor_register')

#         # check username
#         if Author.objects.filter(name=name).exists():
#            messages.warning(request,'Username are Already exists !')
#            return redirect('register')
        
#         user = Author(
#             name=name,
#             email=email,
#             password = password
#         )
#         # user.set_password(password)
#         user.save()
#         # print("hii/n")
#         return redirect('instructor_login')


#     return render(request,'instructor_register/register.html')


# def login(request):

#     if request.method == "POST":
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         user = Author.objects.get(email=email)

		
#         # user = EmailBackEnd1.authenticate(request,
#         #                              username=email,
#         #                              password=password)

#         if user!=None and user.password == password:
#         #    login(request,user)
#            return render(request,'instructor/home.html',{"user":user})
#         else:
#            messages.error(request,'Email and Password Are Invalid !')
#            return redirect('instructor_login')
        
#     return render(request,'instructor_register/login.html')
        


def log_out(request):
    logout(request)
    return redirect('instructor_home')     

def home(request):
    name = request.user.username
    print(name)
    course = Course.objects.filter(author__name = name)

    instructor = Author.objects.all()
    # author_name = Author.objects.get(name = name)
    
    material = CourseMaterial.objects.all()
    print(course)
    context = {
        "course": course,
        "material":material,
        "instructor":instructor,
        # "course1":course1
  
    }
    return render(request,'instructor/home.html',context) 



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

# def author_login(request):
#     if request.method == 'POST':
#         # form = AuthorLoginForm(request.POST)
      
#             name = request.POST.get('name')
#             password = request.POST.get('password')
            
#             author = AuthorBackend().authenticate(request,name=name, password=password)
#             author = authenticate_author(name, password)

#             # print("name is",author)
#             if author is not None :
#                 # login(request,author)
#                 request.session['author_id'] = author.id
#                 author = get_logged_in_author(request)
#                 # author_name = Author.objects.get(name = author).id
#                 # print("author_name",author_name)
#                 return render(request,'instructor/home.html',{"author":author}) 
#             else:
#                   messages.error(request,'Email and Password Are Invalid !')
#                   return redirect('instructor_login')
#     return render(request, 'instructor_register/login.html')



def free(request):
    author_name = Author.objects.get(name ='Sakre Chetan').id
    print("author_name",author_name)
    return render(request,'instructor/instructor_base.html')

def profile(request):
    return render(request,'instructor/profile_update.html')

def profile_update(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        domain = request.POST.get('domain')
        category = request.POST.get('category')
        gender = request.POST.get('gender')
        phone_no = request.POST.get('phone')
        bio = request.POST.get('bio')
        author_profile = request.FILES['image']
        print("author is ......................",author_profile)

        user_id = request.user.id
        user = User.objects.get(id=user_id)
        author = Author.objects.get(user = user)
        # category = Categories.objects.get(name= category)

        author.domain = domain
        category, created = Categories.objects.get_or_create(name=category)

        author.category = category
        author.gender = gender
        author.phone_no= phone_no
        author.about_author= bio
        author.author_profile = author_profile
        if password != None and password != "":
            author.password = password
        author.save()
        messages.success(request,'Profile Are Successfully Updated. ')
        return redirect('instructor_profile')
    
def create_course(request):
    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES)
        what_you_learn_formset = WhatYouLearnFormSet(request.POST, prefix='what_you_learn')
        requirements_formset = RequirementsFormSet(request.POST, prefix='requirements')
        video_formset = VideoFormSet(request.POST, request.FILES, prefix='videos')
    
        # category = Categories.objects.get(name= category_name)
        # print("category is...",category)

       


        if all([form.is_valid() for form in [course_form, what_you_learn_formset, requirements_formset, video_formset]]):
            # course_instance = course_form.save()
            if course_form.is_valid():
                category_name = course_form.cleaned_data['category']  # Get the category name from the form
                try:
                  category_instance = Categories.objects.get(name=category_name)
                except Categories.DoesNotExist:
                  category_instance, created = Categories.objects.get_or_create(name=category_name)
                course_instance = course_form.save(commit=False)
                author_instance = Author.objects.get(user=request.user)
                course_instance.author = author_instance  
                course_instance.category = category_instance
                # if Categories.objects.filter(name= category_name).exists():
                #             course_instance.category = category_instance
                # else:
                #             cat = Categories(name = category)   
                #             course_instance.category = category
                #             cat.save()
  
                # course_instance.category = category_instance

                course_instance.save()

            for form in what_you_learn_formset:
                if form.cleaned_data:
                    instance = form.save(commit=False)
                    instance.course = course_instance
                    author_instance = Author.objects.get(user=request.user)
                    course_instance.author = author_instance
                    course_instance.save()
                    instance.save()

            for form in requirements_formset:
                if form.cleaned_data:
                    instance = form.save(commit=False)
                    instance.course = course_instance
                    instance.save()

            # if lesson_formset.is_valid():
            #     for form in lesson_formset:
            #         if form.cleaned_data:
            #             instance = form.save(commit=False)
            #             instance.course = course_instance
            #             instance.save()        

            for form in video_formset:
                if form.cleaned_data:
                    instance = form.save(commit=False)
                    instance.course = course_instance
                    lesson_name = form.cleaned_data.get('lesson_name')
                    material = form.cleaned_data['material']
                    # print("lec pdf is ................",material)
                    if lesson_name:
                        # Create a new lesson instance
                        lesson = Lesson.objects.create(name=lesson_name, course=course_instance)
                        instance.lesson = lesson
                    instance.save()

                    
                    if material:
                        # Create a new lesson instance
                        material = CourseMaterial.objects.create(pdf_file=material, course=course_instance)
                        instance = form.save(commit=False)
                        instance.material = material
                    instance.save()


      
            messages.success(request,'Profile Are Successfully Updated. ')

            return redirect('create_course')

    else:
        course_form = CourseForm()
        what_you_learn_formset = WhatYouLearnFormSet(prefix='what_you_learn')
        requirements_formset = RequirementsFormSet(prefix='requirements')
        video_formset = VideoFormSet(prefix='videos')
        # lesson_formset = LessonFormSet()

    return render(request,'instructor/create_course.html', {
        'course_form': course_form,
        'what_you_learn_formset': what_you_learn_formset,
        'requirements_formset': requirements_formset,
        'video_formset': video_formset,
        #  "user":user
        # 'lesson_formset': lesson_formset,  
    })




def add_content(request):
    if request.method == 'POST':
        requirement_forms = []
        what_you_learn_forms = []
        video_forms = []
        # lesson_forms = []

        # Process Requirement forms
        requirement_count = int(request.POST.get('requirement_count', 0))
        for i in range(1, requirement_count + 1):
            form =RequirementsFormSet(request.POST, prefix=f'requirement_{i}')
            if form.is_valid():
                requirement_forms.append(form)
            else:
                print(f'Requirement form {i} errors:', form.errors)
        
        # Process What You Learn forms
        what_you_learn_count = int(request.POST.get('what_you_learn_count', 0))
        for i in range(1, what_you_learn_count + 1):
            form = WhatYouLearnFormSet(request.POST, prefix=f'what_you_learn_{i}')
            if form.is_valid():
                what_you_learn_forms.append(form)
            else:
                print(f'What You Learn form {i} errors:', form.errors)

        # Process Video forms
        video_count = int(request.POST.get('video_count', 0))
        for i in range(1, video_count + 1):
            form = VideoFormSet(request.POST, prefix=f'video_{i}')
            if form.is_valid():
                video_forms.append(form)
            else:
                print(f'Video form {i} errors:', form.errors)

        # Process Lesson forms
        # lesson_count = int(request.POST.get('lesson_count', 0))
        # for i in range(1, lesson_count + 1):
        #     form = LessonForm(request.POST, prefix=f'lesson_{i}')
        #     if form.is_valid():
        #         lesson_forms.append(form)
        #     else:
        #         print(f'Lesson form {i} errors:', form.errors)

        # Process other fields of the Course model
        course_form = CourseForm(request.POST)
        if course_form.is_valid() and all(form.is_valid() for form in requirement_forms) \
                and all(form.is_valid() for form in what_you_learn_forms) \
                and all(form.is_valid() for form in video_forms) :
                # and all(form.is_valid() for form in lesson_forms):
            course_instance = course_form.save()  # Save the course instance
            # Save other related instances or perform other operations
            return redirect('create_course')
        else:
            print('Course form errors:', course_form.errors)

    # If the request method is GET, render the form page
    requirement_form = RequirementsFormSet()
    what_you_learn_form = WhatYouLearnFormSet()
    video_form = VideoFormSet()
    # lesson_form = LessonForm()
    course_form = CourseForm()

    return render(request, 'instructor/create_course.html', {
        'requirement_form': requirement_form,
        'what_you_learn_form': what_you_learn_form,
        'video_form': video_form,
        # 'lesson_form': lesson_form,
        'course_form': course_form,
       
    })


from django.http import JsonResponse

def save_lesson(request):
    if request.headers.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest' and request.method == 'POST':
        lesson_name = request.POST.get('lesson_name')
        # Save the lesson name to the Lesson model
        lesson = Lesson.objects.create(name=lesson_name)
        lesson.save()
        return JsonResponse({'success': True})
    # Return an error response if the request is not AJAX or POST
    return JsonResponse({'success': False})


def instructor_course(request):
    # print("id is ",id)

    name = request.user
    print(name)
    

    course = Course.objects.filter(author__user = name)
    print("tutor course are..........",course)
    context = {

    
        "course": course
    }
    return render(request,'instructor/my_courses.html',context)

def instructor_search_course(request):
    query = request.GET['query']
    name = request.user.username
    course = Course.objects.filter(title__icontains = query,status='PUBLISH',author__name = name)
    category = Categories.objects.all().order_by('id')
    context = {
        "category":category,
        "course":course

    }
    return render(request,'instructor/search_course.html',context)

def update_course(request,id=None):
    if id:
        course_instance = get_object_or_404(Course, pk=id)
    else:
        course_instance = None

    if request.method == 'POST':
        course_form = CourseForm(request.POST, request.FILES, instance=course_instance)
        what_you_learn_formset = WhatYouLearnFormSet(request.POST, prefix='what_you_learn', instance=course_instance)
        requirements_formset = RequirementsFormSet(request.POST, prefix='requirements', instance=course_instance)
        video_formset = VideoFormSet(request.POST, request.FILES, prefix='videos', instance=course_instance)

        if all([form.is_valid() for form in [course_form, what_you_learn_formset, requirements_formset, video_formset]]):
            course_instance = course_form.save(commit=False)
            author_instance = Author.objects.get(user=request.user)
            course_instance.author = author_instance

            category_name = course_form.cleaned_data['category']  
            category_instance, created = Categories.objects.get_or_create(name=category_name)
            course_instance.category = category_instance
            course_instance.save()

            what_you_learn_formset.save()
            requirements_formset.save()

            # Save videos with proper lesson assignment
            if video_formset.is_valid():
                for video_form in video_formset:
                    if video_form.cleaned_data:
                        video_instance = video_form.save(commit=False)
                        lesson_name = video_form.cleaned_data.get('lesson_name')
                        material = video_form.cleaned_data['material']

                        if lesson_name:
                            # If a lesson name is provided, create or get the corresponding lesson
                            lesson_instance, created = Lesson.objects.get_or_create(name=lesson_name, course=course_instance)
                            video_instance.lesson = lesson_instance
                        video_instance.course = course_instance
                        video_instance.save()


                        if material:
                        # Create a new lesson instance
                            material = CourseMaterial.objects.create(pdf_file=material, course=course_instance)
                            # instance = video_form.save(commit=False)
                        video_instance.material = material
                        video_instance.save()


            messages.success(request, 'Course successfully updated.' if id else 'Course successfully created.')

            return redirect('create_course')  # Adjust the URL name as needed

    else:
        course_form = CourseForm(instance=course_instance)
        what_you_learn_formset = WhatYouLearnFormSet(prefix='what_you_learn', instance=course_instance)
        requirements_formset = RequirementsFormSet(prefix='requirements', instance=course_instance)
        video_formset = VideoFormSet(prefix='videos', instance=course_instance)

    return render(request, 'instructor/create_course.html', {
        'course_form': course_form,
        'what_you_learn_formset': what_you_learn_formset,
        'requirements_formset': requirements_formset,
        'video_formset': video_formset,
    })

def submit_review(request,id):

    if request.method == 'POST':

        rating = request.POST.get('rating')
        title = request.POST.get('title')
        content = request.POST.get('content')
        course = Course.objects.get(id = id)
        user_name = request.user.username
        user = User.objects.get(username = user_name)

   
        review = Review.objects.create(
            course_id =id,
            course = course,
            user = user,
            
            rating=rating,
            title=title,
            content=content
        )
        messages.success(request,"Your review has been successfully submitted..!!")
        return redirect(request.META.get('HTTP_REFERER'))

    else:

     return render(request,'course/course_details.html')
    
from django.shortcuts import get_object_or_404
from django.http import FileResponse
# from .models import CourseMaterial

def download_pdf(request, id):
    material = get_object_or_404(CourseMaterial, id = id)
    file_path = material.pdf_file.path
    response = FileResponse(open(file_path, 'rb'), as_attachment=True)
    return response    



# instructor_watch_course

def instructor_watch_course(request,slug):
    # print("ddadadad",lecture)
    course_id = Course.objects.get(slug = slug)
    course = Course.objects.filter(slug = slug)
    material = CourseMaterial.objects.all()
    lecture = request.GET.get('lecture')
    # print("dsfsgsdbfgsgf",lecture)
    video = Video.objects.filter(id=lecture)
    # print(video.get())
    

    # try:
    # check_enroll = UserCourse.objects.get(user = request.user , course = course_id) 
    if course.exists():
            course = course.first()
    else:
        print("ggogogoggogogogoggogo...........")

        return redirect('404')    
    # except UserCourse.DoesNotExist:
    #     print("hhihihihihihhihihihihhi")
    #     return redirect('404')  

    context ={
        "course":course,
        "video":video,
        "lecture":lecture,
        # "check_enroll":check_enroll,
        "material":material

    }  
    return render(request,'instructor/instructor_watch_course.html',context)

    # instructor/instructor_watch_course.html