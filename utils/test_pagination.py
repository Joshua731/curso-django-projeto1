from unittest import TestCase
from unittest.mock import Mock
from recipes.tests.test_recipe_base import RecipeTestBase
from utils.pagination import make_pagination_range, make_pagination

class PaginationTest(RecipeTestBase):
    def test_make_pagination_range_returns_a_pagination_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

        
    def test_first_range_is_static_if_current_page_is_less_than_middle_page(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)
        
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=2,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)
        
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=3,
        )['pagination']
        self.assertEqual([2, 3, 4, 5], pagination)
        
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=4,
        )['pagination']
        self.assertEqual([3, 4, 5, 6], pagination)
        
    def test_make_sure_middle_ranges_are_correct(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=10,
        )['pagination']
        self.assertEqual([9, 10, 11, 12], pagination)
        
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=12,
        )['pagination']
        self.assertEqual([11, 12, 13, 14], pagination)
        
    def test_make_pagination_range_is_static_when_last_page_is_next(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=18,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
        
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=19,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
        
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=20,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
        
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=21,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
    
    def test_make_pagination_handles_invalid_page_input(self):
        request_mock = Mock()
        request_mock.GET = {'page': 'invalid'}

        _, pagination_range = make_pagination(
            request=request_mock,
            queryset=list(range(1, 101)),
            per_page=10,
            qty_pages=4,
        )

        self.assertEqual(pagination_range['current_page'], 1)

    def test_make_pagination_handles_empty_page_input(self):
        request_mock = Mock()
        request_mock.GET = {}

        _, pagination_range = make_pagination(
            request=request_mock,
            queryset=list(range(1, 101)),
            per_page=10,
            qty_pages=4,
        )

        self.assertEqual(pagination_range['current_page'], 1)

    def test_make_pagination_range_adjusts_for_out_of_bounds_start_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=-1,
        )['pagination']
        self.assertEqual([1, 2, 3, 4], pagination)

    def test_make_pagination_range_adjusts_for_out_of_bounds_stop_range(self):
        pagination = make_pagination_range(
            page_range=list(range(1, 21)),
            qty_pages=4,
            current_page=25,
        )['pagination']
        self.assertEqual([17, 18, 19, 20], pagination)
    
    def test_recipe_model_str_representation(self):
        # Cria uma receita com um título específico
        title = "Test Recipe Title"
        recipe = self.make_recipe(title=title)
        
        # Verifica se o método __str__ retorna o título corretamente
        self.assertEqual(str(recipe), title)

