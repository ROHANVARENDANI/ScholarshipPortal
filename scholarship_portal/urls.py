from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf.urls import url
from django.contrib.auth.forms import UserCreationForm

from Scholarship.views import index, scholarships, internships, exchange_programs, post, search, filterView, post_create, post_update, post_delete, registerPage, loginPage, logoutUser, contactPage

from subscribe.views import email_list_signup




urlpatterns = [
    path('admin/', admin.site.urls),
    path('', index, name='index'),
    path('scholarships/', scholarships, name='scholarship-list'),
    path('filter/', filterView, name='filter'),
    path('internships/', internships, name='internship-list'),
    path('exchange_programs/', exchange_programs, name='exchange_program-list'),
    path('search/', search, name='search'),
    path('contact/', contactPage, name='contact'),
    path('register/', registerPage, name="register"),
	path('login/', loginPage, name="login"),  
	path('logout/', logoutUser, name="logout"),
    path('email-signup/', email_list_signup, name='email-list-signup'),
    path('post/<id>/', post, name='scholarship-detail'),
    path('create/', post_create, name='scholarship-create'),
    path('post/<id>/update/', post_update, name='scholarship-update'),
    path('post/<id>/delete/', post_delete, name='scholarship-delete'),
    path('tinymce/', include('tinymce.urls')),
    # path('chat/', include('chat.urls', namespace='chat')),
    path('chat/', include('django_chatter.urls')),
]


if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)