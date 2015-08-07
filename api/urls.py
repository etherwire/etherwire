from django.conf.urls import include, url
from django.contrib import admin
from blockchain.models import Block
from rest_framework import routers, serializers, viewsets

# Serializers define the API representation.
class BlockSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Block

# ViewSets define the view behavior.
class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.all()
    serializer_class = BlockSerializer

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'blocks', BlockViewSet)

urlpatterns = [
    url(r'^', include(router.urls))
]
