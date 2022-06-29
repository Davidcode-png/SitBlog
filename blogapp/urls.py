from django.urls import path
from .views import index,about,post_detail,loginUser,registerUser,logoutUser,createPost,editPost,blog,categoryView,contact,deletePost
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('',index,name='index'),
    path('about/',about,name='about'),
    path('login/',loginUser,name='login'),
    path('register/',registerUser,name='register'),  
    path('logout/',logoutUser,name='logout'),
    path('create-post/',createPost,name='create'),
    path('blog/',blog,name='blog'),
    path('contact/',contact,name='contact'),
    path('category/<str:pk>/',categoryView,name='category'),
    path('delete/<str:pk>',deletePost,name='delete'),
    path('edit-post/<str:pk>/',editPost,name='edit'),

    path('<str:pk>/',post_detail,name='post_detail'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
