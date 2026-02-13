from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.db.models import Sum
from .serializers import StoreTotalSalesSerializer, UserSerializer
from django.contrib.auth.models import User 
from rest_framework.authtoken.models import Token
from .models import Sale

from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

@api_view(['POST'])
def register(request):
    print(request.data)
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()

        user = User.objects.get(username=serializer.data['username'])
        user.set_password(serializer.data['password'])  # Hash the password
        user.save()

        token = Token.objects.create(user=user)
        return Response({'token': token.key, 'user': serializer.data}, status=201)
    
    return Response(serializer.errors, status=400)


@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')

    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response({'error': 'Invalid credentials'}, status=401)

    if not user.check_password(password):
        return Response({'error': 'Invalid password'}, status=401)

    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'user': UserSerializer(user).data})

@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def Profile(request):
    print (request.user)

    serializer =UserSerializer(instance=request.user)

    return Response({**serializer.data, "message": f"Welcome back {serializer.data['username']}"}, status=200)

@api_view(['GET'])
def home(request):
    return Response({"message": "Hello API"})
# Create your views here.


@api_view(['GET'])
def getSales(request):
    # Group by store, sum total_price for each
    #call calculate_total() method for each sale to ensure total_price is up to date
    for sale in Sale.objects.all():
        sale.calculate_total()
        sale.save()
        
    sales_by_store = (
        Sale.objects
        .values('store__id', 'store__name')
        .annotate(total_sales=Sum('total_price'))
        .order_by('store__name')
    )
    
    serializer = StoreTotalSalesSerializer(sales_by_store, many=True)
    return Response(serializer.data)

