from django.forms.widgets import ClearableFileInput
from django.utils.translation import gettext_lazy as _


class CustomClearableFileInput(ClearableFileInput):
    """
    For Admin UI Book Editing.
    """
    clear_checkbox_label = _('Remove')
    initial_text = _('Current Cover')
    input_text = _('')
    template_name = 'reader/custom_widget_templates/custom_clearable_file_input.html'
