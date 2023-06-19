import random
import string
from django.db.models.signals import pre_save
from ..experts.models import *

def refer_code_gen(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def unique_reference_code_generator(instance):
	"""This will generate reference code  that will be unique"""
	reference_code_new = refer_code_gen()
	Klass= instance.__class__
	qs_exists= 	Klass.objects.filter(refer_code=reference_code_new).exists()
	if qs_exists:
		return unique_reference_code_generator(instance)
	return reference_code_new

def pre_save_create_user_id(sender, instance, *args, **kwargs):
    instance.refer_code = unique_reference_code_generator(instance)
pre_save.connect(pre_save_create_user_id, sender=UserAccount)