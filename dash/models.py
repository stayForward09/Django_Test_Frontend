from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Type(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Article(models.Model):
    sn = models.CharField(max_length=255, verbose_name="S/N")
    location = models.CharField(max_length=255)
    used = models.CharField(max_length=255)
    model = models.ForeignKey(Type, on_delete=models.CASCADE)

    def __str__(self):
        return self.sn