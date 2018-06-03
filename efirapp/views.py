from .forms import *
from django.shortcuts import render,redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import *
from django.template.loader import get_template
from django.http import HttpResponse
from .filters import *
import requests
from django.views.generic.edit import CreateView,DeleteView,UpdateView
from django.urls import reverse

def home(request):
    template = get_template("home.html")
    return HttpResponse(template.render())

def record(request):
    template = get_template("test.html")
    return HttpResponse(template.render())

def track_login(request):
    template = get_template("complaint_list.html")
    if request.method == 'POST':
        form = TrackForm(request.POST)
        if form.is_valid():
            url = 'https://ext.digio.in:444/test/otpkyc'
            PARAMS = {'aadhaar_id': request.POST.get('aadhaar_id'), 'otp': request.POST.get('otp'), 'txn_id': request.POST.get('txn_id')}
            response = requests.post(url, json=PARAMS)
            if response.status_code == 200:
                list = Complaint.objects.filter(aadhar_no_id=request.POST.get('aadhaar_id'))
                return HttpResponse(template.render(context={'list': list}))
            else:
                return HttpResponse("Wrong credentials")
        else:
            return HttpResponse("Invalid form")
    else:
        form = TrackForm()
        return render(request, 'complaint_login.html', {
            'form': form
        })

class statusupdateview(UpdateView):
    model = Status
    fields = ('status','comments',)

    def get_success_url(self):
        return reverse("search")

    def get_object(self, queryset=None):
        id = self.kwargs.get('fir_id')
        result = Status.objects.all().get(fir_id_id=id)
        return result


def complain_login(request):
    template = get_template("data.html")
    if request.method == 'POST':
        form = AdForm(request.POST)
        list = Aadhar.objects.filter(aadhaar_id=request.POST.get('aadhaar_id'))
        if len(list) > 0:
            return HttpResponse(template.render(context={'list': list}))
        if form.is_valid():
            url = 'https://ext.digio.in:444/test/otpkyc'
            PARAMS = {'aadhaar_id': request.POST.get('aadhaar_id'), 'otp': request.POST.get('otp'), 'txn_id': request.POST.get('txn_id')}
            response = requests.post(url, json=PARAMS)
            if response.status_code == 200:
                try:
                    data = response.json()
                except:
                    return HttpResponse("Data load error")

                input_instance = form.save(commit=False)
                input_instance.name = data['kyc_data']['name']
                input_instance.dob= data['kyc_data']['date_of_birth']
                input_instance.gender = data['kyc_data']['gender']
                input_instance.phone = data['kyc_data']['phone']
                input_instance.email = data['kyc_data']['email']
                add= data['kyc_data']['address']['care_of']+" " +data['kyc_data']['address']['house'] +" "+ data['kyc_data']['address']['street'] +" "+ data['kyc_data']['address']['locality']+" " +data['kyc_data']['address']['village_town_or_city'] + " " +data['kyc_data']['address']['sub_district'] + " "+ data['kyc_data']['address']['district']+" "+data['kyc_data']['address']['state'] + " "+ data['kyc_data']['address']['country'] + " "+ data['kyc_data']['address']['pincode']
                input_instance.address = add
                input_instance.save()
                list = Aadhar.objects.filter(aadhaar_id=request.POST.get('aadhaar_id'))
                return HttpResponse(template.render(context={'list': list}))
            else:
                return HttpResponse("Wrong credentials.")

    else:
        form = AdForm()
    return render(request, 'complaint_login.html', {
        'form': form
    })

def complain_file(request,aadhaar_id,otp):
    row = Aadhar.objects.filter(aadhaar_id=aadhaar_id)
    x = row.values('otp')[0]['otp']
    if str(x)!=otp:
        return HttpResponse(otp + str(x) )
    if request.method == 'POST':
        form = ComplaintForm(request.POST, request.FILES)
        if form.is_valid():
            input_instance = form.save(commit=False)
            input_instance.aadhar_no = Aadhar(aadhaar_id=aadhaar_id)
            input_instance.save()
            list = Complaint.objects.filter(aadhar_no_id=aadhaar_id)
            return render(request, 'complaint_list.html', {
        'list': list
    })
    else:
        form = ComplaintForm()
    return render(request, 'complaint_upload.html', {
        'form': form
    })


def status(request,fir_id):
    a = Status.objects.filter(fir_id_id=fir_id)
    #status = dict(TYPE_CHOICES).get(a.values('status')[0]['status'])
    status = int(a.values('status')[0]['status'])
    comment = a.values('comments')[0]['comments']
    return render(request, 'track.html', {
        'fir_id' :fir_id, 'status':status, 'comments' :comment
    })

def load_cities(request):
    state_id = request.GET.get('state')
    cities = City.objects.filter(state_id=state_id).order_by('name')
    return render(request, 'city_dropdown_list_options.html', {'cities': cities})


def search(request):
    list = Complaint.objects.all().prefetch_related('status_set')

    filter = CompFilter(request.GET, queryset=list)
    return render(request, 'comp_list.html', {'filter': filter})

def aadhar(request,aadhaar_id):
    data = Aadhar.objects.filter(aadhaar_id=aadhaar_id)
    return render(request, 'aadhar.html', {'list': data})


def statecreate(request):
    if request.method == 'POST':
        form = StateForm(request.POST, )
        if form.is_valid():
            form.save()
    else:
        form = StateForm()
    return render(request, 'state_form.html', {
        'form': form
    })




def cityview(request):
    if request.method == 'POST':
        form = CityForm(request.POST, )
        if form.is_valid():
            form.save()
    else:
        form = CityForm()
    return render(request, 'efirapp/city_form.html', {
        'form': form
    })