from django.db import models
from useraccounts.models import UserAccount
from help_function.main import FileHandling

class Author(models.Model):
    """Author Details"""
    user         = models.OneToOneField(UserAccount, on_delete=models.CASCADE,verbose_name="Author")
    profession   = models.CharField(max_length=30, blank=True, null=True )
    about_me     = models.TextField(verbose_name="About Me", blank=True, null=True)
    updated_on   = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank = True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.user.first_name) + " " + str(self.user.last_name)   

    class Meta:
        verbose_name_plural = "Authors" 
        ordering = ("-updated_on",)

class BlogCategory(models.Model):
    """Blog Categories"""
    name            =  models.CharField(max_length=200, blank=True, null=True)
    img             =  models.URLField(null = True, blank = True)
    number          =  models.PositiveIntegerField(null=True, blank=True)
    parent_category =  models.ForeignKey("self", on_delete=models.SET_NULL, verbose_name="Parant Category", null=True)

    class Meta:
        verbose_name_plural = " Blog Categories" 
        ordering = ("number",)

    def __str__(self) -> str:
        return str(self.name)

class BlogView(models.Model):
    """Views On Blog"""
    user = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    blog = models.ForeignKey("blog", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.pk)

class Reaction(models.Model):
    """Blog Reactions"""
    obj          = FileHandling("structure/emoji.json")
    user         = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    blog         = models.OneToOneField("blog", on_delete=models.CASCADE)
    reactions    = models.JSONField(default=obj.get_data(), verbose_name="Reaction")
    updated_on   = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank = True, null=True)
    date_created = models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return str(self.user.pk)
    
    class Meta:
        verbose_name_plural = "Blog Reactions" 
        ordering = ("-updated_on",)


class Comments(models.Model):
    """Comments"""
    user            = models.ForeignKey(UserAccount, on_delete=models.CASCADE)
    content         = models.TextField()
    blog            = models.ForeignKey("blog", related_name="comments", on_delete=models.CASCADE)
    reply_comment   = models.ForeignKey("self", related_name="reply", on_delete=models.CASCADE)   
    timestamp       = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.pk)

class Blog(models.Model):
    """Blogs"""
    author            = models.ForeignKey(Author, on_delete=models.CASCADE, verbose_name="Author")
    title             = models.CharField(max_length=200, blank=True, null=True, verbose_name="Title")
    content           = models.TextField(blank = True, null = True)
    category          = models.ForeignKey(BlogCategory, on_delete=models.SET_NULL, null=True, verbose_name="Category")
    service_link_list = models.JSONField(default=list, verbose_name="Services")
    images            = models.JSONField(default = list, verbose_name = "Images")
    previous_post     = models.ForeignKey("self", related_name="previous", on_delete=models.SET_NULL, blank=True, null=True)
    next_post         = models.ForeignKey("self", related_name="next", on_delete=models.SET_NULL, blank=True, null=True)
    comment_count     = models.PositiveIntegerField(default=0)
    updated_on        = models.DateTimeField(auto_now=True, verbose_name="Last Updated", blank = True, null=True)
    date_created      = models.DateTimeField(auto_now_add=True, blank=True, null=True)

    def __str__(self) -> str:
        return str(self.author.pk) + "-" + str(self.pk)  

    class Meta:
        verbose_name_plural = "Blogs" 
        ordering = ("-updated_on",)
