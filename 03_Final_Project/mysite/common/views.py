from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from common.forms import UserForm, ProfileForm, UserUpdateForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages



def signup(request):
    # 회원가입
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'common/signup.html', {'form': form})

@login_required(login_url='common:login')
def profile(request):
    # 프로필 확인
    context = {'user': request.user }
    return render(request, 'common/profile.html', context)

@login_required(login_url='common:login')
def edit_profile(request):
    # 프로필 편집
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, '프로필이 설공적으로 업데이트 되었습니다.')
            return redirect('common:profile')
    
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)

    context = {
        'user_form' : user_form,
        'profile_form' : profile_form
    }

    return render(request, 'common/edit_profile.html', context)

def page_not_found(request, exception):
    # 404 page not found
    return render(request, 'common/404.html', {})