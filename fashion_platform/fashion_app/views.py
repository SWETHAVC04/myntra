''' from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Item, Outfit, UserPreference
from .serializers import ItemSerializer, OutfitSerializer, UserPreferenceSerializer
from ml.outfit_pairing import OutfitPairer
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Item, Outfit, UserPreference
from .serializers import ItemSerializer, OutfitSerializer, UserPreferenceSerializer
from django.views.decorators.http import require_http_methods

class ItemViewSet(viewsets.ModelViewSet):
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    @action(detail=False, methods=['get'])
    def search(self, request):
        aesthetic = request.query_params.get('aesthetic', None)
        if aesthetic:
            items = Item.objects.filter(aesthetic=aesthetic)
            serializer = self.get_serializer(items, many=True)
            return Response(serializer.data)
        return Response({'error': 'Aesthetic parameter is required'}, status=400)

class OutfitViewSet(viewsets.ModelViewSet):
    queryset = Outfit.objects.all()
    serializer_class = OutfitSerializer

    @action(detail=False, methods=['post'])
    def recommend(self, request):
        item_id = request.data.get('item_id')
        if item_id:
            item = Item.objects.get(id=item_id)
            all_items = Item.objects.all()
            recommended_ids = find_matching_items(item, all_items)
            recommended_items = Item.objects.filter(id__in=recommended_ids)
            serializer = ItemSerializer(recommended_items, many=True)
            return Response(serializer.data)
        return Response({'error': 'Item ID is required'}, status=400)

class UserPreferenceViewSet(viewsets.ModelViewSet):
    queryset = UserPreference.objects.all()
    serializer_class = UserPreferenceSerializer

from ml.categorization import AestheticCategorizer

def categorize_items():
    categorizer = AestheticCategorizer()
    items = Item.objects.all()
    descriptions = [item.description for item in items]
    labels = [item.aesthetic for item in items]
    categorizer.train(descriptions, labels)
    
    # Predict for new items
    new_items = ['description1', 'description2']
    predictions = categorizer.predict(new_items)

def recommend_outfit(item_id):
    items = list(Item.objects.all())
    pairer = OutfitPairer(items)
    seed_item_index = next(index for (index, d) in enumerate(items) if d.id == item_id)
    outfit_indices = pairer.generate_outfit(seed_item_index)
    return [items[i] for i in outfit_indices]

from django.shortcuts import render
from django.http import JsonResponse
from .fashionRecs import FashionRecommendationSystem
from django.contrib.auth.models import User

def home_view(request):
    return render(request, 'fashion_app/home.html')

def search_view(request):
    return render(request, 'fashion_app/search.html')

def recommendations_view(request):
    return render(request, 'fashion_app/recommendations.html')

@require_http_methods(["GET"])
def get_outfit_recommendation(request):
    # In a real app, you'd get the actual user
    user = User.objects.first()  # or get the logged-in user
    
    system = FashionRecommendationSystem()
    outfit, trend = system.get_outfit(user)
    
    if outfit and trend:
        outfit_data = [{
            'category': item.category,
            'name': item.name,
            'color': item.color
        } for item in outfit]
        
        return JsonResponse({
            'outfit': outfit_data,
            'trend': {'name': trend.name}
        })
    else:
        return JsonResponse({'error': 'Unable to generate outfit'}, status=400)


def darkacademia(request, aesthetic_name):
    # Convert URL-friendly name back to title case
    aesthetic_title = aesthetic_name.replace('-', ' ').title()
    
    # Here you would fetch data related to this aesthetic
    # For now, we'll just pass the name
    context = {
        'aesthetic_name': aesthetic_title,
    }
    return render(request, 'fashion_app/darkAcademia.html', context)

def apparel_set_view(request, aesthetic):
    # Fetch items based on the aesthetic
    items = Item.objects.filter(aesthetic=aesthetic)[:12]  # Limit to 12 items for this example
    context = {
        'aesthetic': aesthetic,
        'items': items
    }
    return render(request, 'fashion_app/apparel_set.html', context) '''

from django.shortcuts import render
from .models import Item, UserPreference  # Remove Outfit from here

def home_view(request):
    return render(request, 'fashion_app/home.html')

def search_view(request):
    return render(request, 'fashion_app/search.html')

def recommendations_view(request):
    return render(request, 'fashion_app/recommendations.html')

def apparel_set_view(request, aesthetic):
    items = Item.objects.filter(aesthetic=aesthetic)[:12]
    context = {
        'aesthetic': aesthetic,
        'items': items
    }
    return render(request, 'fashion_app/apparel_set.html', context)

def darkacademia(request, item_name):
    return render(request, 'fashion_app/dark-academia.html', {'item_name': item_name})

from django.shortcuts import render
from .models import Item, UserPreference

def home_view(request):
    # Get all unique aesthetics
    aesthetics = Item.objects.values_list('aesthetic', flat=True).distinct()
    return render(request, 'fashion_app/home.html', {'aesthetics': aesthetics})

def apparel_set_view(request, aesthetic):
    items = Item.objects.filter(aesthetic=aesthetic)[:12]
    context = {
        'aesthetic': aesthetic,
        'items': items
    }
    return render(request, 'fashion_app/apparel_set.html', context)

# Keep your other views as they are