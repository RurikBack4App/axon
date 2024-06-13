from django.urls import path
from .views import (
    LoanViewSet,
    PaymentViewSet,
    AssetViewSet,
    PriceComparisonViewSet,
    LoanCreditMemoViewSet,
    LoanScheduleViewSet,
    DealerViewSet,
    ProspectiveClientViewSet,
)

urlpatterns = [
    # Loans
    path('loans/', LoanViewSet.as_view({'get': 'list', 'post': 'create'}), name='loan-list'),
    path('loans/<int:pk>/', LoanViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='loan-detail'),
    path('loans/<int:pk>/approve/', LoanViewSet.as_view({'post': 'approve'}), name='loan-approve'),
    path('loans/<int:pk>/reject/', LoanViewSet.as_view({'post': 'reject'}), name='loan-reject'),
    path('loans/<int:pk>/disburse/', LoanViewSet.as_view({'post': 'disburse'}), name='loan-disburse'),
    path('loans/<int:pk>/upload_credit_memo/', LoanViewSet.as_view({'post': 'upload_credit_memo'}), name='loan-creditmemo-upload'),
    path('loans/<int:pk>/assign_reviewer/', LoanViewSet.as_view({'post': 'assign_reviewer'}), name='loan-assign-reviewer'),

    # Assets
    path('assets/', AssetViewSet.as_view({'get': 'list', 'post': 'create'}), name='asset-list'),
    path('assets/<int:pk>/', AssetViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='asset-detail'),
    path('assets/<int:pk>/upload_file/', AssetViewSet.as_view({'post': 'upload_file'}), name='asset-upload-file'),

    # Dealers
    path('dealers/', DealerViewSet.as_view({'get': 'list', 'post': 'create'}), name='dealer-list'),
    path('dealers/<int:pk>/', DealerViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='dealer-detail'),

    # Prospective Clients
    path('prospectiveclients/', ProspectiveClientViewSet.as_view({'get': 'list', 'post': 'create'}), name='prospectiveclient-list'),
    path('prospectiveclients/<int:pk>/', ProspectiveClientViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='prospectiveclient-detail'),
    path('prospectiveclients/<int:pk>/approve/', ProspectiveClientViewSet.as_view({'post': 'approve'}), name='prospectiveclient-approve'),
    path('prospectiveclients/<int:pk>/reject/', ProspectiveClientViewSet.as_view({'post': 'reject'}), name='prospectiveclient-reject'),
    path('prospectiveclients/<int:pk>/query/', ProspectiveClientViewSet.as_view({'post': 'query'}), name='prospectiveclient-query'),

    # Price Comparisons
    path('pricecomparisons/', PriceComparisonViewSet.as_view({'get': 'list', 'post': 'create'}), name='pricecomparison-list'),
    path('pricecomparisons/<int:pk>/', PriceComparisonViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='pricecomparison-detail'),

    # Credit Memos
    path('creditmemos/', LoanCreditMemoViewSet.as_view({'get': 'list', 'post': 'create'}), name='creditmemo-list'),
    path('creditmemos/<int:pk>/', LoanCreditMemoViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='creditmemo-detail'),

    # Payments
    path('loans/<int:loan_id>/payments/', PaymentViewSet.as_view({'get': 'list', 'post': 'create'}), name='payment-list'),
    path('loans/<int:loan_id>/payments/<int:pk>/', PaymentViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='payment-detail'),

    # Loan Schedules
    path('loanschedules/', LoanScheduleViewSet.as_view({'get': 'list', 'post': 'create'}), name='loanschedule-list'),
    path('loanschedules/<int:pk>/', LoanScheduleViewSet.as_view({'get': 'retrieve', 'put': 'update', 'delete': 'destroy'}), name='loanschedule-detail'),
]
