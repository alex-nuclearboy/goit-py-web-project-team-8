from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

# Create your models here.
class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name', default="Sample tag")
    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1, related_name='cm_tag_set')

    def __str__(self):
        return self.name

class Contact(models.Model):
    days_table = {}
    months_table = {
        "January":"January",
        "February":"February",
        "March":"March",
        "April":"April",
        "May":"May",
        "June":"June",
        "July":"July",
        "August":"August",
        "September":"September",
        "October":"October",
        "November":"November",
        "December":"December",
                    }
    years_table = {}
    for i in range(1,32):
        if i > 9:
            days_table[str(i)] = i
        else:
            days_table["0" + str(i)] = "0" + str(i)
    for i in range(1,2025):
        years_table[str(i)] = i

    creator = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    name = models.CharField(max_length=20, verbose_name='Name', default="Unnamed contact")
    phone = models.CharField(max_length=12, verbose_name='Phone', default="-")
    email = models.CharField(max_length=30, verbose_name='Email', default="-")
    address = models.CharField(max_length=50, verbose_name='Address', default="-")
    birth_day = models.CharField(max_length=2, verbose_name='Birth day', default="-", choices=days_table)
    birth_month = models.CharField(max_length=15, verbose_name='Birth month', default="-", choices=months_table)
    birth_year = models.CharField(max_length=4, verbose_name='Birth year', default="-", choices=years_table)
    tags = models.ManyToManyField(Tag)
    creation_date = models.DateTimeField(default=now, verbose_name='Creation date')

    def __str__(self):
        return f"{self.name} -{self.phone}."