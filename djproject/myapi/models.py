from django.db import models

# Create your models here.


class hydjobs(models.Model):
    date = models.DateField()
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    eligibility = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.IntegerField()

    def __str__(self):
        return self.company


class blorejobs(models.Model):
    date = models.DateField()
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    eligibility = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.IntegerField()

    def __str__(self):
        return self.company


class chennaijobs(models.Model):
    date = models.DateField()
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    eligibility = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.IntegerField()

    def __str__(self):
        return self.company


class punejobs(models.Model):
    date = models.DateField()
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    eligibility = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.IntegerField()

    def __str__(self):
        return self.company


class noidajobs(models.Model):
    date = models.DateField()
    company = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    eligibility = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    email = models.EmailField()
    phonenumber = models.IntegerField()

    def __str__(self):
        return self.company