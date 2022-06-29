from django.db import models
from django.contrib.auth.models import User
import uuid

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,null=True,blank = True)
    name = models.CharField(max_length=200,blank=True,null=True)
    email = models.EmailField(max_length=450,blank=True,null=True)
    username = models.CharField(max_length=200,blank=True,null=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    def __str__(self):
        return self.user.username

class Category(models.Model):
    owner = models.ForeignKey(Profile,on_delete=models.CASCADE,blank=True,null=True)
    name = models.CharField(max_length=200,blank=True,null=True)
    id = models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    class Meta:
        verbose_name = 'Categorie'

    def __str__(self):
        return str(self.name)
    

class Post(models.Model):
    author = models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    description = models.TextField(null=True,blank=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    thumbnail = models.ImageField(null=True,blank=True,upload_to ='images')
    #tags = models.ManyToManyField('Tag',blank=True)
    id = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True,unique=True)

    # def save(self,*args,**kwargs):
    #     super().save(*args, **kwargs)
    #     img = Image.open(self.thumbnail.path)

    #     if (img.height < img.width) or (img.height == 1081 or img.width == 1921):
    #         # output_size = (1920,1080)
    #         # img.thumbnail(output_size,Image.ANTIALIAS)
    #         # #img = img.rotate(270)
    #         # # img = img.resize(output_size)
    #         # img.save(self.thumbnail.path)
    #         (width, height) = img.size
    #         left = int((width - 1000)/2)
    #         right = left + 1000
    #         new_img = img.crop((left, 0, right, height))
    #         new_img = new_img.resize((1000,1000))
    #         new_img = new_img.rotate(-90)
    #         new_img.save(self.thumbnail.path)
    
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.title


# class Tag(models.Model):
#     name = models.CharField(max_length=200)
#     created = models.DateTimeField(auto_now_add=True)
#     id = models.UUIDField(default=uuid.uuid4, unique=True,primary_key=True,editable=False)

#     def __str__(self):
#         return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
