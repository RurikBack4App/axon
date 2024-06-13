from rest_framework import serializers
from .models import Asset, Dealer, Loan, LoanSchedule, Payment, LoanCreditMemo, PriceComparison, ProspectiveClient
from users.serializers import UserSerializer


class AssetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['id', 'description', 'price', 'pictures', 'latitude', 'longitude']
        
class AssetFileUploadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Asset
        fields = ['pictures']

class DealerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dealer
        fields = ['id', 'name', 'phone', 'location', 'latitude', 'longitude']

class PriceComparisonSerializer(serializers.ModelSerializer):
    dealer = DealerSerializer()
    class Meta:
        model = PriceComparison
        fields = ['id', 'prospective_client', 'dealer', 'price']

class LoanSerializer(serializers.ModelSerializer):
    client = UserSerializer(many=False, read_only=True)
    asset = AssetSerializer(many=False, read_only=True)
    class Meta:
        model = Loan
        fields = ['id', 'client', 'amount', 'asset', 'status', 'interest_rate', 'balance_remaining', 'reviewed_by']

    def validate_asset(self, value):
        if not Asset.objects.filter(pk=value.id).exists():
            raise serializers.ValidationError("Asset does not exist.")
        return value

class LoanScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanSchedule
        fields = ['id', 'loan', 'payment_date', 'amount', 'amount_paid', 'issue', 'expected_resolution_date', 'days_past_resolution', 'flag_days_past_resolution']

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'loan', 'date', 'amount']

class LoanCreditMemoSerializer(serializers.ModelSerializer):
    class Meta:
        model = LoanCreditMemo
        fields = ['id', 'loan', 'file']
      
class ProspectiveClientSerializer(serializers.ModelSerializer):
    user = UserSerializer(many=False, read_only=True)
    asset = AssetSerializer(many=False, read_only=True)
    price_comparisons = PriceComparisonSerializer(many=True, read_only=True)
    class Meta:
        model = ProspectiveClient
        fields = ['id', 'user', 'loan_amount', 'asset', 'status', 'bvn', 'home_address', 'passport_picture', 'price_comparisons']
        