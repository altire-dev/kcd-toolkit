pyinstaller ^
    --noupx^
    -F --noconsole --clean ^
    -n kcd-asset-finder-v1.0.0^
    --upx-dir=..\resources\upx-4.2.4-win64^
    --icon=.\kcd_asset_finder\resources\icon.ico^
    --add-data kcd_asset_finder\resources\icon.ico:resources^
    .\main.py