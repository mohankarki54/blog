from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.contrib import auth
from datetime import datetime
import feedparser
from django.template.defaultfilters import truncatewords_html
from time import mktime


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(blank=True, null=True,
                width_field = 'width_field', height_field = 'height_field', editable = 'True', upload_to='blog_project/mediacdn/')
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default = 0)


    def publish(self):
        self.published_date = timezone.make_aware(datetime.now(),timezone.get_default_timezone())
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})


    def __str__(self):
        return self.title






class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments', on_delete = models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.make_aware(datetime.now(),timezone.get_default_timezone()))
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text

class User(auth.models.User, auth.models.PermissionsMixin):


    def __str__(self):
        return "@{}".format(self.username)

class Feed(models.Model):
    title = models.CharField(max_length=200)
    url = models.URLField(unique=True)
    is_active = models.BooleanField(default=True)


    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Check to see if this is a new feed or not
        new_feed = self.pk is None

        feed_data = feedparser.parse(self.url)

        # Set feed title field if available
        if new_feed:
            if feed_data.feed.title:
                self.title = feed_data.feed.title
        else:
                self.title = "Undefined"

        super(Feed, self).save(*args, **kwargs)

        if new_feed:
            self.get_feed_articles()

    def get_feed_articles(self):
        feed_data = feedparser.parse(self.url)

        for entry in feed_data.entries:
            try:
                article = Article.objects.get(url=entry.link)
            except:
                article = Article()

            article.title = entry.title
            article.url = entry.link
            article.description = entry.description
            article.description_truncated = truncatewords_html(entry.description, 150)

            # Set publication date

            d = datetime(*(entry.published_parsed[0:6]))
            dateString = d.strftime('%Y-%m-%d %H:%M:%S')

            article.publication_date = dateString


            article.feed = self
            article.save()




class Article(models.Model):
    feed = models.ForeignKey(Feed, on_delete = models.CASCADE)
    title = models.CharField(max_length=200)
    url = models.URLField()
    description = models.TextField()
    publication_date = models.DateTimeField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("articles_list")

    class Meta:
        ordering = ['-publication_date']
