import os
import json
from . import exceptions

localstorage_writer_version='v1.0.0'

currentfile=None
loadedjson={}
metadata={}

SupportInfo=True
localstorage=loadedjson
rootidentifierstart='$$ROOT$'
localdatastart='$$LOCAL$'
metadata_separator='-'
metadata_separatorChar=44
metadata_separatorMsg='END'
metadata_bgseparatorMsg='>> START LOCALSTORAGE'
debug=False
indent=4
localstorage_file_version='no file selected'


def LocalStorageSettings(support_info=SupportInfo,debugging=debug,json_indent=indent,root_identifier_start=rootidentifierstart,local_identifier_start=localdatastart,metadata_separator_character=metadata_separator,metadata_separator_count=metadata_separatorChar,metadata_separator_message=metadata_separatorMsg,metadata_separator_innerMessage=metadata_bgseparatorMsg):
   '''
    Modify LocalStorage module settings
   '''
   global SupportInfo,debug,indent,metadata_separator,metadata_bgseparatorMsg,metadata_separatorChar,metadata_separatorMsg,rootidentifierstart,localdatastart
   SupportInfo=support_info
   debug=debugging
   indent=json_indent
   metadata_separator=metadata_separator_character
   metadata_separatorChar=metadata_separator_count
   metadata_bgseparatorMsg=metadata_separator_innerMessage
   metadata_separatorMsg=metadata_separator_message
   localdatastart=local_identifier_start
   rootidentifierstart=root_identifier_start
   return {"debugging":debug,"support_info":SupportInfo,"indent":indent,"metadata_separator_character":metadata_separator,"metadata_separator_count":metadata_separatorChar,"metadata_separator_innerMessage":metadata_bgseparatorMsg,"metadata_separator_message":metadata_separatorMsg,"root_identifier_start":rootidentifierstart,"local_identifier_start":localdatastart}

def refresh(encoding='utf-8'):
    global loadedjson,metadata,localstorage_file_version
    if os.path.exists(currentfile):
        with open(currentfile,'r',encoding=encoding) as localstorage:
          rawdata=str(localstorage.read())
          alllines=rawdata.splitlines()
          for line in alllines:
              metadatalist=[f'{localdatastart.replace('=','')}SUPPORTLINK',f'{localdatastart.replace('=','')}SUPPORTMAIL',f'{localdatastart.replace('=','')}IDENTIFIER']
              if line.startswith('$$LOCAL$') and any(required in line for required in metadatalist):
                  if 'SUPPORTLINK'in line:
                      metadata['supportlink']=line.split('=',2)[1]
                  elif 'SUPPORTMAIL' in line:
                      metadata['supportmail']=line.split('=',2)[1]
                  elif 'IDENTIFIER'in line:
                      metadata['name']=line.split('=',2)[1]
              elif line.startswith(rootidentifierstart):
                  if 'WRITER' in line:
                      localstorage_file_version=line.split('=',2)[1]
              else:
                  break
          try:
                  loadedjson=json.loads(rawdata.split(f'{metadata_separator}{metadata_separatorMsg}{metadata_separator*(metadata_separatorChar-len(metadata_separator)-len(metadata_separatorMsg))}',2)[1])
                  if debug:
                     print(json.loads(rawdata.split(f'{metadata_separator}{metadata_separatorMsg}{metadata_separator*(metadata_separatorChar-len(metadata_separator)-len(metadata_separatorMsg))}',2)[1]))
          except Exception as er:
                  if debug:
                      print(er)
                  if SupportInfo:
                   print(f'LocalStorage file may be corrupted or unreadable')
                   if len(metadata)!=0:
                    print('Support info >')
                    for key,value in metadata:
                      print(f'   {key}:{value}')
                   else: 
                       print('>> No support info was provided.')
                  else :
                     raise exceptions.LocalStorageReadError(f'Unable to read localstorage file {currentfile}.\nLocalStorage file may be corrupted.\n{er}')
    else:
         raise FileNotFoundError
def load(storage_file_path,encoding='utf-8'):
    'Load an existing storage file to read'
    global currentfile
    currentfile=os.path.abspath(storage_file_path)
    refresh(encoding=encoding)

