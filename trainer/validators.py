# import datetime
# from django.core.exceptions import ValidationError
#
#
# def validate_date(date):
#     if datetime.datetime.strptime(str(date), '%Y-%m-%d') > datetime.datetime.now():
#         print('test')
#         raise forms.ValidationError('test')
#     return date
