from dajax.core import Dajax

def multiply(request, a, b):
    dajax = Dajax()
    result = int(a) * int(b)
    dajax.assign('#result','value',str(result))
    return dajax.json()

from django.utils import simplejson
from dajaxice.decorators import dajaxice_register

@dajaxice_register
def dajaxice_example(request):
    return simplejson.dumps({'message':'Hello from Python!'})
