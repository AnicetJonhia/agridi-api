from django.db import models



class Crop(models.Model):
    name = models.CharField(max_length=100)
    season = models.ForeignKey('Season', related_name='crops', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    season = models.ForeignKey('Season', related_name='events', on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class Season(models.Model):
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(blank=True, null=True)

    def duration(self):
        return (self.end_date - self.start_date).days

    def __str__(self):
        return self.name

