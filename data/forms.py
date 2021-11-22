from django import forms
from .validators import validate_file_extension
from .models import Document


# class UploadFileForm(forms.Form):
#     file = forms.FileField(validators=[validate_file_extension])
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['file'].label = "File"
#         self.fields['file'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Upload File'})


class UploadFileForm(forms.ModelForm):
    published_year = forms.DateField(label='date',
                                     widget=forms.DateInput(format="12-06-2018",
                                                            attrs={'class': 'form-control',
                                                                   'type': 'date'}
                                                            ),
                                     )

    class Meta:
        model = Document
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['document_title'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Document Title',
                                                           'style': 'margin-top: 8px; margin-bottom: 8px'})
        self.fields['resource_url'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Document Source Url',
                                                         'style': 'margin-top: 8px; margin-bottom: 8px'})
        self.fields['author_name'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Author Name',
                                                        'style': 'margin-top: 8px; margin-bottom: 8px'})
        self.fields['published_year'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Published Year',
                                                           'style': 'margin-top: 8px; margin-bottom: 8px'})
        self.fields['description'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Description',
                                                        'style': 'margin-top: 8px; margin-bottom: 8px'})
        self.fields['number_of_pages'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Number of Pages',
                                                            'style': 'margin-top: 8px; margin-bottom: 8px'})
        self.fields['file'].widget.attrs.update({'class': 'form-control', 'placeholder': 'File',
                                                 'style': 'margin-top: 8px; margin-bottom: 8px'})
