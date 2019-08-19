# coding = utf-8

from django.test import TestCase
from lists.forms import ItemForm, EMPTY_ITEM_ERROR, INPUT_PLACEHOLDER
from lists.forms import ExistingListItemForm, DUPLICATE_ITEM_ERROR

from lists.models import Item, List

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

    def test_form_save_handles_saving_to_list(self):
        list_ = List.objects.create()
        form = ItemForm(data={'text': 'do me'})
        new_item = form.save(for_list=list_)
        self.assertEqual(new_item, Item.objects.first())
        self.assertEqual(new_item.text, 'do me')
        self.assertEqual(new_item.list_id, list_)


class ExistingListItemFormTest(TestCase):

    def test_form_renders_item_text_input(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_)
        self.assertIn(f'placeholder="{INPUT_PLACEHOLDER}"', form.as_p())

    def test_form_validation_for_blank_items(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(data={'text': ''}, for_list=list_)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [EMPTY_ITEM_ERROR])
        # form.save()

    def test_form_save_handles_saving_to_list(self):
        list_ = List.objects.create()
        Item.objects.create(list_id=list_, text='no twins!')
        form = ExistingListItemForm(data={'text': 'no twins!'}, for_list=list_)

        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['text'], [DUPLICATE_ITEM_ERROR])

    def test_form_save(self):
        list_ = List.objects.create()
        form = ExistingListItemForm(for_list=list_, data={'text': 'test_save'})
        new_item = form.save()
        self.assertEqual(new_item, Item.objects.all()[0])
