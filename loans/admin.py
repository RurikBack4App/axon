from django.contrib import admin
from loans.models import Asset, Dealer, ProspectiveClient, Loan, LoanSchedule, Payment, LoanCreditMemo,  PriceComparison

admin.site.register(Asset)
admin.site.register(Dealer)
admin.site.register(ProspectiveClient)
admin.site.register(Loan)
admin.site.register(LoanSchedule)
admin.site.register(Payment)
admin.site.register(LoanCreditMemo)
admin.site.register(PriceComparison)