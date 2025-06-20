import os

from django.db.models import F, Q, Value
from django.db.models.functions import Concat
from django.forms.models import model_to_dict
from django.http import JsonResponse
from django.http.response import Http404
from django.views.generic import DetailView, ListView
from utils.pagination import make_pagination
from django.shortcuts import render
from django.core.exceptions import ObjectDoesNotExist
from django.db.models.aggregates import Count
from tag.models import Tag
from recipes.models import Recipe
from django.utils import translation
from django.utils.translation import gettext as _

PER_PAGE = int(os.environ.get('PER_PAGE', 6))


class RecipeListViewBase(ListView):
    model = Recipe
    context_object_name = 'recipes'
    ordering = ['-id']
    template_name = 'recipes/pages/home.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            is_published=True,
        )
        qs = qs.select_related('author', 'category')
        qs = qs.prefetch_related('tags', 'author__profile')
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_obj, pagination_range = make_pagination(
            self.request,
            ctx.get('recipes'),
            PER_PAGE
        )
        
        html_language = translation.get_language()
        
        ctx.update(
            {
                'recipes': page_obj, 
                'pagination_range': pagination_range,  
                'html_language': html_language                       
            }
        )
        
        # print(ctx.get('recipes'))
        
        return ctx


class RecipeListViewHome(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'


class RecipeListViewHomeApi(RecipeListViewBase):
    template_name = 'recipes/pages/home.html'

    def render_to_response(self, context, **response_kwargs):
        recipes = self.get_context_data()['recipes']
        recipes_list = recipes.object_list.values()

        return JsonResponse(
            list(recipes_list),
            safe=False
        )


class RecipeListViewCategory(RecipeListViewBase):
    template_name = 'recipes/pages/category.html'

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        
        category_translation = _('Category')

        ctx.update({
            'title': f'{ctx.get("recipes")[0].category.name} - {category_translation} | '
        })

        return ctx

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            category__id=self.kwargs.get('category_id')
        )

        if not qs:
            raise Http404()

        return qs

class RecipeListViewTag(RecipeListViewBase):
    template_name = 'recipes/pages/tag.html'

    def get_queryset(self, *args, **kwargs):

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(tags__slug=self.kwargs.get('slug', ''))
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        page_title = Tag.objects.filter(slug=self.kwargs.get('slug', '')).first()
        
        if not page_title:
            page_title = 'No recipes found'
        
        page_title = F'{page_title} - Tag |'
        
        ctx.update({
            'page_title': page_title
        })

        return ctx

class RecipeListViewSearch(RecipeListViewBase):
    template_name = 'recipes/pages/search.html'

    def get_queryset(self, *args, **kwargs):
        search_term = self.request.GET.get('q', '')

        if not search_term:
            raise Http404()

        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(
            Q(
                Q(title__icontains=search_term) |
                Q(description__icontains=search_term),
            )
        )
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)
        search_term = self.request.GET.get('q', '')

        ctx.update({
            'page_title': f'Search for "{search_term}" |',
            'search_term': search_term,
            'additional_url_query': f'&q={search_term}',
        })

        return ctx


class RecipeDetail(DetailView):
    model = Recipe
    context_object_name = 'recipe'
    template_name = 'recipes/pages/recipe-view.html'

    def get_queryset(self, *args, **kwargs):
        qs = super().get_queryset(*args, **kwargs)
        qs = qs.filter(is_published=True)
        return qs

    def get_context_data(self, *args, **kwargs):
        ctx = super().get_context_data(*args, **kwargs)

        ctx.update({
            'is_detail_page': True
        })

        return ctx


class RecipeDetailAPI(RecipeDetail):
    def render_to_response(self, context, **response_kwargs):
        recipe = self.get_context_data()['recipe']
        recipe_dict = model_to_dict(recipe)

        recipe_dict['created_at'] = str(recipe.created_at)
        recipe_dict['updated_at'] = str(recipe.updated_at)

        if recipe_dict.get('cover'):
            recipe_dict['cover'] = self.request.build_absolute_uri() + \
                recipe_dict['cover'].url[1:]
        else:
            recipe_dict['cover'] = ''

        del recipe_dict['is_published']
        del recipe_dict['preparation_steps_is_html']

        return JsonResponse(
            recipe_dict,
            safe=False,
        )
        
def theory(request, *args, **kwargs):
    # recipes = Recipe.objects.all()
    # recipes = recipes.filter(title__icontains='Teste').first()
    # recipes = recipes.filter(id=1000).order_by('-id').last()
    # # try:
    #     recipes = Recipe.objects.get(id=1000)
    # except ObjectDoesNotExist:
    #     recipes = None
    # list(recipes)    
    
    # recipes = Recipe.objects.filter(
    #     Q(
    #         Q(
    #             title__icontains='da',
    #             id__gt=2, 
    #             is_published=True
    #         ) | 
    #         Q(
    #             id__gt=1000
    #         )
    #     )
    # )[:10]
    
    # recipes = Recipe.objects.values('id', 'title').filter(title__icontains='teste') # .filter(author_id__gt=1)
    
    recipes = Recipe.objects.get_published()
    
    number_of_recipes = recipes.aggregate(number=Count('id'))
    
    print(recipes)
    
    context = {
        'recipes': recipes,
        'number_of_recipes': number_of_recipes["number"]
    }
    
    return render(
        request,
        'recipes/pages/theory.html',
        context=context
    )