from unittest.mock import patch

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .base import RecipeBaseFunctionalTest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

@pytest.mark.functional_test
class RecipeHomePageFunctionalTest(RecipeBaseFunctionalTest):
    def test_recipe_home_page_without_recipes_not_found_message(self):
        self.browser.get(self.live_server_url)
        body = self.browser.find_element(By.TAG_NAME, 'body')
        self.assertIn('No recipes found here 🥺', body.text)

    @patch('recipes.views.PER_PAGE', new=2)
    def test_recipe_search_input_can_find_correct_recipes(self):
        recipes = self.make_recipe_in_batch()

        title_needed = 'This is what I need'
        recipes[0].title = title_needed
        recipes[0].save()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Aguarda o campo de busca estar presente
        search_input = WebDriverWait(self.browser, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, '//input[@placeholder="Search for a recipe"]')
            )
        )

        # Digita o título e envia
        search_input.send_keys(title_needed)
        search_input.send_keys(Keys.ENTER)

        # Aguarda a presença do resultado atualizado após ENTER
        WebDriverWait(self.browser, 10).until(
            EC.text_to_be_present_in_element(
                (By.CLASS_NAME, 'main-content-list'),
                title_needed
            )
        )

        # Agora reobtém o elemento para evitar o stale reference
        content_list = self.browser.find_element(
            By.CLASS_NAME, 'main-content-list'
        )

        # Verifica se o título está visível
        self.assertIn(title_needed, content_list.text)
        
    @patch('recipes.views.site.PER_PAGE', new=2)
    def test_recipe_home_page_pagination(self):
        self.make_recipe_in_batch()

        # Usuário abre a página
        self.browser.get(self.live_server_url)

        # Vê que tem uma paginação e clica na página 2
        page2 = self.browser.find_element(
            By.XPATH,
            '//a[@aria-label="Go to page 2"]'
        )
        page2.click()

        # Vê que tem mais 2 receitas na página 2
        self.assertEqual(
            len(self.browser.find_elements(By.CLASS_NAME, 'recipe')),
            2
        )