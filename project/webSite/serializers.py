from rest_framework import serializers
from .models import Order


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    status = serializers.HiddenField(default='Отправлен')



    class Meta:
        model = Order
        fields = "__all__"

class OrderSerializer2(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())
    # user = serializers.PrimaryKeyRelatedField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Order
        fields = "__all__"




