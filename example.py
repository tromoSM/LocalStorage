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

# Clear storage file
localstorage.clear()

# Debugging
localstorage.LocalStorageSettings(debugging=True) # set this before other functions to debug correctly