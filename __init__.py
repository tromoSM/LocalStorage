import os
import json
from localstorage import exceptions

localstorage_writer_version='v1.0.0'

currentfile=None
loadedjson={}
metadata={}

SupportInfo=True
localstorage=loadedjson
rootidentifierstart='$$ROOT$'
localdatastart='$$LOCAL$'
metadata_seperator='-'
metadata_seperatorChar=44
metadata_seperatorMsg='END'
metadata_bgseperatorMsg='>> START LOCALSTORAGE'
debug=False
indent=4

def LocalStorageSettings(support_info=SupportInfo,debugging=debug,json_indent=4):
   global SupportInfo,debug,indent
   SupportInfo=support_info
   debug=debugging
   indent=json_indent
   return {"debugging":debug,"support_info":SupportInfo,"indent":indent}

def refresh(encoding='utf-8'):
    global loadedjson,metadata
    if os.path.exists(currentfile):
        with open(currentfile,'r',encoding=encoding) as localstorage:
          rawdata=str(localstorage.read())
          alllines=rawdata.splitlines()
          for line in alllines:
              metadatalist=['$$LOCAL$SUPPORTLINK','$$LOCAL$SUPPORTMAIL','$$LOCAL$IDENTIFIER']
              if line.startswith('$$LOCAL$') and any(required in line for required in metadatalist):
                  if 'SUPPORTLINK'in line:
                      metadata['supportlink']=line.split('=',2)[1]
                  elif 'SUPPORTMAIL' in line:
                      metadata['supportmail']=line.split('=',2)[1]
                  elif 'IDENTIFIER'in line:
                      metadata['name']=line.split('=',2)[1]
              else:
                  break
          try:
                  loadedjson=json.loads(rawdata.split(f'{metadata_seperator}{metadata_seperatorMsg}{metadata_seperator*(metadata_seperatorChar-len(metadata_seperator)-len(metadata_seperatorMsg))}',2)[1])
                  if debug:
                     print(json.loads(rawdata.split(f'{metadata_seperator}{metadata_seperatorMsg}{metadata_seperator*(metadata_seperatorChar-len(metadata_seperator)-len(metadata_seperatorMsg))}',2)[1]))
          except Exception as er:
                  if debug:
                      print(er)
                  if SupportInfo:
                   print(f'LocalStorage file may be corrupted or unreadable'),
                   print('Support info >')
                   for key,value in metadata:
                      print(f'   {key}:{value}')
                  else :
                     raise exceptions.LocalStorageReadError(f'Unable to read localstorage file {currentfile}.\nLocalStorage file may be corrupted.\n{er}')
    else:
         raise FileNotFoundError
def load(storage_file_path,encoding='utf-8'):
    global currentfile
    currentfile=os.path.abspath(storage_file_path)
    refresh()

def getItem(key):
    if currentfile==None:
        raise exceptions.LocalStorageNoStorageFileSelected('You must select a localstorage file to use this function\nexample: localstorage.load(example.localstorage)')
    return loadedjson.get(key)

def setItem(key,value,encoding='utf-8'):
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
{rootidentifierstart}WRITER={localstorage_writer_version}
{localdatastart}IDENTIFIER={metadata.get('name')}
{localdatastart}SUPPORTLINK={metadata.get('supportlink')}
{localdatastart}SUPPORTMAIL={metadata.get('supportmail')}
{metadata_seperator*metadata_seperatorChar}
{metadata_bgseperatorMsg}
{metadata_seperator}{metadata_seperatorMsg}{metadata_seperator*(metadata_seperatorChar-(len(metadata_seperatorMsg)+len(metadata_seperator)))}    """
         metadatawr=metadatawr.strip()
         storage.write(f'{metadatawr}\n{json.dumps(loadedjson,indent=indent)}')
    except Exception as er:
       print(er)
       raise exceptions.LocalStorageWriteError(f'Unable to write data to localstorage file {currentfile}.\n{er}')
    
def clear():
    if currentfile==None:
        raise exceptions.LocalStorageNoStorageFileSelected('You must select a localstorage file to use this function\nexample: localstorage.load(example.localstorage)')
    global loadedjson
    loadedjson.clear()

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
{metadata_seperator*metadata_seperatorChar}
{metadata_bgseperatorMsg}
{metadata_seperator}{metadata_seperatorMsg}{metadata_seperator*(metadata_seperatorChar-(len(metadata_seperatorMsg)+len(metadata_seperator)))}
            """
            metadata=metadata.strip()
            new.write(metadata)
            return path