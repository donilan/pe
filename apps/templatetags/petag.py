from django import template
import pefile, time

register = template.Library()

@register.filter(name='hex')
def hexFn(value, fmt='0x%X'):
    if isinstance(value, str):
        return ''.join([ '\\x%X' % ord(s) for s in value])
    elif isinstance(value, int) or isinstance(value, long):
        return fmt % value
    return value

@register.filter(name='hex4')
def hex4Fn(value):
    return hexFn(value, '0x%04X')

@register.filter(name='hex8')
def hex8Fn(value):
    return hexFn(value, '0x%08X')

@register.filter(name='file_header_characteristics')
def file_header_characteristics(value):
    if isinstance(value, int):
        result = '<table cellspacing="0" cellpadding="0" style="width: 300px;" >\n'
        for k, v in filter(lambda a: isinstance(a[0], int), pefile.IMAGE_CHARACTERISTICS.items()):
            result += '<tr><td class="title">'+ v+ '</td><td>'
            if value & k > 0:
                result += '<span class="important">True</span>'
            else:
                result += 'False'
            result += '</td></tr>\n'

        result += '</table>'
        return result
    else:
        return value

@register.filter(name='op_header_dll_characteristics')
def op_header_dll_characteristics(value):
    result = '<table cellspacing="0" cellpadding="0" style="width: 300px;" >\n'
    for v, k in pefile.dll_characteristics:
        result += '<tr><td class="title">'+ v+ '</td><td>'
        if value & k > 0:
            result += '<span class="important">True</span>'
        else:
            result += 'False'
        result += '</td></tr>\n'
    result += '</table>'
    return result

@register.filter(name='timestamp')
def timestampFn(value):
    return time.asctime(time.gmtime(value))

@register.simple_tag(takes_context=True, name='out')
def outFn(context, value, title, important=False):
    if important:
        important = 'important'
    else:
        important = ''

    if isinstance(value, int) or isinstance(value, long):
        value = hexFn(value)

    return ''.join(['<td class="title">', title,
                    '</td><td class="value ',
                    important, '">', value, '</td>'])
