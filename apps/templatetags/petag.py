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

@register.filter(name='file_header_characteristics', is_safe=True)
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

@register.filter(name='op_header_dll_characteristics', is_safe=True)
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

@register.filter(name='section_characteristics', is_safe=True)
def section_characteristics(value):
    result = ''
    for v, k in pefile.section_characteristics:
        if value & k > 0:
            result += v + '<br />\n'
    return result

@register.filter(name='timestamp')
def timestampFn(value):
    return time.asctime(time.gmtime(value))

@register.filter(name='peType')
def peType(value):
    if pefile.OPTIONAL_HEADER_MAGIC_PE == value:
        return 'Optional header magic pe'
    elif pefile.OPTIONAL_HEADER_MAGIC_PE_PLUS == value:
        return 'Optional header magic pe plus'

@register.filter(name='resourceType')
def resourceType(value):
    for v,k in pefile.resource_type:
        if k == value:
            return v
    return 'Unknow'

@register.filter(name='lang')
def lang(value):
    return pefile.LANG[value]
        

@register.simple_tag(takes_context=True, name='out')
def outFn(context, value, title, important=False):
    if important:
        important = 'important'
    else:
        important = ''

    if isinstance(value, bool):
        value = 'True' if value else 'False'
    elif isinstance(value, int) or isinstance(value, long):
        value = str(value)
    
    return ''.join(['<td class="title">', title,
                    '</td><td class="value ',
                    important, '">', value, '</td>'])

@register.simple_tag(takes_context=True, name='peResource')
def peResource(context, pe, rva, size, typeId):

    # RT_STRING
    if typeId == 6:
        data = pe.get_memory_mapped_image()[rva:rva+size]
        offset = 0
        strings = []
        while True:
            if offset >= size:
                break
            ustr_length = pe.get_word_from_data(data[offset:offset+2],0)
            offset += 2
            if ustr_length == 0:
                continue
            ustr = pe.get_string_u_at_rva(rva+offset, max_length=ustr_length)
            offset += ustr_length*2
            strings.append(ustr)

        return '<ol>' + ''.join(['<li>' +s + '</li>'for s in strings]) + '</ol>'
    else:
        return '-'
    
