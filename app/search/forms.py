from django import forms

class User_Inputs(forms.Form):
    department = forms.CharField(
        label='出発地'
    )

    destination = forms.CharField(
        label='目的地'
    )

    priority = forms.fields.ChoiceField(
        label='優先事項',
        choices = (
            ('TIME', '時間優先'),
            ('COST', '費用優先'),
        ),
        widget=forms.widgets.Select   
    )

    # travel_mode = forms.fields.ChoiceField(
    #     label='交通手段',
    #     choices = (
    #         ('walking', '徒歩'),
    #         ('bicycle', '自転車'),
    #         ('driving', '車'),
    #     ),
    #     widget=forms.widgets.Select
    # )


    staying_time = forms.IntegerField(
        label='滞在時間',
        help_text='分'
    ) #分表記

    # has_rental = forms.fields.ChoiceField(
    #     label='レンタルを',
    #     choices = (
    #         (1, '利用する'),
    #         (0, '利用しない')
    #     ),
    #     widget=forms.widgets.Select,
    #     disabled=False,
    # )
