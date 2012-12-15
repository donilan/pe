# Create your views here.
import pefile
from django.shortcuts import render_to_response

def exe(request):
    pe = pefile.PE('NOTEPAD.EXE')
#    pe = pefile.PE('helloWorld.exe')
    return render_to_response('exe.html', _pe_attr(pe))

def dll(request):
    pe = pefile.PE('PSAPI.DLL')
    return render_to_response('dll.html', _pe_attr(pe))

def _pe_attr(pe):
    resource = None
    resourceLength = 0
    if hasattr(pe, 'DIRECTORY_ENTRY_RESOURCE'):
        resource = pe.DIRECTORY_ENTRY_RESOURCE
        resourceLength = resource.struct.__format_length__

    return {'pe': pe,
            'dos': pe.DOS_HEADER, 
            'dos_length': pe.DOS_HEADER.__format_length__,
            'file_header': pe.FILE_HEADER,
            'machine': pefile.MACHINE_TYPE[pe.FILE_HEADER.Machine],
            'file_header_length': pe.FILE_HEADER.__format_length__,
            'op_header': pe.OPTIONAL_HEADER,
            'op_header_length': pe.OPTIONAL_HEADER.__format_length__,
            'resource': resource,
            'resource_length': resourceLength,
            }

