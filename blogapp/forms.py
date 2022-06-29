from django.forms import ModelForm
from django import forms
from .models import Profile,Post,Tag,Comment
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name','email','username','password1','password2']
        labels = {
            'first_name':'Name'
        }


    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm,self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs.update({'class':'input100','placeholder':'Name'})
        self.fields['email'].widget.attrs.update({'class':'input100','placeholder':'Email'})
        self.fields['username'].widget.attrs.update({'class':'input100','placeholder':'Username'})
        self.fields['password1'].widget.attrs.update({'class':'input100','placeholder':'Password'})
        self.fields['password2'].widget.attrs.update({'class':'input100','placeholder':'Confirm Password'})


class PostForm(ModelForm):
    options = [(option,option) for option in Tag.objects.all()]
    #tags  = MultipleChoiceField(widget=Select2MultipleWidget,
    #                                     choices=options)
    class Meta:
        model = Post      
        fields = ['title','category','thumbnail','description']#'tags']
        labels = {
            'title': 'Title',
            
        }
        widgets = {
            'description': Textarea(attrs={'class':'form-control','placeholder':'Enter Blog Post','id':'exampleFormControlTextarea1','rows':'10','cols':2}),
            'title' : TextInput(attrs={'placeholder':'Title','label':'Title'}),
            #'category' : TextInput(attrs={'placeholder':'Category'})
        }
        def __init__(self, *args, **kwargs):
            super(CustomUserCreationForm,self).__init__(*args, **kwargs)
            self.fields['title'].widget.attrs.update({'placeholder':'Title'})
            #self.fields['description'].widget.attrs.update({'class':'form-control','placeholder':'Enter Blog Post','id':'exampleFormControlTextarea1','rows':'3'})
           # self.fields['category'].widget.attrs.update({'placeholder':'Username'})
            self.fields['thumbnail'].widget.attrs.update({'placeholder':'Password'})
            self.fields['tags'].widget.attrs.update({'class':'selectpicker'})

class CommentForm(ModelForm):
    class Meta:
        model = Comment
        fields = ('name', 'email', 'body')

class ContactForm(forms.Form):
	first_name = forms.CharField(
        max_length = 50
         )
	subject = forms.CharField(max_length = 250)
	email_address = forms.EmailField(max_length = 150)
	message = forms.CharField(widget = forms.Textarea, max_length = 2000)