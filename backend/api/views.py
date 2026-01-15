from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend, FilterSet, NumberFilter, CharFilter, BooleanFilter
from django.db.models import Q, Count, Avg, Min, Max
from .models import Parcel, ParcelImage, ParcelDocument, NearbyAmenity, Inquiry, ParcelComparison
from .serializers import (
    ParcelSerializer, ParcelListSerializer, ParcelDetailSerializer,
    ParcelImageSerializer, ParcelDocumentSerializer, NearbyAmenitySerializer,
    InquirySerializer, ParcelComparisonSerializer
)
from django.core.mail import send_mail
from django.conf import settings
import math


class ParcelFilter(FilterSet):
    """Custom filter for advanced parcel search"""
    min_price = NumberFilter(field_name='sale_price', lookup_expr='gte')
    max_price = NumberFilter(field_name='sale_price', lookup_expr='lte')
    min_area = NumberFilter(field_name='area_sqm', lookup_expr='gte')
    max_area = NumberFilter(field_name='area_sqm', lookup_expr='lte')
    sub_city = CharFilter(field_name='sub_city', lookup_expr='icontains')
    wereda = CharFilter(field_name='wereda', lookup_expr='icontains')
    street = CharFilter(field_name='street_name', lookup_expr='icontains')
    property_type = CharFilter(field_name='property_type')
    listing_type = CharFilter(field_name='listing_type')
    has_electricity = BooleanFilter(field_name='has_electricity')
    has_water = BooleanFilter(field_name='has_water')
    has_sewage = BooleanFilter(field_name='has_sewage')
    status = CharFilter(field_name='status')
    
    class Meta:
        model = Parcel
        fields = ['property_type', 'listing_type', 'sub_city', 'wereda', 'status']


