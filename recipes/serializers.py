from collections import defaultdict
from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Recipe, Tag
from authors.validators import AuthorRecipeValidator

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug']
    # id = serializers.IntegerField()
    # name = serializers.CharField(max_length=255)
    # slug = serializers.CharField()
    
class RecipeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Recipe
        fields = [
            'id', 'title', 'description', 'author', 'category', 'tags', 'public', 'preparation',
            'tag_objects', 'tag_links', 'preparation_time', \
            'preparation_time_unit', 'servings', 'servings_unit', \
            'preparation_steps', 'cover'
        ]
        
    # id = serializers.IntegerField()
    # title = serializers.CharField(max_length=65)
    # description = serializers.CharField(max_length=165)
    public = serializers.BooleanField(source='is_published', read_only=True)
    preparation = serializers.SerializerMethodField(method_name='any_method_name', read_only=True)
    
    category = serializers.StringRelatedField(
        read_only=True
    )

    tag_objects = TagSerializer(
        many=True, source='tags', read_only=True
    )
    tag_links = serializers.HyperlinkedRelatedField(
        many=True,
        source='tags',
        # queryset=Tag.objects.all(),
        view_name='recipes:recipes_api_v2_tag',
        read_only=True
    )
    
    def any_method_name(self, recipe):
        return f'{recipe.preparation_time} - {recipe.preparation_time_unit}'
    
    def validate(self, attrs):
        if self.instance is not None and attrs.get('servings') is None:
            attrs['servings'] = self.instance.servings
            
        if self.instance is not None and attrs.get('preparation_time') is None:
            attrs['preparation_time'] = self.instance.preparation_time
            
        super_validate = super().validate(attrs)
        AuthorRecipeValidator(data=attrs, ErrorClass=serializers.ValidationError)
        # title = attrs.get('title')
        # description = attrs.get('description')

        # if title == description:
        #     raise serializers.ValidationError({
        #         "title": ["Posso", "ter", "mais de um erro"],
        #         "description": ["Posso", "ter", "mais de um erro"],
        #     })

        return super_validate

    # def validate_title(self, value):
    #     print("Validate title: ", value)
    #     title = value
    #     if len(title) < 5:
    #         raise serializers.ValidationError("Must have at least 5 chars.")
    #     return title