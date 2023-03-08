from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect
from django.urls import reverse_lazy


class CustomLoginView(LoginView):
	template_name = 'login.html'
	redirect_authenticated_user = True
	success_url = reverse_lazy('schemas')


def LogoutView(request):
	logout(request)
	return redirect('login')


def base(request):
	if not request.user.is_authenticated:
		return redirect('login')
	return render(request, 'base.html')
