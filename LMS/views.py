from django.shortcuts import redirect,render

from django.template.loader import render_to_string
from django.http import JsonResponse

from myapp.models import*
from django.db.models import Sum,Avg
from django.contrib import messages
from django.contrib.auth.decorators import login_required


def BASE(request ):
    user_name = request.user.id
    name = UserProfile.objects.filter(user = user_name , role = "Tutor")
    if name:
        user_is_tutor = True
    else:
        user_is_tutor = False
    return render(request,'base.html',{"user_is_tutor":user_is_tutor})

def home(request ):
    category = Categories.objects.all().order_by('id')[0:5]
    course = Course.objects.filter(status='PUBLISH').order_by('id')[0:3]
    course_author = Course.objects.all()

    instructor  = Author.objects.all().order_by('id')[0:4]
    # print(author)
    
    context={
       "category":category,
       "course":course,
       "instructor": instructor,
       "course_author":course_author
   }
    return render(request,'main/home.html',context)    


 

def contact_us(request ):
    
    if request.method == "POST":
        name = request.POST.get('name')
        email= request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        print(name,email,subject,message)
        
        ContactUs.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
            
        )
        messages.success(request,'Your Response Successfully Submited.')
    user_name = request.user.id
    name = UserProfile.objects.filter(user = user_name , role = "Tutor")
    if name:
        user_is_tutor = True
    else:
        user_is_tutor = False

    print("user status in contact us",user_is_tutor)    
       
        
      
    return render(request,'main/contact.html',{"user_is_tutor":user_is_tutor})
    
def about_us(request ):
    user_name = request.user.id
    name = UserProfile.objects.filter(user = user_name , role = "Tutor")
    if name:
        user_is_tutor = True
    else:
        user_is_tutor = False
    category = Categories.objects.all().order_by('id')
    context = {
        "category":category,
        "user_is_tutor":user_is_tutor

    }
    return render(request,'main/about_us.html',context)    

def single_course(request):
   
    category = Categories.objects.filter(course__status = 'PUBLISH').order_by('id').distinct()
   
    level = Level.objects.all()

    course = Course.objects.filter(status='PUBLISH')
    instructor = Author.objects.all()
    a = Course.objects.filter(status = 'PUBLISH')
    # time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))


    total_courses =  Course.objects.filter(status = 'PUBLISH').count()
    freecourse_count = Course.objects.filter(price = 0,status = 'PUBLISH').count()
    paidcourse_count = Course.objects.filter(price__gte=1,status = 'PUBLISH').count()
    # instructor_count = Course.objects.filter(Author.name).count
    context = {
        "course":course,
        "total_courses":total_courses,
        "category":category,
        "level":level,
        "freecourse_count":freecourse_count,
        "paidcourse_count":paidcourse_count,
        "instructor":instructor,
     
        # "instructor_count":instructor_count,
        
          }

    return render(request,'main/single_course.html',context)    

def rough(request ):
    course = Course.objects.filter(status='PUBLISH').order_by('id')

    return render(request,'main/freework.html',{"course":course })    

def search_course(request ):
    query = request.GET['query']
    course = Course.objects.filter(title__icontains = query,status='PUBLISH')
    # print(course)
    category = Categories.objects.all().order_by('id')
    context = {
        "category":category,
        "course":course

    }


    return render(request,'search/search.html',context)    

