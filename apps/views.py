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

def load(request, offset, _length):
    length = int(_length)
    offset = int(offset)
    data = request.session['pe']
    return HttpResponse(simplejson.dumps(
            {'digit': _toDigit(data, offset, length),
             'ascii': _toAscii(data, offset, length),
             'unicode': _toUnicode(data, offset, length),
             'position': _toPosition(offset, length),
             'offset': offset,
             'length': length,
                 }), mimetype='application/json')

def _toPosition(offset, length):
    return ''.join(_spanValue('%08X'% i, 'position-cell', 'position', i)\
                       for i in range(offset, offset+length, 16))

def _toDigit(value, offset, length):
    result = []
    for i in range(offset, offset+length):
        result.append(_spanValue('%02X' % ord(value[i]),\
                                     'digit', 'digit-cell', i))
    return ''.join(result)


def _toUnicode(value, offset, length):
    result = []
    for i in range(offset, offset+length, 2):
        try:
            val = unichr(struct.unpack('h', value[i:i+2])[0])
        except ValueError:
            val = '.'
        result.append(_spanValue(val, 'unicode', 'unicode-cell', i))
    return ''.join(result)

def _toAscii(value, offset, length):
    result = []
    for i in range(offset, offset+length):
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

