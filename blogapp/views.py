from django.core.mail import send_mail, BadHeaderError
from django.shortcuts import render,redirect,HttpResponse
from .models import Post,Category,Tag
from django.contrib.auth.models import User
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.decorators import login_required
from .utils import paginationProfile
from .forms import CustomUserCreationForm, PostForm,CommentForm,ContactForm

def index(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    tags = Tag.objects.all()
    
    context = {'posts':posts,'categories':categories,'tags':tags}
    return render(request,'blogapp/index.html',context)

def about(request):
    return render(request,'blogapp/about.html')

def loginUser(request):
    page = 'login'
    # if request.user.is_authenticated:
    #     return redirect('index')
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST['password']
        user = authenticate(request, username = username,password = password)
        if user is not None:
            login(request,user)
            return redirect('index')
        else:
            print('Error')
    return render(request,'blogapp/login.html')

def registerUser(request):
    page = 'register'
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('index')
        else:
            print('An error has occured during registration')

    context = {'page':page,'form':form}
    return render(request,'blogapp/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect(loginUser)

def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            first_name= form.cleaned_data['first_name']
            subject= form.cleaned_data['subject']
            email= form.cleaned_data['email_address'] 
            message= form.cleaned_data['message']
            
            #message = "\n".join(body.values())

            try:
                send_mail(subject, message, email, ['admin@example.com']) 
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            return redirect (index)
            
    form = ContactForm()
    return render(request, "blogapp/contact.html", {'form':form})


@login_required(login_url='login')
def createPost(request):
    if not request.user.is_authenticated:
        return redirect(login)
    profile = request.user.profile
    form = PostForm()

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = profile
            post.save()
            return redirect(index)
        else:
            print(form.errors)
    context = {'form':form}
    return render(request,'blogapp/create-post.html',context)

def editPost(request,pk):
    #profile = request.user.profile
    post = Post.objects.get(id=pk)
    form = PostForm(instance=post)

    if request.method == 'POST':
        form = PostForm(request.POST,request.FILES,instance=post)
        if form.is_valid():
            form.save()
        
            return redirect(index)
        else:
            print(form.errors)
    context = {'form':form}
    return render(request,'blogapp/create-post.html',context)


def blog(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    custom_range,posts = paginationProfile(request,posts,4)
    context ={'posts':posts,'custom_range':custom_range,'categories':categories}

    return render(request,'blogapp/blog.html',context)

def categoryView(request,pk):
    category_posts = Post.objects.filter(category=pk)
    posts = Post.objects.all()
    categories = Category.objects.all()
    custom_range,category_posts = paginationProfile(request,category_posts,4)
    context ={'category_posts':category_posts,'custom_range':custom_range,'posts':posts,
                'categories':categories}
    return render(request,'blogapp/categories.html',context)


def post_detail(request,pk):
    categories = Category.objects.all()
    post = Post.objects.get(id=pk)
    comments = post.comments.all()
    comment_form = CommentForm(None)
    print(comments)
    new_comment = None 
    if request.method == 'POST' and request.POST['body']:
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            # Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            # Assign the current post to the comment
            new_comment.post = post
            # Save the comment to the database
            new_comment.save()
            return redirect(post_detail,pk=post.pk)
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()
    posts = Post.objects.all()
    context = {'post':post,'posts':posts ,'comments': comments,
                                           'comment_form': comment_form,
                                           'categories':categories}
    return render(request,'blogapp/post-detail.html',context)
    

def deletePost(request,pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect(index)
    context = {'post':post}
    return render(request,'blogapp/delete.html',context)