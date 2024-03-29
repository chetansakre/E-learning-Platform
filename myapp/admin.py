from django.contrib import admin
from .models import*
# Register your models here.

class What_you_learn_Tabularinline(admin.TabularInline):
    model = What_you_learn

class Requirements_Tabularinline(admin.TabularInline):
    model = Requirements 

class Video_Tabularinline(admin.TabularInline):
    model = Video 

class course_admin(admin.ModelAdmin):
    inlines = (What_you_learn_Tabularinline,Requirements_Tabularinline,Video_Tabularinline)   
    list_display = ["title","author","category","level","language","status","certificate","price" ]
    search_fields = ("title","category__name",)
    list_filter = ("category","author","level","language","price" )
    



    # list_display=('featured_image','title','author')


class AuthorAdmin(admin.ModelAdmin):
    list_display = ["name", "category", "gender", "image_tag"]
    search_fields = ("name",)
    list_filter = ("category","gender", )
    

class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "role", "email",]
    list_filter = ("role",)
    search_fields = ("user__username",)
    # def get_author_gender(self, obj):
    #     # Assuming UserProfile has a foreign key 'user' to the 'User' model
    #     # Assuming User model has a foreign key 'author' to the 'Author' model
    #     # Assuming Author model has a field 'gender'
    #     # Replace 'author__gender' with the actual field name if different
    #     return obj.user.author.gender if obj.user.author else None

    # get_author_gender.short_description = 'Author Gender'  # Customize the column header




class UserCourseAdmin(admin.ModelAdmin):
    list_display = ["user","course",'get_author_name',"paid","date"]
    # list_filter = ("user",)

    def get_author_name(self, obj):
        return obj.course.author.name  # Assuming 'author' has a 'name' field
    get_author_name.short_description = 'Author'  # Customize the colum
class ContactAdmin(admin.ModelAdmin):
    list_display = ["name","email","subject","created_at"]
    search_fields = ("email","subject",)
    list_filter = ("created_at", )

class ReviewAdmin(admin.ModelAdmin):
    list_display = ["course","user","rating","date",]
    search_fields = ["course__title","rating","user__username",]
    list_filter = ["date","rating"]
    ordering = ['rating'] 

class  RequirementsAdmin(admin.ModelAdmin):
    list_display = ["course","points"]
    list_filter = ["course"]
    search_fields = ["course"]


class  What_you_learnAdmin(admin.ModelAdmin):
    list_display = ["course","points"]
    list_filter = ["course"]    
    search_fields = ["course"]
    

class  LessonAdmin(admin.ModelAdmin):
    list_display = ["course","name"]
    list_filter = ["course"]
    search_fields = ["course__title"]    
    ordering = ['name'] 





admin.site.register(Categories)
admin.site.register(Author,AuthorAdmin)
admin.site.register(Course,course_admin)
admin.site.register(Level)
admin.site.register(Requirements,RequirementsAdmin)
admin.site.register(What_you_learn,What_you_learnAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Language)
admin.site.register(UserCourse,UserCourseAdmin)
admin.site.register(UserProfile,UserProfileAdmin)
admin.site.register(ContactUs,ContactAdmin)
admin.site.register(Review,ReviewAdmin)
admin.site.register(CourseMaterial)














