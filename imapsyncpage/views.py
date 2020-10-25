from django.http import HttpResponse
from django import forms
from django.shortcuts import render
import subprocess
import time

def index(request):
        return render(request, "index.html")

class NameForm(forms.Form):
        mail1 = forms.CharField(label='Your mail1', max_length=20)
        pass1 = forms.CharField(label='Your pass1', max_length=20)
        host1 = forms.CharField(label='Your host1', max_length=20)
        mail2 = forms.CharField(label='Your mail2', max_length=20)
        pass2 = forms.CharField(label='Your pass2', max_length=20)
        host2 = forms.CharField(label='Your host2', max_length=20)

def get_form(request):
    submitbutton= request.POST.get("submit") 
    if request.method == 'POST':
        form= NameForm(request.POST)
        
        if form.is_valid():
            mail1= form.cleaned_data.get("mail1")
            pass1= form.cleaned_data.get("pass1")
            host1= form.cleaned_data.get("host1")
            mail2= form.cleaned_data.get("mail2")
            pass2= form.cleaned_data.get("pass2")
            host2= form.cleaned_data.get("host2")

            FileName = "logs/" + time.strftime("%Y%m%d-%H%M%S") + "_" + mail1 + "_" + mail2 + ".log"

            transfer = subprocess.run(['sudo', '/usr/bin/imapsync', '--no-modulesversion', '--nolog', '--host1', host1, '--user1', mail1, '--password1', pass1, '--host2', host2, '--user2', mail2, '--password2', pass2], stdout=subprocess.PIPE)

            file = open(FileName,'w')
            file.write(transfer.stdout.decode("utf-8"))
            file.close()

            FileName = "http://kvs02.likan.space/" + FileName
            return HttpResponse(FileName)
