pyinstaller ^
    --noupx^
    -F --noconsole --clean ^
    -n kcd-mod-generator-v1.1.2^
    --upx-dir=..\resources\upx-4.2.4-win64^
    --icon=.\kcd_mod_generator\resources\icon.ico^
    --add-data kcd_mod_generator\resources\icon.ico:resources^
    --add-data kcd_mod_generator\resources\modding_eula.txt:resources^
    --paths ..\kcd-core^
    .\main.py