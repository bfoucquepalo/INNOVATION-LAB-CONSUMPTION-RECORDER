# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['/Users/benoitfoucque/GITHUB_PALOIT_HK/INNOVATION-LAB-CONSUMPTION-RECORDER/consumption_recorder_v2.py'],
             pathex=[],
             binaries=[],
             datas=[('consumption_recorder_ux_definition_v2.kv','.'),('PALOIT_LOGO_200-200.jpeg','.')],
             hiddenimports=[],
             hookspath=[],
             hooksconfig={},
             runtime_hooks=[],
             excludes=['_tkinter', 'Tkinter', 'enchant', 'twisted'],
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
          name='paloit_carbon_analyser',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=False,
          disable_windowed_traceback=False,
          target_arch=None,
          codesign_identity=None,
          entitlements_file=None )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas, 
               strip=False,
               upx=True,
               upx_exclude=[],
               name='paloit_carbon_analyser'
               )
app = BUNDLE(coll,
             name='paloit_carbon_analyser.app',
             icon='PALOIT_LOGO_200-200.jpeg',
             bundle_identifier=None)
