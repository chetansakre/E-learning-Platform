from django.db import models
from django.utils.text import slugify
from django.db.models.signals import pre_save
from django.contrib.auth.models import User
from django.utils.html import mark_safe


class UserProfile(models.Model):
    USER_ROLE_CHOICES = (
        ('Learner', 'Learner'),
        ('Tutor', 'Tutor'),
    )
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=USER_ROLE_CHOICES)
    email = models.EmailField( max_length=254 ,null=True) 

    


    def __str__(self):
        return self.user.username+ " - " + self.role

class Categories(models.Model):
    icon = models.CharField(max_length=200 , null = True)
    name = models.CharField( max_length=200)


    def __str__(self):
        return self.name
    
class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE ,null =True) 
    author_profile = models.ImageField(upload_to="Media/author")
    name = models.CharField(max_length=100, null=True)
    about_author = models.TextField()
    domain = models.CharField( max_length=100,null=True,default = "Devloper")
    category = models.ForeignKey(Categories, on_delete=models.CASCADE,null=True)
    # email = models.EmailField( max_length=254 ,null=True) 
    # password = models.CharField( max_length=50 ,null=True)
    phone_no = models.IntegerField(null =True)
    gender = models.CharField( max_length=50,null =True)

    def __str__(self):
        return self.name
    def image_tag(self):
        return mark_safe('<img src="%s" width="100px" height="100px" />'%(self.author_profile.url))
    image_tag.short_description = 'Image'


    



class Level(models.Model):
    name = models.CharField( max_length=100)

    def __str__(self):
        return self.name

class Language(models.Model):
    language = models.CharField( max_length=100)
    def __str__(self):
        return self.language

class Course(models.Model):
    STATUS = (
        ('PUBLISH','PUBLISH'),
        ('DRAFT', 'DRAFT'),
    )

    featured_image = models.ImageField(upload_to="Media/featured_img",null=True)
    featured_video = models.CharField(max_length=300,null=True)
    title = models.CharField(max_length=500)
    created_at = models.DateField(auto_now_add=True)
    author = models.ForeignKey(Author,on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(Categories,on_delete=models.CASCADE)
    level = models.ForeignKey(Level,on_delete=models.CASCADE , null =True)
    description = models.TextField()
    price = models.IntegerField(null=True,default=0)
    language = models.ForeignKey(Language, on_delete=models.CASCADE,null = True)
    deadline = models.CharField( max_length=100,null=True)
    discount = models.IntegerField(null=True)
    slug = models.SlugField(default='', max_length=500, null=True, blank=True)
    status = models.CharField(choices=STATUS,max_length=100,null=True)
    certificate = models.CharField( max_length=50 , null=True)


    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        from django.urls import reverse
        return reverse("course_details", kwargs= {'slug':self.slug})
    

def create_slug(instance, new_slug=None):
    slug = slugify(instance.title)
    if new_slug is not None:
        slug = new_slug
    qs = Course.objects.filter(slug=slug).order_by('-id')
    exists = qs.exists()
    if exists:
        new_slug = f"{slug}-{qs.count()}"

        return create_slug(instance, new_slug=new_slug)
    return slug


def pre_save_post_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_receiver, Course)


class What_you_learn(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    points = models.CharField( max_length=500)

    def __str__(self):
        return self.points
    
class Requirements(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    points = models.CharField( max_length=500)

    def __str__(self):
        return self.points
    
class Lesson(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.course.title + " - " + self.name
    

class CourseMaterial(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    # name = models.CharField(max_length=200)
    pdf_file = models.FileField(upload_to="Media/Course_Material")
 
    def __str__(self):
            return self.course.title + " - " + str(self.pdf_file)

    
class Video(models.Model):
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    serial_number = models.IntegerField(null = True)
    thumbnail = models.ImageField( upload_to="Media/Yt_Thumbnail",null=True)
    lesson = models.ForeignKey(Lesson,on_delete=models.CASCADE)
    material = models.ForeignKey(CourseMaterial,on_delete=models.CASCADE,null = True, blank=True)
    title = models.CharField( max_length=100)
    youtube_id = models.CharField(max_length=200)
    time_duration = models.IntegerField(null = True)
    preview = models.BooleanField(default = False)

    def __str__(self):
        return self.title
    

class UserCourse(models.Model):
    user = models.ForeignKey( User, on_delete=models.CASCADE)    
    course = models.ForeignKey(Course,on_delete=models.CASCADE)
    paid = models.BooleanField(default = 0)
    date = models.DateTimeField( auto_now_add=True)

    def __str__(self):
        return self.user.username + " - "  + self.course.title
    

class ContactUs(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField(max_length=100)
    subject = models.CharField(max_length=200)
    message = models.TextField()
  
    created_at = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return self.subject  
    
class Review(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE,null = True)  # ForeignKey to User model
    rating = models.DecimalField(max_digits=2, decimal_places=1)  # Assuming you're storing ratings like 4.5, 3.5, etc.
    title = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    





    


        