@login_required
def course_details(request,slug):
    course = Course.objects.filter(slug = slug,status = 'PUBLISH')
    user_name = request.user.id
    name = UserProfile.objects.filter(user = user_name , role = "Tutor")
    if name:
        user_is_tutor = True
    else:
        user_is_tutor = False

    print("loggedin user isssssss..........",user_is_tutor)    

        
    category = Categories.objects.all().order_by('id')
    video = Video.objects.all()
    course_get = Course.objects.get(slug = slug)
    course_id = course_get.id
    time_duration = Video.objects.filter(course__slug = slug).aggregate(sum=Sum('time_duration'))
    course_reviews = Review.objects.filter(course_id = course_id)
    average_rating = course_reviews.aggregate(Avg('rating'))['rating__avg']
    if average_rating is None:
        average_rating = 0
    else:    

        average_rating = round(average_rating, 2)

    average_rating_percentage =round( (average_rating / 5) * 100)

    reviews_with_rating_5 = Review.objects.filter(course_id=course_id, rating="5").count()
    reviews_with_rating_45 = Review.objects.filter(course_id=course_id, rating="4.5").count()
    reviews_with_rating_3 = Review.objects.filter(course_id=course_id, rating="3").count()
    reviews_with_rating_25 = Review.objects.filter(course_id=course_id, rating="2.5").count()
    reviews_with_rating_1 = Review.objects.filter(course_id=course_id, rating="1").count()


    course_id = Course.objects.get(slug = slug)
    course_author = course_id.author
    instructor_avg_rating = Course.objects.filter(author=course_author).aggregate(Avg('review__rating'))['review__rating__avg']
    if instructor_avg_rating is None:
        instructor_avg_rating = 0
    instructor_avg_rating = round(instructor_avg_rating,2)
    instructor_avg_rating_per = round(((instructor_avg_rating/5) *100))


    instructor_reviews = Review.objects.filter(course__author = course_author)
    instructor_course = Course.objects.filter(author=course_author)
    student_enrolled = UserCourse.objects.filter(course__author = course_author)
    





    try:
         check_enroll  = UserCourse.objects.get(user = request.user , course = course_id)
    except UserCourse.DoesNotExist :
         check_enroll = None     
    if course.exists():
        course = course.first()
    else:
        return redirect('404')   

    context = {
        "course":course,
         "category":category,
         "time_duration": time_duration,
         "check_enroll":check_enroll,
         "video":video,
         "user_is_tutor":user_is_tutor,
         "average_rating":average_rating,
         "average_rating_percentage": average_rating_percentage,
        #  "reviews_with_rating_5_per": reviews_with_rating_5_per,
        #  "reviews_with_rating_45_per": reviews_with_rating_45_per,
        #  "reviews_with_rating_3_per": reviews_with_rating_3_per,
        #  "reviews_with_rating_25_per": reviews_with_rating_25_per,
        #  "reviews_with_rating_1_per": reviews_with_rating_1_per,
         "reviews_with_rating_5": reviews_with_rating_5,
         "reviews_with_rating_45": reviews_with_rating_45,
         "reviews_with_rating_3": reviews_with_rating_3,
         "reviews_with_rating_25": reviews_with_rating_25,
         "reviews_with_rating_1": reviews_with_rating_1,
         "instructor_avg_rating":instructor_avg_rating,
         "instructor_reviews":instructor_reviews,
         "instructor_course": instructor_course,
         "student_enrolled": student_enrolled,
         "instructor_avg_rating_per":instructor_avg_rating_per,
         "course_reviews":course_reviews



    } 

    return render(request,'course/course_details.html',context)

def filter_data(request):
  category = request.GET.getlist('category[]')
  level = request.GET.getlist('level[]') 
  price = request.GET.getlist('price[]')
  instructor = request.GET.getlist('instructor[]')
  

  print(instructor)

  if price ==['PriceFree']:
       course = Course.objects.filter(price=0,status = 'PUBLISH')
  elif price ==['PricePaid']:
       course = Course.objects.filter(price__gte=1,status = 'PUBLISH')
  elif price ==['PriceAll']:
       course = Course.objects.filter(status = 'PUBLISH')

  elif category:
       course = Course.objects.filter(category__id__in=category,status = 'PUBLISH').order_by('-id')
  elif level:
       course = Course.objects.filter(level__id__in = level,status = 'PUBLISH').order_by('-id')
  elif instructor:
       course = Course.objects.filter(author__id__in = instructor,status = 'PUBLISH').order_by('-id')     
      
  else:
      course =Course.objects.filter(status = 'PUBLISH').order_by('-id')  
  context = {
      "course":course
  }      
  t = render_to_string('ajax/course.html',context)

  return JsonResponse({'data': t})


def page_not_found(request):
    category = Categories.objects.all().order_by('id')
    context = {
        "category":category

    }
    return render(request,'error/404.html',context)    

@login_required
def checkout(request,slug):
    course = Course.objects.get(slug = slug,status = 'PUBLISH')

    if course.price==0:
        course =UserCourse(

            user = request.user,
            course = course,
        ) 
        course.save()
        messages.success(request,"Course is Successfully Enrolled !!")
        return redirect('mycourse')

    return render(request,'checkout/checkout.html')

@login_required
def mycourse(request):
    course = UserCourse.objects.filter(user = request.user)
    context ={
        "course":course
    }
    return render(request,'course/mycourse.html',context)

