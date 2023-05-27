import PyInstaller.__main__

PyInstaller.__main__.run([
    'voterwarehouse.py',
    '--onefile',
    '--nowindowed',
    '--hidden-import=Import.Florida',
    '--hidden-import=Warehouse.Florida',
    '--hidden-import=Import.State',
    '--hidden-import=Warehouse.State'
])
