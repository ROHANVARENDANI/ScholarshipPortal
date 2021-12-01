from django.db import models
from django.contrib.auth import get_user_model
from django.urls import reverse
from tinymce import HTMLField

# Create your models here.

User = get_user_model() #This method will return the currently active User model – the custom User model if one is specified, or User otherwise.

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) #this is one to one field with the user provided by django, CASCADE: When the referenced object is deleted,
    # also delete the objects that have references to it.
    profile_picture = models.ImageField()

    def __str__(self): #This method will convert obj to string and will return username.
        return self.user.username

class Fieldofstudies(models.Model):

     title = models.CharField(max_length=20)

     def __str__(self):
         return self.title

class Scholarship(models.Model):
    CATEGORY = (
                ('Internships','Internships'),
                ('Exchange Programs', 'Exchange Programs'),
                ('Scholarships', 'Scholarships'),
			    ) 
    author = models.ForeignKey(Author, on_delete=models.CASCADE)    
    title = models.CharField(max_length=200)
    overview = models.TextField()
    content = HTMLField()
    timestamp = models.DateTimeField(auto_now_add=True)
    #comment_count = models.IntegerField(default = 0)
    start_date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    financial_coverage=models.CharField(max_length=100)
    No_of_scholarships = models.IntegerField()
    thumbnail = models.ImageField()
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    field_of_studies = models.ManyToManyField(Fieldofstudies, blank=True)
    featured = models.BooleanField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("scholarship-detail", kwargs={"id": self.id})

    def get_update_url(self):
        return reverse('scholarship-update', kwargs={'id': self.id})

    def get_delete_url(self):
        return reverse('scholarship-delete', kwargs={'id': self.id})

    def deadline_in_week(self):
        end_date=datetime.now().date() + timedelta(days=7)
        return self.end_date
    # def deadline_in_month(self):
    #     end_date=datetime.now().date() + timedelta(days=30)
    #     return self.end_date

    @property
    def get_comments(self):
        return self.comments.all().order_by('-timestamp')

    @property
    def comment_count(self):
        return Comment.objects.filter(scholarship=self).count()

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    content = models.TextField()
    scholarship = models.ForeignKey(Scholarship, related_name='comments', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username