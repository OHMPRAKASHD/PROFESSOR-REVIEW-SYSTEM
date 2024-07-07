from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm
from .models import Teacher, Review
from django.views import View
from .forms import ReviewForm
from django.shortcuts import get_object_or_404
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.db.models import Avg
from .forms import DiscussionForm, DiscussionReplyForm
from .models import Teacher, Review, Discussion, DiscussionReply
from django.views.generic import ListView

def home(request):
    return render(request,'home.html')

def dashboard(request):
    return render(request,'dashboard.html')

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'registration/register.html', {'form': form})

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required
def teacher_list(request):
    teachers = Teacher.objects.all()
    return render(request, 'teacher_list.html', {'teachers': teachers})


@login_required
def teacher_detail(request, teacher_id):
    teacher = Teacher.objects.get(pk=teacher_id)
    reviews = Review.objects.filter(teacher=teacher)
    average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
    # Pass the average_rating to the template context
    return render(request, 'teacher_detail.html', {'teacher': teacher, 'reviews': reviews, 'average_rating': average_rating})

class AddReviewView(View):
    template_name = 'add_review.html'

    def get(self, request, teacher_id):
        teacher = Teacher.objects.get(pk=teacher_id)
        # Check if the user has already reviewed the teacher
        existing_review = Review.objects.filter(teacher=teacher, user=request.user).first()

        if existing_review:
            # If the user has already reviewed, you can redirect them to the edit review page
            return redirect('edit_review', teacher_id=teacher.id, review_id=existing_review.id)

        form = ReviewForm()
        return render(request, self.template_name, {'teacher': teacher, 'form': form})

    def post(self, request, teacher_id):
        teacher = Teacher.objects.get(pk=teacher_id)
        # Check if the user has already reviewed the teacher
        existing_review = Review.objects.filter(teacher=teacher, user=request.user).first()

        if existing_review:
            # If the user has already reviewed, you can redirect them to the edit review page
            return redirect('edit_review', teacher_id=teacher.id, review_id=existing_review.id)

        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.teacher = teacher
            review.save()
            return redirect('teacher_detail', teacher_id=teacher.id)
        return render(request, self.template_name, {'teacher': teacher, 'form': form})

    

class TeacherDetailView(View):
    template_name = 'teacher_detail.html'

    def get(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        reviews = Review.objects.filter(teacher=teacher)
        form = ReviewForm()
        return render(request, self.template_name, {'teacher': teacher, 'reviews': reviews, 'form': form})

    def post(self, request, teacher_id):
        teacher = get_object_or_404(Teacher, pk=teacher_id)
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.user = request.user
            review.teacher = teacher
            review.save()
            return redirect('teacher_detail', teacher_id=teacher.id)
        reviews = Review.objects.filter(teacher=teacher)
        return render(request, self.template_name, {'teacher': teacher, 'reviews': reviews, 'form': form})

class EditReviewView(View):
    def get(self, request, teacher_id, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.user == request.user:
            # Render a form to edit the review (you can create an edit_review.html template)
            return render(request, 'edit_review.html', {'review': review})
        else:
            # Handle unauthorized access (e.g., show an error message)
            return redirect('teacher_detail', teacher_id=teacher_id)

    def post(self, request, teacher_id, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.user == request.user:
            # Process the form data and update the review
            rating = request.POST.get('rating')
            comment = request.POST.get('comment')
            
            # Update the review attributes
            review.rating = rating
            review.comment = comment
            review.save()
            
            # Redirect back to the teacher detail page
            return redirect('teacher_detail', teacher_id=teacher_id)
        else:
            # Handle unauthorized access (e.g., show an error message)
            return redirect('teacher_detail', teacher_id=teacher_id)

class DeleteReviewView(View):
    def get(self, request, teacher_id, review_id):
        review = get_object_or_404(Review, id=review_id)
        if review.user == request.user:
            # Delete the review
            review.delete()
        # Redirect back to the teacher detail page
        return redirect('teacher_detail', teacher_id=teacher_id)


# Add these views to your views.py
class DiscussionListView(ListView):
    model = Discussion
    template_name = 'discussion_list.html'
    context_object_name = 'discussions'
    ordering = ['-created_at']

from django.utils.decorators import method_decorator
class DiscussionDetailView(View):
    template_name = 'discussion_detail.html'

    def get(self, request, discussion_id):
        discussion = get_object_or_404(Discussion, pk=discussion_id)
        reply_form = DiscussionReplyForm()
        return render(request, self.template_name, {'discussion': discussion, 'reply_form': reply_form})

    @method_decorator(login_required)
    def post(self, request, discussion_id):
        discussion = get_object_or_404(Discussion, pk=discussion_id)
        reply_form = DiscussionReplyForm(request.POST)
        if reply_form.is_valid():
            reply = reply_form.save(commit=False)
            reply.user = request.user
            reply.discussion = discussion
            reply.save()
            return redirect('discussion_detail', discussion_id=discussion.id)
        return render(request, self.template_name, {'discussion': discussion, 'reply_form': reply_form})

@login_required
def add_discussion(request):
    if request.method == 'POST':
        form = DiscussionForm(request.POST)
        if form.is_valid():
            discussion = form.save(commit=False)
            discussion.user = request.user  # Assign the logged-in user to the discussion
            discussion.save()
            return redirect('discussion_list')
    else:
        form = DiscussionForm()
    return render(request, 'add_discussion.html', {'form': form})

@login_required
def edit_discussion(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id, user=request.user)

    if request.method == 'POST':
        form = DiscussionForm(request.POST, instance=discussion)
        if form.is_valid():
            form.save()
            return redirect('discussion_detail', discussion_id=discussion.id)
    else:
        form = DiscussionForm(instance=discussion)

    return render(request, 'edit_discussion.html', {'form': form, 'discussion': discussion})

@login_required
def edit_reply(request, discussion_id, reply_id):
    discussion = get_object_or_404(Discussion, id=discussion_id)
    reply = get_object_or_404(DiscussionReply, id=reply_id, user=request.user, discussion=discussion)

    if request.method == 'POST':
        form = DiscussionReplyForm(request.POST, instance=reply)
        if form.is_valid():
            form.save()
            return redirect('discussion_detail', discussion_id=discussion.id)
    else:
        form = DiscussionReplyForm(instance=reply)

    return render(request, 'edit_reply.html', {'form': form, 'discussion': discussion, 'reply': reply})

@login_required
def delete_discussion(request, discussion_id):
    discussion = get_object_or_404(Discussion, id=discussion_id, user=request.user)
    
    if request.method == 'POST':
        discussion.delete()
        return redirect('discussion_list')
    
    return render(request, 'delete_discussion.html', {'discussion': discussion})

@login_required
def delete_reply(request, discussion_id, reply_id):
    # Get the discussion and reply to be deleted
    discussion = get_object_or_404(Discussion, id=discussion_id)
    reply = get_object_or_404(DiscussionReply, id=reply_id, discussion=discussion, user=request.user)

    if request.method == 'POST':
        # If the request is a POST (typically after confirmation), delete the reply
        reply.delete()
        return redirect('discussion_detail', discussion_id=discussion.id)

    # If the request is a GET (before confirmation), render the confirmation template
    return render(request, 'delete_reply.html', {'discussion': discussion, 'reply': reply})
