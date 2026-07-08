# LocalStorage 
### Localstorage for python with more features
---
## Installation 
```bash
pip install localstorage
```
## Usage (example)
```python
import localstorage

# Create localstorage file if doesnt exist
if localstorage.LocalstorageFileExists('example.localstorage'):
 localstorage.load('example.localstorage')
else:
 localstorage.load(localstorage.CreateLocalstorageFile('example.localstorage'))

# Set Item
localstorage.setItem('Example',"123")
# Get item
print(localstorage.getItem('Example'))

# Clear all items in storage
localstorage.clear()

# Debugging
localstorage.LocalStorageSettings(debugging=True) # set this before other functions to debug correctly
```
### Features
- support info if the file is unreadable
- identifier
- full control over which file contains the data
- change encoding
- add metadata (supportlink,supportmail,identifier)

### About
- [feedback or requests](https://tromosm.gt.tc/?feedback=true&utm_source=feedpylocal_st_readmeorpypi)
- [other projects from developer](https://tromosm.gt.tc/?utm_source=othrpylocal_st_readmeorpypi)