@login_required
def watch_course(request,slug):
    # print("ddadadad",lecture)
    course_id = Course.objects.get(slug = slug)
    course = Course.objects.filter(slug = slug)
    material = CourseMaterial.objects.all()
    lecture = request.GET.get('lecture')
    # print("dsfsgsdbfgsgf",lecture)
    video = Video.objects.filter(id=lecture)
    # print(video.get())
    

    try:
        check_enroll = UserCourse.objects.get(user = request.user , course = course_id) 
        if course.exists():
            course = course.first()
        else:
            print("ggogogoggogogogoggogo...........")

            return redirect('404')    
    except UserCourse.DoesNotExist:
        print("hhihihihihihhihihihihhi")
        return redirect('404')  

    context ={
        "course":course,
        "video":video,
        "lecture":lecture,
        "check_enroll":check_enroll,
        "material":material

    }  
    return render(request,'course/watch_course.html',context)

def instructor_list(request):
    instructor = Author.objects.all()
    category = Categories.objects.all().order_by('id')

    context = {
        "instructor":instructor,
        "category":category,
    }
    return render(request,'instructor/instructor_list.html',context)

def instructor_filter_data(request):

    category = request.GET.getlist('category[]')
    instructor_filter = request.GET.getlist('instructor[]')
    rating_filter = request.GET.getlist('rating[]')

    # print("search Author is ",instructor)


    # specific_author = Author.objects.get(id=<author_id>)


    print(instructor_filter)    


    if category:
        instructor = Author.objects.filter(category__id__in = category).order_by('-id')
 
    elif instructor_filter:
        instructor = Author.objects.filter(id__in = instructor_filter).order_by('-id')
    elif rating_filter == ["1up"]:
       instructor = Author.objects.annotate(avg_rating=Avg('course__review__rating')).filter(avg_rating__gte=1)
        # print("1 up rating  are",instructor)
    elif rating_filter == ["2up"]:
        instructor = Author.objects.annotate(avg_rating=Avg('course__review__rating')).filter(avg_rating__gte=2)
        # print("1 up rating  are",instructor)    
    elif rating_filter == ["25up"]:
        instructor = Author.objects.annotate(avg_rating=Avg('course__review__rating')).filter(avg_rating__gte=2.5)
        # print("1 up rating  are",instructor)    
    elif rating_filter == ["35up"]:
        instructor = Author.objects.annotate(avg_rating=Avg('course__review__rating')).filter(avg_rating__gte=3.5)
    elif rating_filter == ["4up"]:
        instructor = Author.objects.annotate(avg_rating=Avg('course__review__rating')).filter(avg_rating__gte=4)
        # print("1 up rating  are",instructor)
   
    else:
        instructor = Author.objects.all().order_by('-id')


  
    context={
        "instructor":instructor,

    }

    t = render_to_string('ajax/instructor.html',context)
    return JsonResponse({'data': t})

def single_instructor(request,id):
    print("insss id is.............*******",id)
    instructor = Author.objects.filter(id =id)
    course = Course.objects.filter(author__id = id,status = 'PUBLISH')
    lesson_count = Course.objects.filter()
    instructor_reviews = Review.objects.filter(course__author__id = id)
    avg_rating = Course.objects.filter(author__id=id).aggregate(Avg('review__rating'))['review__rating__avg']
    if avg_rating is None:
        avg_rating=0
    else:

         avg_rating= round(avg_rating,2)

    
    # avg_rating = instructor_reviews.filter("rating")
    print("instrcutor rating is............",avg_rating)
    print("instrcutor course count  is............",course)
    print("instrcutor  is............",instructor)


    # print(lesson_count)
    # print(course)
    context={
        "instructor":instructor,
        "course":course,
        "instructor_reviews":instructor_reviews,
        "avg_rating":avg_rating
            }
    return render(request,'instructor/single_instructor.html',context)

def trending_category(request,id):
    course = Course.objects.filter(category_id = id )
    context = {
        "course":course
    }

    return render(request,'course/trending_category.html',context)



def instructor_profile(request):
    user_id = request.user.id
    # instructor = Author.objects.filter(id =user_id)
    course1 = Course.objects.filter(author__id = user_id,status = 'PUBLISH')
    instructor_reviews = Review.objects.filter(course__author__id = user_id)
    avg_rating = Course.objects.filter(author__id=user_id).aggregate(Avg('review__rating'))['review__rating__avg']
    if avg_rating is None:
        avg_rating=0
    else:

         avg_rating= round(avg_rating,2)



    user = User.objects.get(id=user_id)
    instructor = Author.objects.get(name=user)
    course = Course.objects.filter(author__name=user)
  
    
    context={
        "instructor":instructor,
        "course":course,
        "user":user,
         "course":course,
        "instructor_reviews":instructor_reviews,
        "avg_rating":avg_rating

            }
    return render(request,'instructor/profile.html',context)