class ParcelViewSet(viewsets.ModelViewSet):
    queryset = Parcel.objects.all().prefetch_related('images', 'amenities')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_class = ParcelFilter
    search_fields = ['parcel_id', 'title', 'description', 'sub_city', 'wereda', 'street_name', 'landmark']
    ordering_fields = ['sale_price', 'area_sqm', 'created_at', 'views_count', 'price_per_sqm']
    ordering = ['-created_at']
    
    def get_serializer_class(self):
        if self.action == 'list':
            return ParcelListSerializer
        elif self.action == 'retrieve':
            return ParcelDetailSerializer
        return ParcelSerializer
    
    def retrieve(self, request, *args, **kwargs):
        """Increment view count when parcel is viewed"""
        instance = self.get_object()
        instance.views_count += 1
        instance.save(update_fields=['views_count'])
        serializer = self.get_serializer(instance)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Get featured parcels"""
        featured = self.queryset.filter(is_featured=True, status='AVAILABLE')
        serializer = ParcelListSerializer(featured, many=True, context={'request': request})
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def statistics(self, request):
        """Get price statistics and analytics"""
        stats = Parcel.objects.filter(status='AVAILABLE').aggregate(
            avg_price=Avg('sale_price'),
            min_price=Min('sale_price'),
            max_price=Max('sale_price'),
            avg_area=Avg('area_sqm'),
            avg_price_per_sqm=Avg('price_per_sqm'),
            total_parcels=Count('id')
        )
        
        # Group by property type
        by_type = {}
        for ptype in ['RESIDENTIAL', 'COMMERCIAL', 'INDUSTRIAL', 'AGRICULTURAL']:
            type_stats = Parcel.objects.filter(
                status='AVAILABLE', 
                property_type=ptype
            ).aggregate(
                avg_price=Avg('sale_price'),
                count=Count('id'),
                avg_area=Avg('area_sqm')
            )
            by_type[ptype] = type_stats
        
        # Group by sub-city
        by_location = Parcel.objects.filter(
            status='AVAILABLE'
        ).values('sub_city').annotate(
            avg_price=Avg('sale_price'),
            count=Count('id')
        ).order_by('-count')[:10]
        
        return Response({
            'overall': stats,
            'by_property_type': by_type,
            'by_location': list(by_location)
        })
    
    @action(detail=True, methods=['get'])
    def calculate_distance(self, request, pk=None):
        """Calculate distance from parcel to a given location"""
        parcel = self.get_object()
        target_lat = float(request.query_params.get('lat', 0))
        target_lng = float(request.query_params.get('lng', 0))
        
        if not parcel.centroid_lat or not parcel.centroid_lng:
            return Response({'error': 'Parcel coordinates not available'}, status=400)
        
        # Haversine formula for distance calculation
        def haversine(lat1, lon1, lat2, lon2):
            R = 6371  # Earth's radius in kilometers
            
            lat1, lon1, lat2, lon2 = map(math.radians, [float(lat1), float(lon1), lat2, lon2])
            dlat = lat2 - lat1
            dlon = lon2 - lon1
            
            a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
            c = 2 * math.asin(math.sqrt(a))
            
            return R * c
        
        distance = haversine(parcel.centroid_lat, parcel.centroid_lng, target_lat, target_lng)
        
        return Response({
            'distance_km': round(distance, 2),
            'parcel_id': parcel.parcel_id,
            'from': {
                'lat': float(parcel.centroid_lat),
                'lng': float(parcel.centroid_lng)
            },
            'to': {
                'lat': target_lat,
                'lng': target_lng
            }
        })
    
    @action(detail=False, methods=['post'])
    def compare(self, request):
        """Compare multiple parcels"""
        parcel_ids = request.data.get('parcel_ids', [])
        
        if len(parcel_ids) < 2 or len(parcel_ids) > 3:
            return Response(
                {'error': 'Please select 2-3 parcels to compare'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        parcels = Parcel.objects.filter(id__in=parcel_ids)
        serializer = ParcelDetailSerializer(parcels, many=True, context={'request': request})
        
        return Response({
            'parcels': serializer.data,
            'comparison_count': len(parcel_ids)
        })


class InquiryViewSet(viewsets.ModelViewSet):
    queryset = Inquiry.objects.all()
    serializer_class = InquirySerializer
    
    def create(self, request, *args, **kwargs):
        """Create inquiry and send email notification"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        inquiry = serializer.save()
        
        # Get parcel and owner info
        parcel = inquiry.parcel
        
        # Send email to owner (if configured)
        try:
            if parcel.owner_email:
                send_mail(
                    subject=f'New Inquiry for {parcel.parcel_id}',
                    message=f'''
                    You have received a new inquiry for your property {parcel.parcel_id}.
                    
                    From: {inquiry.name}
                    Email: {inquiry.email}
                    Phone: {inquiry.phone}
                    Type: {inquiry.get_inquiry_type_display()}
                    
                    Message:
                    {inquiry.message}
                    ''',
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[parcel.owner_email],
                    fail_silently=True,
                )
        except Exception as e:
            print(f"Email sending failed: {e}")
        
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ParcelImageViewSet(viewsets.ModelViewSet):
    queryset = ParcelImage.objects.all()
    serializer_class = ParcelImageSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        parcel_id = self.request.query_params.get('parcel_id')
        if parcel_id:
            queryset = queryset.filter(parcel_id=parcel_id)
        return queryset


class ParcelDocumentViewSet(viewsets.ModelViewSet):
    queryset = ParcelDocument.objects.all()
    serializer_class = ParcelDocumentSerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        parcel_id = self.request.query_params.get('parcel_id')
        if parcel_id:
            queryset = queryset.filter(parcel_id=parcel_id)
        return queryset


class NearbyAmenityViewSet(viewsets.ModelViewSet):
    queryset = NearbyAmenity.objects.all()
    serializer_class = NearbyAmenitySerializer
    
    def get_queryset(self):
        queryset = super().get_queryset()
        parcel_id = self.request.query_params.get('parcel_id')
        if parcel_id:
            queryset = queryset.filter(parcel_id=parcel_id)
        return queryset
