# -*- mode: python ; coding: utf-8 -*-

block_cipher = None


a = Analysis(['-', 'BLMS', 'On-Boarding', 'Validation\\version.rc', 'D:/_8ZG/_TOOLS/PyCharm/CTCOB17 - BLMS On-Boarding Validation/CTCOB17 - BLMS On-Boarding Validation.py'],
             pathex=['D:\\_8ZG\\_TOOLS\\PyCharm\\CTCOB17 - BLMS On-Boarding Validation'],
             binaries=[],
             datas=[('D:/_8ZG/_TOOLS/PyCharm/CTCOB17 - BLMS On-Boarding Validation/icons', 'icons/'), ('D:/_8ZG/_TOOLS/PyCharm/CTCOB17 - BLMS On-Boarding Validation/CTCOB17 - BLMS On-Boarding Validation.ini', '.'), ('D:/_8ZG/_TOOLS/PyCharm/CTCOB17 - BLMS On-Boarding Validation/read_ini_config.py', '.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='-',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False , version='D:\\_8ZG\\_TOOLS\\PyCharm\\CTCOB17', icon='D:\\_8ZG\\_TOOLS\\PyCharm\\CTCOB17 - BLMS On-Boarding Validation\\icons\\atombondelectronmoleculescience_123078.ico')
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='-')
