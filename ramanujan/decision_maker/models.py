from django.db import models

# Create your models here.


class Poll(models.Model):
    code = models.CharField(max_length=5, primary_key=True)
    admin_code = models.CharField(max_length=10)
    question = models.CharField(max_length=200)
    isopen = models.BooleanField(default=True)


class Candidate(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)
    vote = models.IntegerField(default=0)


class Criteria(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.CharField(max_length=50)


class Score(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    criteria = models.ForeignKey(Criteria, on_delete=models.CASCADE)
    score = models.FloatField()
