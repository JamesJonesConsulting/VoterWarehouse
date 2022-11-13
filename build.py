import PyInstaller.__main__

PyInstaller.__main__.run([
    'voterwarehouse.py',
    '--onefile',
    '--windowed',
    '--hidden-import=Import.Florida',
    '--hidden-import=Warehouse.Florida'
])
