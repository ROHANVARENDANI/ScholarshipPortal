from django.db.models import Count, Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect, reverse
from .models import Scholarship, Author, Fieldofstudies
from .forms import CommentForm, PostForm, CreateUserForm
from .filters import ScholarshipFilter
from subscribe.models import Signup
from subscribe.forms import EmailSignupForm
from django.core.mail import send_mail
from datetime import datetime
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout

from django.contrib.auth.decorators import login_required


from django.contrib import messages

form = EmailSignupForm()




def get_author(user):
    qs = Author.objects.filter(user=user)
    if qs.exists():
        return qs[0]
    return None

def search(request):
    queryset = Scholarship.objects.all()
    query = request.GET.get('q')
    if query:
        queryset = queryset.filter(
            Q(title__icontains=query) |
            Q(overview__icontains=query)
        ).distinct()
    context = {
        'queryset': queryset,
    }
    return render(request, 'search_results.html', context)

def index(request):
    featured = Scholarship.objects.filter(featured=True)
    latest = Scholarship.objects.order_by('-timestamp')[0:3]
    
    
    if request.method == "POST":
        email = request.POST["email"]
        new_signup = Signup()
        new_signup.email = email
        new_signup.save()

    context = {
        'object_list' : featured,
        'latest' : latest,
        'form' : form,
        
    }

    return render(request, 'index.html', context)

