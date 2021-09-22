from rest_framework import serializers
from rest_framework.exceptions import NotFound
from .models import Order, CustomUser, Author, Book


"""
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    end_at = models.DateTimeField(null=True)
    plated_end_at = models.DateTimeField()
"""


class CustomUserNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email']
        read_only_fields = ['id', 'email']


class AuthorNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'surname']
        read_only_fields = ['id', 'surname']


class BookNestedSerializer(serializers.ModelSerializer):
    authors = AuthorNestedSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'authors']
        read_only_fields = ['id', 'name', 'authors']


class OrderListSerializer(serializers.ModelSerializer):
    user = CustomUserNestedSerializer()
    book = BookNestedSerializer()

    class Meta:
        model = Order
        fields = ['user', 'book', 'created_at', 'end_at', 'plated_end_at']
        read_only_fields = ['user', 'book', 'created_at', 'end_at', 'plated_end_at']


class OrderDetailsSerializer(serializers.ModelSerializer):
    user = CustomUserNestedSerializer(required=False)
    book = BookNestedSerializer(required=False)
    user_id = serializers.IntegerField(required=False)
    book_id = serializers.IntegerField(required=False)
    end_at = serializers.DateTimeField(required=False, allow_null=True)
    plated_end_at = serializers.DateTimeField(required=False)

    class Meta:
        model = Order
        fields = ['user', 'book', 'created_at', 'end_at', 'plated_end_at', 'user_id', 'book_id']
        read_only_fields = ['user', 'book', 'created_at']

    def create(self, validated_data):

        user = CustomUser.get_by_id(user_id=validated_data.get('user_id'))
        book = Book.get_by_id(book_id=validated_data.get('book_id'))
        end_at = validated_data.get('end_at', None)
        plated_end_at = validated_data.get('plated_end_at', None)

        if user is None or book is None:
            raise NotFound

        order = Order.objects.create(
            user=user,
            book=book,
            end_at=end_at,
            plated_end_at=plated_end_at
        )
        order.save()

        return order

    def update(self, instance, validated_data):
        instance.plated_end_at = validated_data.get('plated_end_at', instance.plated_end_at)
        instance.end_at = validated_data.get('end_at', instance.end_at)
        instance.save()

        return instance





