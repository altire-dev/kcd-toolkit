pyinstaller ^
    --noupx^
    -F --noconsole --clean ^
    -n kcd-pak-builder-v1.2.1^
    --upx-dir=..\resources\upx-4.2.4-win64^
    --icon=.\kcd_pak_builder\resources\icon.ico^
    --add-data kcd_pak_builder\resources\icon.ico:resources^
    .\main.py