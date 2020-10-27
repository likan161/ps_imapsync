from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django import forms
from django.shortcuts import render
import subprocess
import time
from django.shortcuts import redirect
from django.urls import reverse
from validate_email import validate_email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def emailcheck(mail, pas, host):
    if validate_email(mail):
        try:
            server = smtplib.SMTP(host)
            server.starttls()
            server.login(mail, pas)
            return(True)
        except:
            return(False)

def TestFinishOk(file):
    f_read = open(file, "r")
    last_line = f_read.readlines()[-1]
    if last_line.rstrip() == "Exiting with return value 0 (EX_OK: successful termination) 0/50 nb_errors/max_errors":
        return str(True)

def index(request):
        return render(request, "index.html")

def test(request):
        return render(request, "test.html")

class NameForm(forms.Form):
        mail1 = forms.CharField(max_length=50)
        pass1 = forms.CharField(max_length=50)
        host1 = forms.CharField(max_length=50)
        ssl1 = forms.CharField(max_length=50,required=False)
        mail2 = forms.CharField(max_length=50)
        pass2 = forms.CharField(max_length=50)
        host2 = forms.CharField(max_length=50)
        ssl2 = forms.CharField(max_length=50,required=False)


def get_form(request):
    if request.method == 'POST':

        form= NameForm(request.POST)
        if form.is_valid():
            mail1= form.cleaned_data.get("mail1")
            pass1= form.cleaned_data.get("pass1")
            host1= form.cleaned_data.get("host1")
            ssl1= form.cleaned_data.get("ssl1")
            mail2= form.cleaned_data.get("mail2")
            pass2= form.cleaned_data.get("pass2")
            host2= form.cleaned_data.get("host2")
            ssl2= form.cleaned_data.get("ssl2")

            if not emailcheck(mail1, pass1, host1):
                data = {"mail1auth": True}
                return render(request,'index.html', context=data)
                
            if not emailcheck(mail2, pass2, host2):
                data = {"mail2auth": True}
                return render(request,'index.html', context=data)

            ImapSyncRun = "sudo /usr/bin/imapsync --maxsize 10000000000000000000000 --automap --no-modulesversion --nolog --host1 {0} --user1 {1} --password1 {2} --host2 {3} --user2 {4} --password2 {5}".format(host1,mail1,pass1,host2,mail2,pass2)

            if ssl1 == "adventure":
                ImapSyncRun = ImapSyncRun + " --ssl1"

            if ssl2 == "adventure":
                ImapSyncRun = ImapSyncRun + " --ssl2"

            Command = subprocess.run(ImapSyncRun.split(), stdout=subprocess.PIPE)

            FileName = "logs/" + time.strftime("%Y%m%d-%H%M%S") + "-" + mail1 + "-" + mail2 + ".log"
            file = open(FileName,'w')
            file.write(Command.stdout.decode("utf-8"))
            file.close()
             
            if TestFinishOk(FileName):
                FileName = "http://kvs02.likan.space/" + FileName
                data = {"transfer": True, "FileName": FileName}
                return render(request,'index.html', context=data)
#               return HttpResponse(a)
            else:
                data = {"transfer": "false", "FileName": FileName}
                return render(request,'index.html', context=data)


        else:
            data = {"NoData": True}
            return render(request,'index.html', context=data)
    else:
         return render(request,'index.html')
