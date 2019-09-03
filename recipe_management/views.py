# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect

# Create your views here.


def home(request):
    if request.GET.get('btn_admin'):
        return redirect('/admin')
    elif request.GET.get('btn_user_apis'):
        return redirect('/user-apis')
    elif request.GET.get('btn_recipe_management_apis'):
        return redirect('/recipe-management-apis')
    elif request.GET.get('btn_change_password'):
        return redirect('/user-apis/change-password-view/')
    else:
        return render(request, 'index.html')
