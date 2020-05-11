from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm,ProfileForm
# Create your views here.


#Handles the registration od the user by recievieng a POST reuest
def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        profileform = ProfileForm(request.POST)
        #checks if the form entered is valid
        if form.is_valid() and profileform.is_valid():
            user = form.save()
            user.profile.date_of_birth = profileform.cleaned_data.get('dob')
            profileform.save(commit=False)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your Account created has been created you can now log in { username }!')
            return redirect('login')
        #if not valid re render and send an error message
    else:
        form = UserRegisterForm()
        profileform = ProfileForm()
    return render(request, 'users/register.html', {'form': form,'profileform': profileform})

#Checks to see if user is logged in
@login_required
def profile(request):
    #Updates the profile details
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST,
                                   request.FILES,
                                   instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('profile')

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    return render(request, 'users/profile.html', context)
