from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse


from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import Product
from api.serializers import ProductSerializer
from django.db.models import Q


class ProductListView(APIView):

    def get(self, request):
        # Handle search via query string
        search_query = request.query_params.get('search', '')
        # Filter products that contain the search string in the name or description
        products = Product.objects.filter(
            Q(name__icontains=search_query) | Q(
                description__icontains=search_query)
        )

        # Sort the products
        sort_field = request.query_params.get(
            'sort', 'name')  # Default sorting by name
        sort_order = request.query_params.get(
            'order', 'asc')  # Default order ascending

        if sort_field not in ['id', 'name', 'price', 'stock']:
            sort_field = 'name'  # Default fallback

        if sort_order == 'desc':
            sort_field = f'-{sort_field}'

        products = products.order_by(sort_field)

        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):

        # Handle product selection
        product_id = request.data.get('id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Update the product as selected
        product.selected = not product.selected
        product.save()

        return Response({'id': product.id, 'selected': product.selected}, status=status.HTTP_200_OK)

    def patch(self, request):
        # Update the product details
        product_id = request.data.get('id')
        if not product_id:
            return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=status.HTTP_404_NOT_FOUND)

        # Modify the value of the selected field
        if 'selected' in request.data:
            product.selected = request.data['selected']

        # Update other fields if provided
        allowed_fields = ['name', 'description', 'price', 'stock']
        for field, value in request.data.items():
            if field in allowed_fields:
                setattr(product, field, value)

        product.save()

        # Serialize the updated product
        serializer = ProductSerializer(product)
        return Response(serializer.data, status=status.HTTP_200_OK)
