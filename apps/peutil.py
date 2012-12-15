import struct

"""
PE resource util

"""




def resource(pe, typeId, rva, size):
    _resourceFn[typeId](pe, rva, size)

def menuResource(pe, rva, size):
    rva += 4
    data = pe.get_memory_mapped_image()[rva:rva+size]
    offset = 0
    menuStr = ['<pre>']
    while offset < size-4:
        itemFlags = struct.unpack('h', data[offset:offset+2])[0]
        offset += 2
        
        # POPUP menu
        if 0x0010 & itemFlags > 0:
            menuStr.append('POPUP ')
            _offset, _str = _readerUnicode(pe, rva+offset)
            offset += _offset
            menuStr.append(_str)
            menuStr.append('\n')
            menuStr.append('BEGIN\n')
        else:
            menuId = struct.unpack('h', data[offset:offset+2])[0]
            offset += 2
            # separator
            if menuId == 0:
                menuStr.append('\tMENUITEM SEPARATOR')
                offset += 2
            # menu item
            else:
                menuStr.append('\tMENUITEM "')
                _offset, _str = _readerUnicode(pe, rva+offset)
                offset += _offset
                menuStr.append(_str)
                menuStr.append('"\t%d' % menuId)
            menuStr.append('\n')
            if 0x0080 & itemFlags > 0:
                menuStr.append('END\n')

    menuStr.append('</pre>')
    return ''.join(menuStr)

def _readerUnicode(pe, rva):
    data = pe.get_memory_mapped_image()[rva:]
    offset = 0
    result = []
    while True:
        ustr_length = pe.get_word_from_data(data[offset:offset+2],0)
        offset += 2
        if ustr_length == 0:
            break
    result.append(pe.get_string_u_at_rva(rva, max_length=offset))
    return (offset, ''.join(result))


_resourceFn = {4: menuResource}
