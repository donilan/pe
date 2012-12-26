# Create your views here.
import pefile,string,struct
from django.shortcuts import render_to_response
from django.utils import simplejson
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse

def upload(request):
    return render_to_response('upload.html')


@csrf_exempt
def parse(request):
    f = request.FILES['file']
    if f:
        data = f.read()
        request.session['pe'] = data
        return render_to_response('parse.html')
    else:
        return render_to_response('upload.html', {'error': True})

def load(request, offset):
    data = request.session['pe']
    tmp = data[int(offset): 512]
    return HttpResponse(simplejson.dumps(
            {'digit': _toDigit(tmp),
             'ascii': _toAscii(tmp),
             'unicode': _toUnicode(tmp),
                 }), mimetype='application/json')

def _toDigit(value):
    result = []
    for i in range(0, len(value)):
        result.append(_spanValue('%02X' % ord(value[i]), 'data', 'data-cell', i))
    return ''.join(result)


def _toUnicode(value):
    result = []
    for i in range(0, len(value), 2):
        try:
            val = unichr(struct.unpack('h', value[i:i+2])[0])
        except ValueError:
            val = '.'
        result.append(_spanValue(val, 'unicode', 'unicode-cell', i))
    return ''.join(result)

def _toAscii(value):
    result = []
    for i in range(0, len(value)):
        val = value[i]
        if not val in string.printable:
            val = '.'
        result.append(_spanValue(val, 'ascii', 'ascii-cell', i))
    return ''.join(result)

def _spanValue(value, _id, clazz, idx):
    return ''.join([
            '<span id="%s-%d" class="cell %s" >' % (_id, idx, clazz),
            value,
            '</span>'])

