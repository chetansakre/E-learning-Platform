from django import forms
from django.forms import inlineformset_factory
from django.contrib.auth import get_user_model


from myapp.models import*

class AuthorLoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget = forms.PasswordInput)

# image field

# class CourseForm(forms.ModelForm):
#     class Meta:
#         model = Course
#         fields = ['featured_image', 'featured_video', 'title', 'author', 'category', 'level', 'description', 'price', 'language', 'deadline', 'discount', 'slug', 'status', 'certificate']

    # def __init__(self, *args, **kwargs):
    #     super(CourseForm, self).__init__(*args, **kwargs)
    #     # Example of populating choices for a select field (assuming `Level` model)
    #     self.fields['level'].queryset = Level.objects.all()
    #     # self.fields['author'].queryset = Author.objects.all()
    #     self.fields['category'].queryset = Categories.objects.all()
    #     self.fields[''].queryset = Categories.objects.all()

class WhatYouLearnForm(forms.ModelForm):
    class Meta:
        model = What_you_learn
        fields = ['points']

WhatYouLearnFormSet = inlineformset_factory(Course, What_you_learn,form= WhatYouLearnForm, extra=1,can_delete=False)
        


class RequirementsForm(forms.ModelForm):
    class Meta:
        model = Requirements
        fields = ['points']

RequirementsFormSet = inlineformset_factory(Course, Requirements, form=RequirementsForm, extra=1,can_delete=False)

# class LessonForm(forms.ModelForm):
#     class Meta:
#         model = Lesson
#         fields = ['name']

# LessonFormSet = inlineformset_factory(Course, Lesson, form=LessonForm, extra=1,can_delete=False)

class VideoForm(forms.ModelForm):

    lesson_name = forms.CharField(max_length=200, required=False)  # New lesson name field
    material = forms.FileField(required=False, widget=forms.FileInput(attrs={'placeholder': 'Upload material file'}))

    class Meta:
        model = Video
        fields = ['serial_number', 'thumbnail', 'lesson_name','title', 'youtube_id', 'time_duration', 'preview']

    

VideoFormSet = inlineformset_factory(Course, Video, form=VideoForm, extra=1,can_delete=False)


# WhatYouLearnFormSet = inlineformset_factory(Course, What_you_learn,form= WhatYouLearnForm, extra=1)
# RequirementsFormSet = inlineformset_factory(Course, Requirements,form= RequirementsFormSet, extra=1)
# LessonFormSet = inlineformset_factory(Course, Lesson,form= LessonFormSet, extra=1)
# VideoFormSet = inlineformset_factory(Course, Video, form= VideoForm, extra=1)

class CourseForm(forms.ModelForm):
    category = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'placeholder': 'i.e. Python , PHP etc.','name':'category'}))

    class Meta:
        model = Course
        fields = ['featured_image', 'featured_video', 'title', 'level', 'description', 'price', 'language', 'deadline', 'discount',  'status', 'certificate']



