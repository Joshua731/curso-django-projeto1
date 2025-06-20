from django.urls import path, include
# from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenVerifyView, TokenRefreshView
)

from . import views

app_name = 'recipes'
# recipes:recipe-list
# recipes:recipe-detail pk
recipe_api_v2_router = views.OptionalSlashSimpleRouter()
recipe_api_v2_router.register(
    'recipes/api/v2',
    views.RecipeApiv2ViewSet,
    basename='recipes-api'
)

print(recipe_api_v2_router.urls)

urlpatterns = [
    path(
        '',
        views.RecipeListViewHome.as_view(),
        name="home"
    ),
    path(
        'recipes/search/',
        views.RecipeListViewSearch.as_view(),
        name="search"
    ),
    path(
        'recipes/tags/<slug:slug>',
        views.RecipeListViewTag.as_view(),
        name="tag"
    ),
    path(
        'recipes/category/<int:category_id>/',
        views.RecipeListViewCategory.as_view(),
        name="category"
    ),
    path(
        'recipes/<int:pk>/',
        views.RecipeDetail.as_view(),
        name="recipe"
    ),
    path(
        'recipes/api/v1/',
        views.RecipeListViewHomeApi.as_view(),
        name="recipes_api_v1",
    ),
    path(
        'recipes/api/v1/<int:pk>/',
        views.RecipeDetailAPI.as_view(),
        name="recipes_api_v1_detail",
    ),
    path(
        'recipes/theory/',
        views.theory,
        name='theory'
    ),
    # path(
    #     'recipes/api/v2/',
    #     views.RecipeApiv2ViewSet.as_view({
    #         'get': 'list',
    #         'post': 'create'
    #     }),
    #     name='recipes_api_v2'
    # ),
    # path(
    #     'recipes/api/v2/<int:pk>',
    #     views.RecipeApiv2ViewSet.as_view({
    #         'get': 'retrieve',
    #         'patch': 'partial_update',
    #         'delete': 'destroy',
    #     }),
    #     name='recipes_api_v2_detail',
    # ),
        path(
        'recipes/api/v2/tag/<int:pk>',
        views.tag_api_detail,
        name='recipes_api_v2_tag',
    ),
        
    path('recipes/api/token', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('recipes/api/token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('recipes/api/token/verify', TokenVerifyView.as_view(), name='token_verify'),
    
    # por último
    path('', include(recipe_api_v2_router.urls))

]

# urlpatterns += recipe_api_v2_router.urls