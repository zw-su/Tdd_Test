# coding = utf-8

from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR, INPUT_PLACEHOLDER

'''表单的单元测试'''


class ItemFormTest(TestCase):

    def test_form_renders_text_input(self):
        form = ItemForm()
        print(form.as_p())

    def test_form_item_input_has_placeholder_and_css(self):
        form = ItemForm()
        self.assertIn(f'placeholder="{INPUT_PLACEHOLDER}"', form.as_p())
        self.assertIn('class="form-control input-lg"', form.as_p())

    def test_form_validation_for_blank_items(self):
        form = ItemForm(data={'text': ''})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
        # form.save()
