from django.contrib.auth import password_validation
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.shortcuts import reverse, redirect, render
from django.views import generic
from django.views.decorators.csrf import csrf_protect
from django.views.generic.edit import FormMixin
from .forms import CommentForm
from .models import Post, Comment
from django.contrib import messages

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

    # def get_success_url(self):
    #     return reverse("post", kwargs={"pk": self.object.pk})

    def test_func(self):
        return self.get_object().user == self.request.user


@csrf_protect
def register(request):
    if request.method == "POST":
        # pasiimame reikšmes iš registracijos formos
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # tikriname, ar sutampa slaptažodžiai
        if password == password2:
            # tikriname, ar neužimtas username
            if User.objects.filter(username=username).exists():
                messages.error(request, f'Vartotojo vardas {username} užimtas!')
                return redirect('register')
            else:
                # tikriname, ar nėra tokio pat email
                if User.objects.filter(email=email).exists():
                    messages.error(request, f'Vartotojas su el. paštu {email} jau užregistruotas!')
                    return redirect('register')
                else:
                    try:
                        password_validation.validate_password(password)
                    except password_validation.ValidationError as e:
                        for error in e:
                            messages.error(request, error)
                        return redirect('register')

                    # jeigu viskas tvarkoje, sukuriame naują vartotoją
                    User.objects.create_user(username=username, email=email, password=password)
                    messages.info(request, f'Vartotojas {username} užregistruotas!')
                    return redirect('login')
        else:
            messages.error(request, 'Slaptažodžiai nesutampa!')
            return redirect('register')
    return render(request, 'registration/register.html')