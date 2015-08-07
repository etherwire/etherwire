from django.conf.urls import include, url
from django.contrib import admin
from blockchain.models import Block
from rest_framework import routers, serializers, viewsets
from blockchain.api import LimitedPagination

# Serializers define the API representation.
class BlockSerializer(serializers.HyperlinkedModelSerializer):
    
    class Meta:
        model = Block
        fields = ('number', 'blockhash', 'prevhash', 'gas_limit')
    """
    number = models.IntegerField(primary_key=True)
    blockhash = ByteField(bytes=32)
    prevhash = ByteField(bytes=32)
    nonce = ByteField(bytes=8)
    uncles_hash = ByteField(bytes=32)
    logs_bloom = ByteField(bytes=256)
    transactions_root = ByteField(bytes=32)
    state_root = ByteField(bytes=32)
    miner = ByteField(bytes=20)
    difficulty = models.BigIntegerField()
    total_difficulty = models.BigIntegerField()
    extra_data = ByteField(bytes=32)
    gas_limit = models.BigIntegerField()
    gas_used = models.BigIntegerField()
    timestamp = models.DateTimeField()
    size = models.IntegerField()
    uncles = models.ManyToManyField('Block')
    """

# ViewSets define the view behavior.
class BlockViewSet(viewsets.ModelViewSet):
    queryset = Block.objects.filter(number__lte=50)
    serializer_class = BlockSerializer
    pagination_class = LimitedPagination

# Routers provide an easy way of automatically determining the URL conf.
router = routers.DefaultRouter()
router.register(r'blocks', BlockViewSet)

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^', include(router.urls))
]