def scholarships(request):
    scholarship_list = Scholarship.objects.all()
    most_recent = Scholarship.objects.order_by('-timestamp')[:3]
    internships_count = scholarship_list.filter(category='Internships').count()
    scholarships_count = scholarship_list.filter(category='Scholarships').count()
    exchange_programs_count = scholarship_list.filter(category='Exchange Programs').count()

    paginator = Paginator(scholarship_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    
    context = {

        # 'category':scholarship_list,
        'queryset' : paginated_queryset,
        'page_request_var' : page_request_var,
        'most_recent': most_recent,
        'internships_count':internships_count,
        'scholarships_count':scholarships_count,
        'exchange_programs_count':exchange_programs_count,
        # 'category_count':category_count,
        

    }

    return render(request, 'scholarships.html', context)


def internships(request):
    scholarship_list = Scholarship.objects.all()
    internship_list = Scholarship.objects.filter(category='Internships')
    most_recent = Scholarship.objects.order_by('-timestamp')[:3]
    internships_count = scholarship_list.filter(category='Internships').count()
    scholarships_count = scholarship_list.filter(category='Scholarships').count()
    exchange_programs_count = scholarship_list.filter(category='Exchange Programs').count()
    # # category_count = get_category_count()
    paginator = Paginator(internship_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    
    context = {

        'category':internship_list,
        'queryset' : paginated_queryset,
        'page_request_var' : page_request_var,
        'most_recent': most_recent,
        'internships_count':internships_count,
        'scholarships_count':scholarships_count,
        'exchange_programs_count':exchange_programs_count,
         

    }

    return render(request, 'internships.html', context)


def exchange_programs(request):
    scholarship_list = Scholarship.objects.all()
    exchange_program_list = Scholarship.objects.filter(category='Exchange Programs')
    most_recent = Scholarship.objects.order_by('-timestamp')[:3]
    internships_count = scholarship_list.filter(category='Internships').count()
    scholarships_count = scholarship_list.filter(category='Scholarships').count()
    exchange_programs_count = scholarship_list.filter(category='Exchange Programs').count()
    # # category_count = get_category_count()
    paginator = Paginator(exchange_program_list, 4)
    page_request_var = 'page'
    page = request.GET.get(page_request_var)
    try:
        paginated_queryset = paginator.page(page)
    except PageNotAnInteger:
        paginated_queryset = paginator.page(1)
    except EmptyPage:
        paginated_queryset = paginator.page(paginator.num_pages)

    
    context = {

        'category':exchange_program_list,
        'queryset' : paginated_queryset,
        'page_request_var' : page_request_var,
        'most_recent': most_recent,
        'internships_count':internships_count,
        'scholarships_count':scholarships_count,
        'exchange_programs_count':exchange_programs_count,
         

    }

    return render(request, 'internships.html', context)

def post(request, id):
    post = get_object_or_404(Scholarship, id=id)
    most_recent = Scholarship.objects.order_by('-timestamp')[:3]
    internships_count = Scholarship.objects.filter(category='Internships').count()
    scholarships_count = Scholarship.objects.filter(category='Scholarships').count()
    exchange_programs_count = Scholarship.objects.filter(category='Exchange Programs').count()
    form = CommentForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            form.instance.user = request.user
            form.instance.scholarship = post
            form.save()
            return redirect(reverse("scholarship-detail", kwargs={
                'id': post.pk
            }))

    context = {
        'form' : form,
        'post':post,
        'most_recent': most_recent,
        'internships_count':internships_count,
        'scholarships_count':scholarships_count,
        'exchange_programs_count':exchange_programs_count,
    }
    return render(request, 'post.html', context)

def post_create(request):
    title = 'Create'
    form = PostForm(request.POST or None, request.FILES or None)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("scholarship-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)
        


def post_update(request, id):
    title = 'Update'
    post = get_object_or_404(Scholarship, id=id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        instance=post)
    author = get_author(request.user)
    if request.method == "POST":
        if form.is_valid():
            form.instance.author = author
            form.save()
            return redirect(reverse("scholarship-detail", kwargs={
                'id': form.instance.id
            }))
    context = {
        'title': title,
        'form': form
    }
    return render(request, "post_create.html", context)


def post_delete(request, id):
    post = get_object_or_404(Scholarship, id=id)
    post.delete()
    return redirect(reverse("scholarship-list"))

def registerPage(request):
    if request.user.is_authenticated:
        return redirect('index')

    else:

        form = CreateUserForm()

        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')
                
                

        context = {'form':form}
        return render(request, 'register.html', context)

def loginPage(request):

    if request.user.is_authenticated:
        return redirect('index')

		
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            #username is coming from the html
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)
            #It will authenticate user itself
            #if user is there thn login in and redirect to index page
            if user is not None:
                login(request, user)
                return redirect('index')
            else: 
                messages.info(request, "Username Or Password is incorrect")


        context = {}
        return render (request, 'login.html', context)

def logoutUser(request):
	logout(request)
	return redirect('index')

def contactPage(request):
    if request.method == 'POST':
        message_name = request.POST['message-name']
        message_email = request.POST['message-email']
        message_subject= request.POST['message-subject']
        message=request.POST['message']

        #send an email:
        # send_mail(
        #     message_subject, #subject
        #     message, 
        #     message_email, #from email
        #     [''], # [rohan.varendani@gmail.com], #toEmail

        # )

        return render (request, 'contact.html', {'message_name':message_name})
    else:
	    return render (request, 'contact.html', {})

def is_valid_queryparam(param):
    return param != '' and param is not None


def filterView(request):
    qs = Scholarship.objects.all()
    fieldofstudies=Fieldofstudies.objects.all()
    title_contains_query = request.GET.get('title_contains')
    financialcoverage_query=request.GET.get('financialcoverage')
    deadline_query1=request.GET.get('deadline1')
    # deadline_query2=request.GET.get('deadline2')
    date_min = request.GET.get('date_min')
    date_max = request.GET.get('date_max')
    field = request.GET.get('field')
    
    # dat=datetime.now().date() - timedelta(days=14)
    # print(dat)
    # new=datetime.now().date() - timedelta(days=7)
    # print(new)

    # samples = Scholarship.objects.filter(end_date__gte=datetime.now().date() - timedelta(days=7),
    #                             end_date__lte=datetime.now().date())
    # print(samples)

    if is_valid_queryparam(title_contains_query):
        qs=qs.filter(title__icontains=title_contains_query)
        
    elif is_valid_queryparam(financialcoverage_query) and financialcoverage_query != 'Choose...':

        qs=qs.filter(Q(financial_coverage__icontains=financialcoverage_query)).distinct()
        
         
    if is_valid_queryparam(deadline_query1) and deadline_query1 != 'Choose...':
        qs=Scholarship.objects.filter(end_date__gte=datetime.now().date() - timedelta(days=7),
                                end_date__lte=datetime.now().date())
        print(" These are for range of 7 ", qs)

    # if is_valid_queryparam(deadline_query2):
    #     qs=Scholarship.objects.filter(end_date__gte=datetime.now().date() - timedelta(days=14),
    #                             end_date__lte=datetime.now().date()-timedelta(days=7))
    #     print(" These are for range of 14 ", qs)
   

        
    if is_valid_queryparam(date_min):
        qs = qs.filter(timestamp__gte=date_min)

    if is_valid_queryparam(date_max):
        qs = qs.filter(timestamp__lt=date_max)

    # if is_valid_queryparam(field) and field != 'Choose...':
    #     fieldofstudies = qs.filter(field_of_studies__title=field)
    #     print(fieldofstudies)


    if is_valid_queryparam(field) and field != 'Choose...': 
        qs=qs.filter(Q(field_of_studies__title__icontains=field)).distinct()
        

    
    context = {

        'queryset':qs,
        
        
        
    }
    return render(request, 'filters.html', context)



    