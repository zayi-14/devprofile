from django.db import models
from django.core.exceptions import ValidationError


# ---------------- PROFILE (Single Instance) ----------------
from django.db import models
from django.core.exceptions import ValidationError
from cloudinary_storage.storage import MediaCloudinaryStorage


class Profile(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField()

    profile_image = models.ImageField(
        storage=MediaCloudinaryStorage(),
        upload_to="profile/",
        blank=True,
        null=True
    )

    resume = models.FileField(
        storage=MediaCloudinaryStorage(),
        upload_to="resume/",
        blank=True,
        null=True
    )

    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    github_url = models.URLField(blank=True, null=True)
    instagram_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.pk and Profile.objects.exists():
            raise ValidationError("Only one profile record is allowed.")
        super().save(*args, **kwargs)


# ---------------- SKILLS ----------------
class Skill(models.Model):
    CATEGORY_CHOICES = [
        ("frontend", "Frontend"),
        ("backend", "Backend"),
        ("database", "Database"),
        ("tools", "Tools"),
        ("devops", "DevOps"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    level = models.PositiveIntegerField(default=70)  # percentage
    icon_html = models.TextField(
        help_text="Paste icon HTML here (FontAwesome, Devicon, Boxicons etc.)"
    )

    def __str__(self):
        return self.name


# ---------------- PROJECT ----------------
from django.utils.text import slugify


class Project(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, editable=False)  # Auto + hidden
    role = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to="projects/", blank=True, null=True)
    skills_used = models.ManyToManyField("Skill", blank=True)
    github_link = models.URLField(blank=True, null=True)
    live_link = models.URLField(blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    bullet_points = models.TextField(blank=True, help_text="Add bullet points separated by line breaks")

    # 🔥 This was missing (fixes ordering)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.title)
            unique_slug = base_slug
            counter = 1

            while Project.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{counter}"
                counter += 1

            self.slug = unique_slug

        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


# ---------------- CONTACT MESSAGE ----------------
class Message(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Message from {self.name}"
