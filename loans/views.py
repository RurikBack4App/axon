from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.exceptions import ValidationError
from .models import Asset, Dealer, Loan, LoanSchedule, Payment, LoanCreditMemo, PriceComparison, ProspectiveClient
from .serializers import LoanSerializer, PaymentSerializer, AssetSerializer, AssetFileUploadSerializer, PriceComparisonSerializer, LoanCreditMemoSerializer, LoanScheduleSerializer, DealerSerializer, ProspectiveClientSerializer
from users.permissions import IsSupervisor, IsAgent, IsReviewer
from users.models import User


class LoanViewSet(viewsets.ModelViewSet):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer
    permission_classes = [permissions.IsAuthenticated, IsAgent | IsSupervisor]

    def perform_create(self, serializer):
        prospective_client_id = self.request.data.get('prospective_client')
        if prospective_client_id:
            try:
                prospective_client = ProspectiveClient.objects.get(pk=prospective_client_id)
                if prospective_client.status != 'approved':
                    raise ValidationError("Prospective client must be approved.")
                serializer.validated_data['client'] = prospective_client.user 
                serializer.validated_data['amount'] = prospective_client.loan_amount 
                serializer.validated_data['asset'] = prospective_client.asset 
                serializer.save()
                prospective_client.status = 'loan_created'
                prospective_client.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            except ProspectiveClient.DoesNotExist:
                raise ValidationError("Prospective client not found.")
        else:
            if not self.request.user.role == 'field_agent':
                raise ValidationError("Only agents can create loans")
            serializer.save(client=self.request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, IsAgent | IsSupervisor], parser_classes=[MultiPartParser, FormParser])
    def upload_credit_memo(self, request, pk=None):
        loan = self.get_object()
        serializer = LoanCreditMemoSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(loan=loan)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, IsReviewer])
    def approve(self, request, pk=None):
        loan = self.get_object()
        loan.status = 'approved'
        loan.reviewed_by = request.user
        loan.save()
        return Response({'message': 'Loan approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, IsReviewer])
    def reject(self, request, pk=None):
        loan = self.get_object()
        loan.status = 'rejected'
        loan.reviewed_by = request.user
        loan.save()
        return Response({'message': 'Loan rejected'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, IsAgent | IsSupervisor])
    def disburse(self, request, pk=None):
        loan = self.get_object()
        loan.status = 'disbursed'
        loan.save()
        return Response({'message': 'Loan disbursed'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, IsSupervisor])
    def assign_reviewer(self, request, pk=None):
        loan = self.get_object()
        reviewer_id = request.data.get('reviewer_id')
        if not reviewer_id:
            return Response({'error': 'Missing reviewer ID'}, status=status.HTTP_400_BAD_REQUEST)
        try:
            reviewer = User.objects.get(pk=reviewer_id, role='reviewer')
        except User.DoesNotExist:
            return Response({'error': 'Reviewer not found or invalid role'}, status=status.HTTP_400_BAD_REQUEST)
        
        loan.reviewed_by = reviewer
        loan.save()
        return Response({'message': 'Reviewer assigned successfully'}, status=status.HTTP_200_OK)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAgent | IsSupervisor]

    def perform_create(self, serializer):
        loan_id = self.kwargs.get('loan_id')
        if not loan_id:
            raise ValidationError("Missing 'loan_id' in URL path")
        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            raise ValidationError("Loan does not exist")
        serializer.save(loan=loan)

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated, IsAgent]
    
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, IsAgent], parser_classes=[MultiPartParser, FormParser])
    def upload_file(self, request, pk=None):
        asset = self.get_object()
        serializer = AssetFileUploadSerializer(asset, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DealerViewSet(viewsets.ModelViewSet):
    queryset = Dealer.objects.all()
    serializer_class = DealerSerializer
    permission_classes = [permissions.IsAuthenticated]

class ProspectiveClientViewSet(viewsets.ModelViewSet):
    queryset = ProspectiveClient.objects.all()
    serializer_class = ProspectiveClientSerializer
    permission_classes = [permissions.IsAuthenticated, IsAgent]

    def perform_create(self, serializer):
        if self.request.user.role != 'field_agent':
            raise ValidationError("Only field agents can create prospective clients")
        serializer.save()

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, IsReviewer])
    def approve(self, request, pk=None):
        prospective_client = self.get_object()
        prospective_client.status = 'approved'
        prospective_client.save()
        return Response({'message': 'Prospective client approved'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, IsReviewer])
    def reject(self, request, pk=None):
        prospective_client = self.get_object()
        prospective_client.status = 'rejected'
        prospective_client.save()
        return Response({'message': 'Prospective client rejected'}, status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['POST'], permission_classes=[permissions.IsAuthenticated, IsReviewer])
    def query(self, request, pk=None):
        prospective_client = self.get_object()
        prospective_client.status = 'under_review'
        prospective_client.save()
        # Add logic to send back to field agent or supervisor (using signals or a message queue)
        return Response({'status': 'under_review'})

class PriceComparisonViewSet(viewsets.ModelViewSet):
    queryset = PriceComparison.objects.all()
    serializer_class = PriceComparisonSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        prospective_client_id = self.request.query_params.get('prospective_client')
        dealer_id = self.request.query_params.get('dealer')
        if not prospective_client_id or not dealer_id:
            raise ValidationError("Missing 'prospective_client' or 'dealer' query parameter")
        try:
            prospective_client = ProspectiveClient.objects.get(pk=prospective_client_id)
            dealer = Dealer.objects.get(pk=dealer_id)
        except (ProspectiveClient.DoesNotExist, Dealer.DoesNotExist):
            raise ValidationError("Prospective Client or Dealer does not exist")
        serializer.save(prospective_client=prospective_client, dealer=dealer)

class LoanCreditMemoViewSet(viewsets.ModelViewSet):
    queryset = LoanCreditMemo.objects.all()
    serializer_class = LoanCreditMemoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        loan_id = self.request.query_params.get('loan') 
        if not loan_id:
            raise ValidationError("Missing 'loan' query parameter")
        try:
            loan = Loan.objects.get(pk=loan_id) 
        except Loan.DoesNotExist:
            raise ValidationError("Loan does not exist")
        serializer.save(loan=loan) 

class LoanScheduleViewSet(viewsets.ModelViewSet):
    queryset = LoanSchedule.objects.all()
    serializer_class = LoanScheduleSerializer
    permission_classes = [permissions.IsAuthenticated, IsAgent | IsSupervisor]
    
    def perform_create(self, serializer):
        loan_id = self.request.data.get('loan')
        if not loan_id:
            raise ValidationError("Missing 'loan' in request data")
        try:
            loan = Loan.objects.get(pk=loan_id)
        except Loan.DoesNotExist:
            raise ValidationError("Loan does not exist")
        serializer.save(loan=loan)
