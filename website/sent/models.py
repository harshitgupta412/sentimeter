from django.db import models

# Create your models here.
class Keys(models.Model):
    keyword = models.CharField(max_length=50)

class Data(models.Model):
    keys = models.ForeignKey(Keys, on_delete=models.CASCADE)
    date = models.DateField()
    twitter = models.FloatField()
    reddit = models.FloatField()
    news = models.FloatField()
    overall = models.FloatField()
    v_twitter = models.FloatField()
    v_reddit = models.FloatField()
    v_news = models.FloatField()
    v_overall = models.FloatField()