from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .forms import UserRegistrationForm, UserTypeForm, ProfileForm
from mine_mgt.models import Claim
from .models import Profile
from django.contrib import messages


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)

        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.balance = 0
            new_user.set_password(form.cleaned_data['password'])
            new_user.is_mine = True
            new_user.save()
            Profile.objects.create(user=new_user)
            login(request, new_user)
            return redirect('mine_mgt:dashboard')

    else:
        form = UserRegistrationForm()

    context = {
        'form': form,
    }

    return render(request, 'registration/register.html', context)


def profile(request):
    user = request.user
    claims = Claim.objects.filter(applicant=user)

    context = {
        'user': user,
        'claims': claims
    }
    

    return render(request, 'accounts/profile.html', context)

def upload_profile(request):
    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
                profile = request.user.profile
                if form.cleaned_data['document1']:
                    profile.document1 = form.cleaned_data['document1']
                if form.cleaned_data['document2']:
                    profile.document2 = form.cleaned_data['document2']
                if form.cleaned_data['document3']:
                    profile.document3 = form.cleaned_data['document3']
                profile.save()

                messages.success(request, "Uploaded successfully")
                return redirect('mine_mgt:dashboard')
        messages.error(request, 'File type not valid')
                 
    else:
         form = ProfileForm()

    return render(request, 'accounts/upload_pdf.html', {'form': form})