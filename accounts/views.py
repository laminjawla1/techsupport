from django.shortcuts import render, redirect
from django.contrib.auth.forms import *
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import AccountUpdateForm, UserUpdateForm

@login_required
def account(request):
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        account_form = AccountUpdateForm(request.POST, request.FILES, instance=request.user.account)

        if user_form.is_valid() and account_form.is_valid():
            user_form.save()
            account_form.save()

            messages.success(request, "Account updated successfully 😊")
            return redirect('account')

    else:
       user_form = UserUpdateForm(instance=request.user)
       account_form = AccountUpdateForm(instance=request.user.account) 

    return render(request, 'accounts/profile.html', {
        'user_form': user_form,
        'account_form': account_form
    })
