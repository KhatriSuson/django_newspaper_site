from django.db import models



# Create your models here.

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
class Category(TimeStampModel):
    name = models.CharField(max_length=200)
    

    def __str__(self):
        return self.name
    
class Tag(TimeStampModel):
    name = models.CharField(max_length=100)
    

    def __str__(self):
        return self.name


class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("in_active", "Inactive"),
    ]

    title = models.CharField(max_length=300)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%y/%m/%d", blank=False)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default=False)
    views_count = models.PositiveBigIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    


    def __str__(self):
        return self.title

class Contact(TimeStampModel):
    message = models.TextField()
    name = models.CharField(max_length=300)
    email = models.EmailField()
    subject = models.CharField(max_length=200)


    def __str__(self):
        return self.name
    


class Comment(TimeStampModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    comment = models.TextField()
    name = models.CharField(max_length=50)
    email = models.EmailField()

    def __str__(self):
        return f"{self.email} | {self.comment[:70]}"