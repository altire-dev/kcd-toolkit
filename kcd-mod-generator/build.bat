pyinstaller ^
    --noupx^
    -F --noconsole --clean ^
    -n kcd-mod-generator-v0.0.1^
    --upx-dir=..\resources\upx-4.2.4-win64^
    --icon=.\kcd_mod_generator\resources\icon.ico^
    --add-data kcd_mod_generator\resources\icon.ico:resources^
    .\main.py