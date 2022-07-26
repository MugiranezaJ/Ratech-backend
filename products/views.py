from unittest import result
from authentication import serializers
from authentication.models import UserProfile
from authentication.services.otp_service import OtpService
from products.models import Order, Product
from products.serializers import OrderSerializer, ProductSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework import status
from rest_framework.views import APIView
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from django.conf import settings

# Create your views here.


class ProductAddView(APIView):
    authentication_classes = [TokenAuthentication]
    def post(self, request):
        try:
            serialized = ProductSerializer(data=request.data, context={"request": "post"})
            if serialized.is_valid():
                serialized.save()
                response_data = {
                    "response_code": 1,
                    "data": serialized.data,
                    "message": "Product added successfully"
                }

                return Response(data=response_data, status=status.HTTP_201_CREATED)
            else:
                response_data = {
                    "response_code": 1,
                    "error": serialized.errors,
                    "message": "there was an error while adding product"
                }
                return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            print(e)
            response_data = {
                    "response_code": 0,
                    "error": str(e),
                    "message": "an error occured while adding a product"
                }

            return Response(data=response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class ProductSearchView(APIView):

    def get(self, request):
        try:
            query = request.query_params.get("query")
            search_vector = SearchVector('specifications', weight='C') + SearchVector('name', weight='A')
            search_query = SearchQuery(query)
            products = Product.objects.annotate(rank=SearchRank(search_vector, search_query)).filter(rank__gte=0.1).order_by('-rank')
            serialized = ProductSerializer(products, many=True)
            response = {
                'response_code': 1,
                "count": len(serialized.data),
                'data': serialized.data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'response_code': 0,
                'error': str(e),
                'message': "there was error retrieving products"
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class OrderView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            products = request.data.get("product")
            user = request.data.get("user")
            p_status = request.data.get("status")
            type = request.data.get("type")
            profile = UserProfile.objects.filter(user=request.user)

            products_data = []
            for pro in products:
                product = Product.objects.filter(uuid=pro).first()
                if not product.status == 'Available':
                    response = {
                        'response_code': 0,
                        "error": "",
                        "message": product.condition + " " + product.name + " is not available"
                    }
                    return Response(data=response, status=status.HTTP_400_BAD_REQUEST)

                json = {"product":pro, "type":type, "user":user, "status":p_status}
                products_data.append(json)

            serialized = OrderSerializer(data=products_data, context={"request": "post"}, many=True)
            if serialized.is_valid():
                serialized.save()
                response = {
                    "response_code": 1,
                    "data":serialized.data,
                    "message": "operation done successfully"
                }

                res = OtpService.send_email(self, settings.ADMIN_EMAIL, 'Rateck Live Stock - Product order', serialized.data, "product_template.html")
                print(res)
                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                response = {
                'response_code': 0,
                "error": serialized.errors,
                "message": "an error accured"
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response = {
                'response_code': 0,
                "error": str(e),
                "message": "an error accured"
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

    def get(self, request):
        
        user = UserProfile.objects.get(user=request.user)
        orders = Order.objects.filter(user=user, type='order').order_by('-created_at')
        serialized = OrderSerializer(orders, many=True)
        result = formatd_products(user,orders)

        response_data = {
            "response_code": 1,
            "data": result,
            "message":"operation done successfully"
        }

        return Response(data=response_data, status=status.HTTP_200_OK)

class CheckView(APIView):
    authentication_classes = [TokenAuthentication]

    def post(self, request):
        try:
            products = request.data.get("product")
            user = request.data.get("user")
            p_status = request.data.get("status")
            type = request.data.get("type")

            profile = UserProfile.objects.filter(user=request.user)

            products_data = []
            for pro in products:
                product = Product.objects.filter(uuid=pro).first()
                if product.status == 'Available':
                    p_status = product.status
                json = {"product":pro, "type":type, "user":user, "status":p_status}
                products_data.append(json)

            serialized = OrderSerializer(data=products_data, context={"request": "post"}, many=True)
            if serialized.is_valid():
                serialized.save()
                response = {
                    "response_code": 1,
                    "data":serialized.data,
                    "message": "operation done successfully"
                }

                res = OtpService.send_email(self, settings.ADMIN_EMAIL, 'Rateck Live Stock - Product Check', serialized.data, "product_template.html")
                print(res)
                return Response(data=response, status=status.HTTP_201_CREATED)
            else:
                response = {
                'response_code': 0,
                "error": serialized.errors,
                "message": "an error accured"
                }
                return Response(data=response, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
            response = {
                'response_code': 0,
                "error": str(e),
                "message": "an error accured"
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request):
        
        try:
            user = UserProfile.objects.get(user=request.user)
            orders = Order.objects.filter(user=user, type='check').order_by('-created_at')

            result = formatd_products(user, orders)
            
            response_data = {
                "response_code": 1,
                "data": result,
                "message":"operation done successfully"
            }

            return Response(data=response_data, status=status.HTTP_200_OK)
        except Exception as e:
            print(e)
            response = {
                'response_code': 0,
                "error": str(e),
                "message": "an error accured"
            }
            return Response(data=response, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
def formatd_products(user, payload):
    result = {}
    for order in payload:
        date_string = order.created_at.strftime("%m-%d-%Y %H:%M")
        created_at = order.created_at.strftime("%b %d,%Y  %H:%M")
        serialized_order = OrderSerializer(order)
        product = {**serialized_order.data['products'], "order_status":serialized_order.data['status']}
        if date_string in result:
            result[date_string]['products'].append(product)
        else:
            prod = {'created_at': created_at, 'user':user.uuid, 'products': [product]}
            result[date_string] = prod
    
    return result