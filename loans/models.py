from django.db import models
from django.utils import timezone
from users.models import User

class Asset(models.Model):
    description = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    pictures = models.ImageField(upload_to='asset_photos', blank=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    
class Dealer(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=20)
    location = models.CharField(max_length=255)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)

class ProspectiveClient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE) 
    loan_amount = models.DecimalField(max_digits=10, decimal_places=2)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('under_review', 'Under Review'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
        ),
        default='pending',
    )
    bvn = models.CharField(max_length=11, null=True, blank=True)
    home_address = models.CharField(max_length=255, null=True, blank=True)
    passport_picture = models.ImageField(upload_to='applicants_passports', null=True, blank=True)
    price_comparisons = models.ManyToManyField(Dealer, through='PriceComparison')

class PriceComparison(models.Model):
    prospective_client = models.ForeignKey(ProspectiveClient, on_delete=models.CASCADE)
    dealer = models.ForeignKey(Dealer, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

class Loan(models.Model):
    client = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='loans')
    status = models.CharField(
        max_length=20,
        choices=(
            ('pending', 'Pending'),
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('disbursed', 'Disbursed'),
            ('in_progress', 'In Progress'),
            ('defaulted', 'Defaulted'),
        ),
        default='pending',
    )
    interest_rate = models.DecimalField(max_digits=5, decimal_places=2)
    balance_remaining = models.DecimalField(max_digits=10, decimal_places=2)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, limit_choices_to={'role': 'reviewer'}, related_name='reviewed_loans')

class LoanSchedule(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    payment_date = models.DateTimeField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    issue = models.TextField(null=True, blank=True)
    expected_resolution_date = models.DateField(null=True, blank=True)
    days_past_resolution = models.IntegerField(default=0, editable=False)
    flag_days_past_resolution = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if self.expected_resolution_date:
            self.days_past_resolution = (timezone.now().date() - self.expected_resolution_date).days
            if self.expected_resolution_date < timezone.now().date():
                self.flag_days_past_resolution = True
        super().save(*args, **kwargs)

class Payment(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)

class LoanCreditMemo(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE)
    file = models.FileField(upload_to='credit_memos')
