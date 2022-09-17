# Django Blog App
Django Blog App – Add Bloging and Commenting to Your Django App

Pre-requisites for Building a Django Blog
In this application, we will require knowledge of the following:

* Django Models
* Django Views
* Django URLs
* Django Templates

## Django Forms

Building our own Django Blog App
Now that we’re all set with the required knowledge, let’s get onto building your first Django blog app today.

### Creating a Django Project and App
The first step is to set-up a new Django project for the application. Hence in the terminal run:
~~~
django-admin startproject <project_name>
~~~
Now ,go inside the project, and run the following line to create a Django app:
~~~
django-admin startapp blogapp
~~~

Register the Django app in the settings.py

### INSTALLED_APPS

Create a new urls.py file in the App and then link it to the project urls.py file. Hence, in project/urls.py, add the code:

~~~
from django.contrib import admin
from django.urls import path,include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('blogapp.urls')),
]
~~~

Also register the models in admin.py file. Add the code in admins.py file:

~~~
from .models import BlogModel, CommentModel
admin.site.register(BlogModel)
admin.site.register(CommentModel)
~~~

### Coding the Django Model
Hence in blogapp/models.py, create two models – BlogModel and CommentModel with the following fields
~~~
from django.db import models
class BlogModel(models.Model):
    id = models.IntegerField(primary_key=True)
    blog_title = models.CharField(max_length=20)
    blog = models.TextField()
 
    def __str__(self):
        return f"Blog: {self.blog_title}"
 
class CommentModel(models.Model):
    your_name = models.CharField(max_length=20)
    comment_text = models.TextField()
    blog = models.ForeignKey('BlogModel', on_delete=models.CASCADE)
     
    def __str__(self):
        return f"Comment by Name: {self.your_name}"
~~~
Note that blog field in CommentModel is linked to the BlogModel since each individual blog page will show only the comments on that blog.

### Coding the Django Forms
We also need Two Forms:
Comment Form to write comments
A Search Form to search for Blogs
Hence, create a forms.py file in blogapp and add the below code in it:
~~~
from django import forms
class CommentForm(forms.Form):
    your_name =forms.CharField(max_length=20)
    comment_text =forms.CharField(widget=forms.Textarea)
 
    def __str__(self):
        return f"{self.comment_text} by {self.your_name}"
 
class SearchForm(forms.Form):
    title = forms.CharField(max_length=20)
~~~

### Coding the Django Views
Again we need Two Views:

ListView: To display the list of Blogs and the search form
Detail View: To display individual Blog, the CommentForm and the previously submitted comments
Hence add the following List View and the Detail View into blogapp/views.py:

~~~
from .models import BlogModel,CommentModel
from .forms import SearchForm,CommentForm
from django.shortcuts import render,redirect
 
def BlogListView(request):
    dataset = BlogModel.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            blog = BlogModel.objects.get(blog_title=title)
            return redirect(f'/blog/{blog.id}')
    else:
        form = SearchForm()
        context = {
            'dataset':dataset,
            'form':form,
        }
    return render(request,'blogapp/listview.html',context)
 
def BlogDetailView(request,_id):
    try:
        data =BlogModel.objects.get(id =_id)
        comments = CommentModel.objects.filter(blog = data)
    except BlogModel.DoesNotExist:
        raise Http404('Data does not exist')
     
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment = CommentModel(your_name= form.cleaned_data['your_name'],
            comment_text=form.cleaned_data['comment_text'],
            blog=data)
            Comment.save()
            return redirect(f'/blog/{_id}')
    else:
        form = CommentForm()
 
    context = {
            'data':data,
            'form':form,
            'comments':comments,
        }
    return render(request,'blogapp/detailview.html',context)
~~~

The URL paths for the Views will be:
~~~
path('blogs/', BlogListView, name='blogs'),
path('blog/<int:_id>', BlogDetailView, name='blog'),
~~~

Add the above code in blogapp/urls.py

### Coding the Django Templates
To display the contents, we again need two templates, one for each View. Hence:

Create a templates folder in the App.
In the templates folder, create a folder with the name: blogapp
Now in the templates/blogapp folder, add the following two- listview.html and detailview.html files.

listview.html file
~~~
<form method="post">
    {%csrf_token %}
    <H2> Search Blog Here</H2>
    {{form.as_p}}
    <input type ="submit" value="Search">
</form>
 
{% for data in dataset %}
<h3>{{data.blog_title}}</h3>
<a href = "{% url 'blog' _id=data.id %}">Read More</a>
<hr/>
{% endfor %}
~~~

### detailview.html file
~~~
<h3>Title:</h3><p>{{data.blog_title}}</p><br>
<h3>Blog</h3>
<p>{{data.blog}}</p>
<hr/>
 
<a href = "{% url 'blogs' %}">Go Back</a>
  
<form method="post">
    {%csrf_token %}
    <H2> Comment Here</H2>
    {{form.as_p}}
    <input type ="submit" value="Comment">
