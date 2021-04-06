from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from django.http import HttpResponse, HttpResponseRedirect
# bring in some things to make auth easier
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
# bring in decorator
from django.contrib.auth.decorators import login_required


# attempt form
from django.forms.models import model_to_dict

# import models
from .models import JobsCat, Jobs, Saved, Note, SavedCat
# access the FeedingForm
from .forms import NoteForm

#### My Imports #####
from script import *


# Create your views here.
def index(request):
    return render(request, 'index.html')

def about(request):
  content = 'something here'
  return HttpResponse(f"<p>{content}</p>")

# def about(request):
#   return render(request, 'about.html')

def contact(request):
    return render(request, 'contact.html')

#####

def jobs_index(request):
  reset = JobsCat.objects.all()
  reset.delete()
  jobs = job_quick_search()
  for name in jobs:
    JobsCat.objects.create(name=name, link=jobs[name])
  jobs_cat = JobsCat.objects.all()
  return render(request, 'jobs/index.html', { 'jobs': jobs_cat })

def jobs_show(request, job_id):
  the_cat = JobsCat.objects.get(id=job_id)
  jobs = get_job_search(the_cat.name)
  reset = Jobs.objects.all()
  reset.delete()
  for job in jobs:
    Jobs.objects.create(category=the_cat.name, name=job, comp=jobs[job][0], link=jobs[job][1])
  all_jobs = Jobs.objects.filter(category=the_cat.name)
  return render(request, 'jobs/show.html', { 
    'the_cat': the_cat,
    'jobs' : all_jobs
  })

def jobs_show_cat(request, cat_id):
  the_cat = SavedCat.objects.get(id=cat_id)
  jobs = get_job_search(the_cat.name)
  reset = Jobs.objects.all()
  reset.delete()
  for job in jobs:
    Jobs.objects.create(category=the_cat.name, name=job, comp=jobs[job][0], link=jobs[job][1])
  all_jobs = Jobs.objects.filter(category=the_cat.name)
  return render(request, 'jobs/show.html', { 
    'the_cat': the_cat,
    'jobs' : all_jobs
  })

def job_detail(request, job_id):
  the_job = Jobs.objects.get(id=job_id)
  all_jobs = Jobs.objects.filter(category=the_job.name)

  return render(request, 'jobs/detail.html', { 
    'jobs' : the_job,
  })

def job_description(request, job_id):
  the_job = Jobs.objects.get(id=job_id)
  the_link = the_job.link
  content = the_detail(the_link)
  return HttpResponse(content)

def saved_job_description(request, job_id):
  the_job = Saved.objects.get(id=job_id)
  the_link = the_job.link
  content = the_detail(the_link)
  return HttpResponse(content)

def save_cat(request, job_id):
  the_cat = JobsCat.objects.get(id=job_id)
  SavedCat.objects.create(name=the_cat.name, user=request.user)
  return redirect('cats_saved')

def save_job(request, job_id):
  the_job = Jobs.objects.get(id=job_id)
  Saved.objects.create(category=the_job.category, name=the_job.name, comp=the_job.comp, link=the_job.link, user=request.user)
  return redirect('jobs_saved')

@login_required()
def jobs_saved(request):
  jobs = Saved.objects.filter(user= request.user)
  return render(request, 'jobs/saved.html', { 'jobs': jobs })

@login_required()
def cats_saved(request):
  cats = SavedCat.objects.filter(user= request.user)
  return render(request, 'jobs/saved_cats.html', { 'cats': cats })

class JobDelete(DeleteView):
  model = Saved
  success_url = '/jobs/saved'

class JobDelete(DeleteView):
  model = SavedCat
  success_url = '/jobs/savedcats'

def selected_job(request, pk):
  the_job = Saved.objects.get(id=pk)
  note_form = NoteForm() 
  return render(request, 'jobs/saved_detail.html', { 'job': the_job , 'note_form': note_form })
 
@login_required()
def add_note(request, pk):
  # this time we are passing the data from our request in that form
  form = NoteForm(request.POST)
  # validate form.is_valid built in
  if form.is_valid():
    # don't save yet!! First lets add out cat_id
    new_note = form.save(commit=False)
    new_note.saved_id = pk
    # cats been added we can save
    new_note.save()
  return redirect('selected_job', pk = pk)


def signup(request):
  error_message = ''
  if request.method == 'POST':
    # This is how to create a 'user' form object
    # that includes the data from the browser
    form = UserCreationForm(request.POST)
    if form.is_valid():
      # This will add the user to the database
      user = form.save()
      # This is how we log a user in via code
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  # A GET or a bad POST request, so render signup.html with an empty form
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)