def getItem(key):
    '''Get an item from Localstorage
    \n`getItem` will return None if the key is missing in localstorage
    '''
    if currentfile==None:
        raise exceptions.LocalStorageNoStorageFileSelected('You must select a localstorage file to use this function\nexample: localstorage.load(example.localstorage)')
    return loadedjson.get(key)

def setItem(key,value,encoding='utf-8'):
    '''Set a value to an item from Localstorage'''
    if currentfile==None:
        raise exceptions.LocalStorageNoStorageFileSelected('You must select a localstorage file to use this function\nexample: localstorage.load(example.localstorage)')
    global loadedjson
    loadedjson[key]=value
    try:
        if not metadata.get('supportlink'):
            metadata['supportlink']='not founnd'
        if not metadata.get('supportmail'):
            metadata['supportmail']='not found'
        if not metadata.get('name'):
            metadata['name']='not found'

        with open(currentfile,'w',encoding=encoding) as storage:
         metadatawr=f"""
{rootidentifierstart}WRITER=LOCALSTORAGE PY MODULE {localstorage_writer_version}
{localdatastart}IDENTIFIER={metadata.get('name')}
{localdatastart}SUPPORTLINK={metadata.get('supportlink')}
{localdatastart}SUPPORTMAIL={metadata.get('supportmail')}
{metadata_separator*metadata_separatorChar}
{metadata_bgseparatorMsg}
{metadata_separator}{metadata_separatorMsg}{metadata_separator*(metadata_separatorChar-(len(metadata_separatorMsg)+len(metadata_separator)))}    """
         metadatawr=metadatawr.strip()
         storage.write(f'{metadatawr}\n{json.dumps(loadedjson,indent=indent)}')
    except Exception as er:
       print(er)
       raise exceptions.LocalStorageWriteError(f'Unable to write data to localstorage file {currentfile}.\n{er}')
    
def clear(clearMetadata=False,encoding='utf-8'):
    if currentfile==None:
        raise exceptions.LocalStorageNoStorageFileSelected('You must select a localstorage file to use this function\nexample: localstorage.load(example.localstorage)')
    global loadedjson
    loadedjson.clear()
    try:
        if not clearMetadata:
            with open(currentfile,'r',encoding=encoding) as read:
                splittr=f'{metadata_separator}{metadata_separatorMsg}{metadata_separator*(metadata_separatorChar-len(metadata_separator)-len(metadata_separatorMsg))}'
                write=read.read().split(splittr,2)[0]+f'{splittr}\n'+"{ }"
        else:
            write=''

        with open(currentfile,'w',encoding=encoding) as wr:
            wr.write(write)    

    except Exception as er:
        if debug:
            print(er)
        raise exceptions.LocalStorageStorageClearError("Can't clear storage from localstorage file.")
    
def removeItem(key):
    if currentfile==None:
        raise exceptions.LocalStorageNoStorageFileSelected('You must select a localstorage file to use this function\nexample: localstorage.load(example.localstorage)')
    global loadedjson
    try:
     del loadedjson[key]
    except KeyError:
     pass


def CreateLocalstorageFile(path,support_site='not found',support_mail='not found',identifier='not found',encoding='utf-8'):
    if os.path.exists(path):
       raise exceptions.LocalStorageFileAlreadyExist(f"{path} file already exist. If you're trying to load a localstorage file use load() instead of CreateLocalstorageFile()")
    else:
       with open(os.path.abspath(path),'w',encoding=encoding) as new:
            metadata=f"""
{rootidentifierstart}WRITER={localstorage_writer_version}
{localdatastart}IDENTIFIER={identifier}
{localdatastart}SUPPORTLINK={support_site}
{localdatastart}SUPPORTMAIL={support_mail}
{metadata_separator*metadata_separatorChar}
{metadata_bgseparatorMsg}
{metadata_separator}{metadata_separatorMsg}{metadata_separator*(metadata_separatorChar-(len(metadata_separatorMsg)+len(metadata_separator)))}
            """
            metadata=metadata.strip()
            new.write(metadata)
            return path

def LocalstorageFileExists(path):
    """Returns True if Localstorage file already exists"""
    return os.path.exists(os.path.abspath(path))

#runtimeglobal
__all__=[
    "LocalStorageSettings",
    "load",
    "getItem",
    "setItem",
    "clear",
    "removeItem",
    "CreateLocalstorageFile",
    "localstorage_writer_version",
    "localstorage_file_version",
    "LocalstorageFileExists"
]