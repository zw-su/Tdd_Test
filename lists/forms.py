# coding = utf-8

from django import forms
from lists.models import Item

EMPTY_ITEM_ERROR = "你不能输入一个空的待办事项"
INPUT_PLACEHOLDER = "输入你想要做的事情"


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