</form>
 
{%for comment in comments%}
<p><strong>{{comment.your_name}}:</strong> {{comment.comment_text}}</p>
{%endfor %}
~~~

The Final Code for the Project
The combined final code for all the files is given below:

models.py
~~~
from django.db import models
class BlogModel(models.Model):
    id = models.IntegerField(primary_key=True)
    blog_title = models.CharField(max_length=20)
    blog = models.TextField()
 
    def __str__(self):
        return f"Blog: {self.blog_title}"
 
class CommentModel(models.Model):
    your_name = models.CharField(max_length=20)
    comment_text = models.TextField()
    blog = models.ForeignKey('BlogModel', on_delete=models.CASCADE)
     
    def __str__(self):
        return f"Comment by Name: {self.your_name}"
~~~

### forms.py
~~~
from django import forms
 
class CommentForm(forms.Form):
    your_name =forms.CharField(max_length=20)
    comment_text =forms.CharField(widget=forms.Textarea)
 
    def __str__(self):
        return f"{self.comment_text} by {self.your_name}"
 
 
 
class SearchForm(forms.Form):
    title = forms.CharField(max_length=20)
~~~

### views.py
~~~
from .models import BlogModel,CommentModel
from .forms import SearchForm,CommentForm
from django.shortcuts import render,redirect
 
def BlogListView(request):
    dataset = BlogModel.objects.all()
    if request.method == 'POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            blog = BlogModel.objects.get(blog_title=title)
            return redirect(f'/blog/{blog.id}')
    else:
        form = SearchForm()
        context = {
            'dataset':dataset,
            'form':form,
        }
    return render(request,'blogapp/listview.html',context)
 
 
def BlogDetailView(request,_id):
    try:
        data =BlogModel.objects.get(id =_id)
        comments = CommentModel.objects.filter(blog = data)
    except BlogModel.DoesNotExist:
        raise Http404('Data does not exist')
     
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            Comment = CommentModel(your_name= form.cleaned_data['your_name'],
            comment_text=form.cleaned_data['comment_text'],
            blog=data)
            Comment.save()
            return redirect(f'/blog/{_id}')
    else:
        form = CommentForm()
 
    context = {
            'data':data,
            'form':form,
            'comments':comments,
        }
    return render(request,'blogapp/detailview.html',context)
~~~

### listview.html
~~~
<html>
<body>
<form method="post">
    {%csrf_token %}
    <H2> Search Blog Here</H2>
    {{form.as_p}}
    <input type ="submit" value="Search">
</form>
 
{% for data in dataset %}
<h3>{{data.blog_title}}</h3>
<a href = "{% url 'blog' _id=data.id %}">Read More</a>
<hr/>
{% endfor %}
</html>
</body>
~~~

### detailview.html
~~~
<html>
<body>
<h3>Title:</h3><p>{{data.blog_title}}</p><br>
<h3>Blog</h3>
<p>{{data.blog}}</p>
<hr/>
 
<a href = "{% url 'blogs' %}">Go Back</a>
 
 
<form method="post">
    {%csrf_token %}
    <H2> Comment Here</H2>
    {{form.as_p}}
    <input type ="submit" value="Comment">
</form>
 
{%for comment in comments%}
<p><strong>{{comment.your_name}}:</strong> {{comment.comment_text}}</p>
{%endfor %}
</html>
</body>
~~~

### blogapp/urls.py
~~~
from django.contrib import admin
from django.urls import path
from .views import *
 
urlpatterns = [
    path('blogs/', BlogListView, name='blogs'),
    path('blog/<int:_id>', BlogDetailView, name='blog'),
]
~~~

### Implementation of the Project
~~~
python3 manage.py migrate
python3 manage.py makemigrations
python3 manage.py migrate
~~~
Now run the server using the terminal:
~~~
python3 manage.py runserver
~~~

Now add a few Blogs via the admin site(“/admin“)
![Alt text](https://www.askpython.com/wp-content/uploads/2020/08/blog-admin-1024x762.png.webp)

Now go to “/blogs” endpoint
![Alt text](https://www.askpython.com/wp-content/uploads/2020/08/blogs-1024x762.png.webp)

Now go to any of the blogs, say Django Hello World
![Alt text](https://www.askpython.com/wp-content/uploads/2020/08/Blog-1-1024x708.png.webp)

Add a comment and hit submit, the comment will appear below
![Alt text](https://www.askpython.com/wp-content/uploads/2020/08/blog-1-with-comment-1024x744.png.webp)

Note that when you go to any other blog, let’s say the Django Views one, you won’t see the above comment since it is only for the Django Hello World Blog.
![Alt text](https://www.askpython.com/wp-content/uploads/2020/08/blog-2-1024x744.png.webp)

## Conclusion
That’s it, coders, this was all about the Django Blog application. Try creating your own Blog app with additional features like user authentication. Do check out the Django User Authentication [article](https://www.askpython.com/django/django-blog-app) for help.
