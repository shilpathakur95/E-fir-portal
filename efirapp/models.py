from django.db import models
TYPE_CHOICES = (
        ('1', 'Received'),
        ('2', 'Registered'),
        ('3','Investigating'),
        ('4','Charge sheet filed')
    )
class Aadhar(models.Model):
    aadhaar_id = models.BigIntegerField(primary_key=True)
    otp = models.BigIntegerField()
    txn_id = models.BigIntegerField()
    name=models.CharField(max_length=200)
    dob=models.CharField(max_length=50)
    gender = models.CharField(max_length=2)
    phone = models.CharField(max_length=10)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=500)
    def __unicode__(self):

        return '%s %s %s %s %s %s %s %s %s' % (str(self.aadhaar_id), str(self.otp),
                                               str(self.txn_id), self.name, self.dob , self.gender, self.phone, self.email, self.address )


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Complaint(models.Model):
    fir_id =models.AutoField(primary_key=True)
    aadhar_no = models.ForeignKey(Aadhar, on_delete=models.CASCADE)
    state  = models.ForeignKey(State,on_delete=models.SET_NULL, null=True)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True)
    complain = models.TextField(max_length=10000, blank=True)
    recording = models.FileField(blank=True)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super(Complaint, self).save(*args, **kwargs)
        if is_new:
            cd = Status(fir_id=self)
            #cd.fir_id = self.pk
            cd.save()

    def __str__(self):
        return str(self.aadhar_no.aadhaar_id)

class Status(models.Model):

    fir_id = models.ForeignKey(Complaint, on_delete=models.CASCADE)
    status = models.CharField(max_length=10,choices=TYPE_CHOICES,default='1')
    comments = models.TextField(max_length=500,blank=True)

