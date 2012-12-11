# Create your views here.
import pefile
from django.shortcuts import render_to_response

def exe(request):
    pe = pefile.PE('NOTEPAD.EXE')
    return render_to_response('exe.html', _pe_attr(pe))

def dll(request):
    pe = pefile.PE('PSAPI.DLL')
    return render_to_response('pe.html', {'pe': pe})

def _pe_attr(pe):
    return {'dos': pe.DOS_HEADER, 
            'dos_length': pe.DOS_HEADER.__format_length__,
            'file_header': pe.FILE_HEADER,
            'machine': pefile.MACHINE_TYPE[pe.FILE_HEADER.Machine],
            'file_header_length': pe.FILE_HEADER.__format_length__}

