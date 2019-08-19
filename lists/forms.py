# coding = utf-8

from django import forms
from lists.models import Item
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "你不能输入一个空的待办事项"
INPUT_PLACEHOLDER = "输入你想要做的事情"
DUPLICATE_ITEM_ERROR = "你已经有这个待办事项了"


class ItemForm(forms.models.ModelForm):

    class Meta:
        model = Item
        fields = ('text',)
        widgets = {
            'text': forms.fields.TextInput(attrs={
                'placeholder': INPUT_PLACEHOLDER,
                'class': 'form-control input-lg',
            })
        }
        error_messages = {
            'text': {'required': EMPTY_ITEM_ERROR}
        }

    def save(self, for_list):
        self.instance.list_id = for_list
        return super().save()


class ExistingListItemForm(ItemForm):
    def __init__(self, for_list, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.instance.list_id = for_list

    def validate_unique(self):
        try:
            self.instance.validate_unique()
        except ValidationError as w:
            w.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
            self._update_errors(w)

    def save(self):
        return forms.models.ModelForm.save(self)
