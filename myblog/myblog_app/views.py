from django.contrib import auth, messages
from django.forms.forms import Form
from django.shortcuts import render, redirect
from django.urls.base import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, RedirectView
from django.urls import reverse
# from django.views.generic.edit import FormView
from .forms import UserCreationForm, NewUserForm
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.forms import AuthenticationForm, PasswordResetForm
from django.contrib.auth import REDIRECT_FIELD_NAME, login, authenticate, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from .comment import CommentForm
from .models import Post, Comment
from django.shortcuts import render, get_object_or_404


from .models import Post

# Create your views here.

class BlogListView(ListView):
  model = Post
  template_name = 'home.html'
  
class BlogDetailView(DetailView):
  model = Post
  template_name = 'post_detail.html'
  
class BlogCreateView(CreateView):
  model = Post
  template_name = 'post_new.html'
  fields = ['title', 'author', 'body']
  
class BlogUpdateView(UpdateView):
  model = Post
  template_name = 'post_edit.html'
  fields = ['title', 'body']
  
class BlogDeleteView(DeleteView):
  model = Post
  template_name = 'post_delete.html'
  success_url = reverse_lazy('home')
  
class SignUpView(SuccessMessageMixin, CreateView):
  template_name = 'register.html'
  success_url = reverse_lazy('login')
  form_class = UserCreationForm
  success_message = 'Your profile was created successfully'


def login_request(request):
  if request.method == "POST":
    form = AuthenticationForm(request, data=request.POST)
    if form.is_valid():
      username = form.cleaned_data.get('username')
      password = form.cleaned_data.get('password')
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        messages.info(request, f'You are logged in as {username}.')
        return redirect('home')
      else:
        messages.error(request, 'Invalid username or password.')
    else:
      messages.error(request, 'Invalid username or password.')
  form = AuthenticationForm()
  return render(request=request, template_name='login.html', context={'form':form})
    
# class LoginView(FormView):
#   template_name = 'login.html'
#   form_class = AuthenticationForm
#   success_url = reverse_lazy('home')
#   redirect_field_name = REDIRECT_FIELD_NAME
  
  # @method_decorator(sensitive_post_parameters('password'))
  # @method_decorator(csrf_protect)
  # @method_decorator(never_cache)
  # def dispatch(self, request, *args, **kwargs):
  #     # Sets a test cookie to make sure the user has cookies enabled
  #     request.session.set_test_cookie()

  #     return super(LoginView, self).dispatch(request, *args, **kwargs)

  # def form_valid(self, form):
  #     login(self.request, form.get_user())

  #     # If the test cookie worked, go ahead and
  #     # delete it since its no longer needed
  #     if self.request.session.test_cookie_worked():
  #         self.request.session.delete_test_cookie()

  #     return super(LoginView, self).form_valid(form)

  # def get_success_url(self):
  #     redirect_to = self.request.REQUEST.get(self.redirect_field_name)
  #     if not is_safe_url(url=redirect_to, host=self.request.get_host()):
  #         redirect_to = self.success_url
  #     return redirect_to

# class LogoutView(RedirectView):
#   success_url = reverse_lazy('login')
#   def get(self, request, *args, **kwargs):
#     auth_logout(request)
#     return super(LogoutView, self).get(request, *args, **kwargs)

def logout_request(request):
  logout(request)
  messages.info(request, 'You have successfully logout')
  return redirect('login')


def password_reset_request(request):
	if request.method == "POST":
		password_reset_form = PasswordResetForm(request.POST)
		if password_reset_form.is_valid():
			data = password_reset_form.cleaned_data['email']
			associated_users = User.objects.filter(Q(email=data))
			if associated_users.exists():
				for user in associated_users:
					subject = "Password Reset Requested"
					email_template_name = "password/password_reset_email.txt"
					c = {
					"email":user.email,
					'domain':'127.0.0.1:8000',
					'site_name': 'Website',
					"uid": urlsafe_base64_encode(force_bytes(user.pk)),
					"user": user,
					'token': default_token_generator.make_token(user),
					'protocol': 'http',
					}
					email = render_to_string(email_template_name, c)
					try:
						send_mail(subject, email, 'admin@example.com' , [user.email], fail_silently=False)
					except BadHeaderError:
						return HttpResponse('Invalid header found.')
					return redirect ("/password_reset/done/")
	password_reset_form = PasswordResetForm()
	return render(request=request, template_name="password/password_reset.html", context={"form":password_reset_form})



def comment_detail(request, slug):
    template_name = 'comment.html'
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
    else:
        comment_form = CommentForm()

    return render(request, template_name, context={'post': post,
                                           'comments': comments,
                                           'new_comment': new_comment,
                                           'comment_form': comment_form})