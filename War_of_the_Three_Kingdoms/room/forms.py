from django import forms

from .models import Room


class RoomCreateForm(forms.ModelForm):
    private_code = forms.CharField(
        label='私人房號',
        min_length=4,
        max_length=12,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': '私人房可自訂，例如 TK001'}),
    )

    class Meta:
        model = Room
        fields = ['name', 'room_type']
        labels = {
            'name': '房間名稱',
            'room_type': '房間類型',
        }
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': '例如：桃園結義'}),
            'room_type': forms.Select(choices=Room.RoomType.choices),
        }

    def clean_private_code(self):
        code = self.cleaned_data.get('private_code', '').strip().upper()
        if code and not code.isalnum():
            raise forms.ValidationError('房號只能使用英文字母與數字。')
        if code and Room.objects.filter(code=code).exists():
            raise forms.ValidationError('這個房號已經被使用。')
        return code

    def clean(self):
        cleaned_data = super().clean()
        room_type = cleaned_data.get('room_type')
        private_code = cleaned_data.get('private_code')
        if room_type == Room.RoomType.PRIVATE and not private_code:
            self.add_error('private_code', '私人房需要設定房間號碼。')
        return cleaned_data


class PrivateRoomJoinForm(forms.Form):
    code = forms.CharField(
        label='房間號碼',
        max_length=12,
        widget=forms.TextInput(attrs={'placeholder': '輸入房號'}),
    )

    def clean_code(self):
        return self.cleaned_data['code'].strip().upper()
