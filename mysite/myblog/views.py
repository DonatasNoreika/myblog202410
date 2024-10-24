from django.contrib.auth import password_validation
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import reverse, redirect, render
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin
from .forms import CommentForm, UserUpdateForm, ProfileUpdateForm
from .models import Post, Comment
from django.contrib import messages
from django.utils.translation import gettext as _

# Create your views here.

class PostListView(generic.ListView):
    model = Post
    template_name = "posts.html"
    context_object_name = "posts"
    paginate_by = 5


class PostDetailView(FormMixin, generic.DetailView):
    model = Post
    template_name = "post.html"
    context_object_name = "post"
    form_class = CommentForm

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.id})

    def form_valid(self, form):
        form.instance.post = self.object
        form.instance.user = self.request.user
        form.save()
        return super().form_valid(form)

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class UserPostListView(LoginRequiredMixin, generic.ListView):
    model = Post
    template_name = "userposts.html"
    context_object_name = "posts"

    def get_queryset(self):
        return Post.objects.filter(user=self.request.user)

class UserCommentListView(LoginRequiredMixin, generic.ListView):
    model = Comment
    template_name = "usercomments.html"
    context_object_name = "comments"

    def get_queryset(self):
        return Comment.objects.filter(user=self.request.user)


class CommentUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Comment
    template_name = "comments_form.html"
    fields = ['content']

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.get_object().user == self.request.user


class CommentDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Comment
    template_name = "comments_delete.html"
    context_object_name = "comment"

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.post.pk})

    def test_func(self):
        return self.get_object().user == self.request.user


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    model = Post
    template_name = "post_form.html"
    fields = ['title', 'content']
    success_url = "/userposts/"

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, generic.UpdateView):
    model = Post
    template_name = "post_form.html"
    fields = ['title', 'content']

    def get_success_url(self):
        return reverse("post", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.get_object().user == self.request.user

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, generic.DeleteView):
    model = Post
    template_name = "post_delete.html"
    context_object_name = "post"
    success_url = "/"

    def test_func(self):
        return self.get_object().user == self.request.user


@csrf_protect
def register(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        if password == password2:
            if User.objects.filter(username=username).exists():
                # messages.error(request, f"Vartotojas vardas {username} užimtas!")
                messages.error(request, _('Username %s already exists!') % username)
                return redirect("register")
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, _('Email %s already exists!') % email)
                    return redirect("register")
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as err:
                        for error in err:
                            messages.error(request, error)
                        return redirect("register")
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, _('User %s registered!') % username)
                    return redirect("login")

        else:
            messages.error(request, _('Passwords do not match!'))
            return redirect("register")
    return render(request, template_name="registration/register.html")

@login_required
def profile(request):
    if request.method == "POST":
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        new_email = request.POST['email']
        if new_email == "":
            messages.error(request, _("Email cannot be empty"))
            return redirect('profile')
        if request.user.email != new_email and User.objects.filter(email=new_email).exists():
            messages.error(request, _('User with e-mail %s already registered!!') % new_email)
            return redirect('profile')
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.info(request, _('Profile updated!'))
            return redirect('profile')


    u_form = UserUpdateForm(instance=request.user)
    p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, "profile.html", context=context)