from django.shortcuts import render, get_object_or_404
from .models import Profile, Skill, Project, Message


def home(request):
    profile = Profile.objects.first()
    skills = Skill.objects.all().order_by("category")
    projects = Project.objects.prefetch_related("skills_used").order_by("-created_at")[:6]

    success = False

    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject") or "Portfolio contact"
        message_text = request.POST.get("message")

        if name and email and message_text:
            Message.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message_text,
            )
            success = True

    return render(request, "home.html", {
        "profile": profile,
        "skills": skills,
        "projects": projects,
        "success": success,
    })


def project_list(request):
    selected_skill = request.GET.get("skill")  # read filter value from URL
    
    skills = Skill.objects.all().order_by("name")

    projects = Project.objects.all().order_by("-created_at")

    if selected_skill:
        projects = projects.filter(skills_used__name=selected_skill)

    return render(request, "list.html", {
        "projects": projects,
        "skills": skills,
        "selected_skill": selected_skill
    })



def project_detail(request, slug):
    project = get_object_or_404(Project, slug=slug)

    # Convert bullet points (line breaks → list)
    bullet_list = project.bullet_points.split("\n") if project.bullet_points else []

    return render(request, "detail.html", {
        "project": project,
        "bullet_list": bullet_list,
    })
