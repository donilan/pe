import struct, pefile

"""
PE resource util

"""

def resource(pe, typeId, rva, size):
    return _resourceFn.get(typeId, unknowResource)(pe, rva, size)

def unknowResource(*arg):
    return "unknow resource."


def menuResource(pe, rva, size):
    """
    Parse menu resource
    """
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

def rtResource(pe, rva, size):
    offset = 0
    strings = []
    print hex(pe.get_offset_from_rva(rva))
    while True:
        if offset >= size:
            break
        _offset, _str = _readerUnicode(pe, rva+offset)
        offset += _offset
        strings.append(_str)
    return '<pre>' + ''.join(strings) + '</pre>'

def iconGroupResource(pe, rva, size):
    data = pe.get_memory_mapped_image()[rva: rva+size]
    result = ['Type: ']
    tmp = struct.unpack('h', data[2:4])[0]
    if tmp == 1:
        result.append('ICON')
    elif tmp == 2:
        result.append('Cursor')
    else:
        result.append('Unknow')
    result.append('<br/>Image count: ')
    count = struct.unpack('h', data[4:6])[0]
    result.append(str(count))
    result.append('<br/>')
    base = 6
    for i in range(0, count):
        idx = base + i*14
        result.append("Image[%d], width: %d, height: %d, color: %02d, planes: 0x%X, bit count: 0x%02X, data size: 0x%04X, relate offset: %d<br />" \
            % (i+1, 
               ord(struct.unpack('c', data[idx:idx+1])[0]),
               ord(struct.unpack('c', data[idx+1:idx+2])[0]),
               ord(struct.unpack('c', data[idx+2:idx+3])[0]),
               struct.unpack('h', data[idx+4:idx+6])[0],
               struct.unpack('h', data[idx+6:idx+8])[0],
               struct.unpack('l', data[idx+8:idx+12])[0],
               struct.unpack('h', data[idx+12:idx+14])[0]
               ))
    return ''.join(result)

def _iconResource(pe):
    rt_group_icon_idx = [entry.id for entry in \
                             pe.DIRECTORY_ENTRY_RESOURCE.entries]\
                             .index(pefile.RESOURCE_TYPE['RT_GROUP_ICON'])
    rt_icon_idx = [entry.id for entry in \
                             pe.DIRECTORY_ENTRY_RESOURCE.entries]\
                             .index(pefile.RESOURCE_TYPE['RT_ICON'])
    iconGroupDir = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_group_icon_idx]
    iconDir = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_icon_idx]
    result = {'type': None, 'count': None, 'iconGroup': [], 'icons': [] }
    for entry in iconGroupDir.directory.entries:
        for en in entry.directory.entries:
            rva = en.data.struct.OffsetToData
            size = en.data.struct.Size
            data = pe.get_memory_mapped_image()[rva: rva+size]
            result['type'] = struct.unpack('h', data[2:4])[0]
            result['count'] = struct.unpack('h', data[4:6])[0]
            for i in range(0, result['count']):
                r = {}
                idx = i*14+6
                r['width'] = ord(struct.unpack('c', data[idx:idx+1])[0])
                r['height'] = ord(struct.unpack('c', data[idx+1:idx+2])[0])
                r['color'] = ord(struct.unpack('c', data[idx+2:idx+3])[0])
                r['planes'] = struct.unpack('h', data[idx+4:idx+6])[0]
                r['bitCount'] = struct.unpack('h', data[idx+6:idx+8])[0]
                r['dataSize'] = struct.unpack('l', data[idx+8:idx+12])[0]
                r['relateOffset'] = struct.unpack('h', data[idx+12:idx+14])[0]
                r['data'] = data[:6] + data[idx:idx+14]
                result['iconGroup'].append(r)
    for entry in iconDir.directory.entries:
        for en in entry.directory.entries:
            rva = en.data.struct.OffsetToData
            size = en.data.struct.Size
            data = pe.get_memory_mapped_image()[rva: rva+size]
            r = {'rva': rva, 'size': size, 'data': data}
            result['icons'].append(r)
    return result

def _iconGroup(pe):
    rt_group_icon_idx = [entry.id for entry in \
                             pe.DIRECTORY_ENTRY_RESOURCE.entries]\
                             .index(pefile.RESOURCE_TYPE['RT_GROUP_ICON'])
    iconGroupDir = pe.DIRECTORY_ENTRY_RESOURCE.entries[rt_group_icon_idx]
    en = iconGroupDir.directory.entries[0].directory.entries[0]
    rva = en.data.struct.OffsetToData
    size = en.data.struct.Size
    data =  pe.get_memory_mapped_image()[rva: rva+size]
    count = struct.unpack('h', data[4:6])[0]
    newData = data[:6]
    for i in range(0, count):
        base = 6 + i*14
        tmp = ''.join([data[base:base+12], chr(count*0x10+6), chr(0)*3])
        newData += tmp
    return newData

# not work
def iconResource(pe, rva, size):
    icon = _iconGroup(pe) + pe.get_memory_mapped_image()[rva: rva+size]
#    f = open('img-'+str(rva)+'.ico', 'wb')
#    f.write(icon)
#    f.close()
    return '<img src="data:iamge/ico;base64,' + icon.encode('base64') + '" />'


def _readerUnicode(pe, rva):
    data = pe.get_memory_mapped_image()[rva:]
    offset = 0
    result = []
    while True:
        ustr = pe.get_word_from_data(data[offset:offset+2],0)
        offset += 2
        result.append(unichr(ustr))
        if ustr == 0:
            break
    return (offset, ''.join(result))


_resourceFn = {
    3: iconResource,
    4: menuResource,
    6: rtResource,
    14: iconGroupResource,
    }
