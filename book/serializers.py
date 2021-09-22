from rest_framework import serializers
from .models import Author, Book


class AuthorNestedSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ['id', 'surname']
        read_only_fields = ['id', 'surname']


class BookListSerializer(serializers.ModelSerializer):
    authors = AuthorNestedSerializer(many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'authors', 'count']
        read_only_fields = ['id', 'name', 'description', 'authors', 'count']


class BookDetailsSerializer(serializers.ModelSerializer):
    authors = AuthorNestedSerializer(required=False, many=True)

    class Meta:
        model = Book
        fields = ['id', 'name', 'description', 'count', 'authors']

    def create(self, validated_data):
        book = Book.objects.create(
            name=validated_data.get('name'),
            description=validated_data.get('description'),
            count=validated_data.get('count')
        )
        book.save()

        book = self.update_book_authors(book, validated_data)

        return book

    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.count = validated_data.get('count', instance.count)
        instance.save()
        instance = self.update_book_authors(instance, validated_data)

        return instance

    @staticmethod
    def update_book_authors(instance, validated_data):
        authors = validated_data.get('authors', None)
        if authors is not None:
            for author in authors:
                author = Author.get_by_id(author_id=author['id'])
                instance.authors.add(author)
        instance.save()

        return instance



