
from django.contrib import admin
from django.urls import path,include
from .import views, user_login,instructor_login
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('base',views.BASE,name='name'),
    path('',views.home,name="home"),
    path('contact/',views.contact_us,name="contact_us"),
    # path('contact/database',views.CONTACT,name="contact_database"),
    path('about/',views.about_us,name="about_us"),
    path('accounts/',include('django.contrib.auth.urls')),
    path('accounts/register',user_login.register,name="register"),
    path('dologin',user_login.dologin,name="dologin"),
    path('logout',user_login.log_out,name="logout"),

    path('accounts/profile',user_login.profile,name="profile"),
    path('accounts/profile/update',user_login.profile_update,name="profile_update"),
    path('rough',views.single_course, name="single_course"),
    path('roughwork',views.rough, name="rough"),
    path('search',views.search_course, name="search_course"),
    path('course/<slug:slug>',views.course_details, name="course_details"),
    path('product/filter-data',views.filter_data,name="filter-data"),
    path('404',views.page_not_found,name="404"),
    path('checkout/<slug:slug>',views.checkout,name="checkout"),
    path('mycourse',views.mycourse,name="mycourse"),
    path('course/watch-course/<slug:slug>',views.watch_course,name="watch_course"),
    path('instructor_list',views.instructor_list,name="instructor_list"),
    path('instrcutor/filter-data',views.instructor_filter_data,name="instructor_filter-data"),
    path('instructor/<int:id>',views.single_instructor,name="single_instructor"),
    # path('instructor/register',instructor_login.register,name="instructor_register"),
    # path('instructor/login',instructor_login.login,name="instructor_login"),
    path('instructor/logout',instructor_login.log_out,name="instructor_logout"),
    path('instructor/home',instructor_login.home,name="instructor_home"),
    path('free',instructor_login.free,name="free"),
    path('instructor/profile/update',instructor_login.profile_update,name="instructor_profile_update"),
    path('instructor/profile',instructor_login.profile,name="instructor_profile"),
    path('instructor/create_course',instructor_login.create_course,name="create_course"),
    path('instructor/course/update/<int:id>',instructor_login.update_course,name="update_course"),
    path('save_lesson/', instructor_login.save_lesson, name='save_lesson'),
    path('instructor/course', instructor_login.instructor_course, name='instructor_course'),
    path('instructor/search_course',instructor_login.instructor_search_course, name="instructor_search_course"),

    path('course/instructor/watch-course/<slug:slug>',instructor_login.instructor_watch_course,name="instructor_watch_course"),

    path('instructor/submit_review/<int:id>',instructor_login.submit_review, name="submit_review"),
    path('course/category/<int:id>',views.trending_category, name="trending_category"),
    path('instrcutor/profile',views.instructor_profile, name="instructor_profile1"),
    
    path('download-pdf/<int:id>', instructor_login.download_pdf, name='download_pdf'),




    



]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)

admin.site.site_header = "E-learning Platform Admin"
admin.site.site_title = "E-learning Platform Admin Portal"
admin.site.index_title = "Welcome to E-learning Platform"



