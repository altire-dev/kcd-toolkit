pyinstaller ^
    --noupx^
    -F --noconsole --clean ^
    -n kcd-mod-suite-v1.0.0^
    --upx-dir=..\resources\upx-4.2.4-win64^
    --paths ..\kcd-mod-generator^
    --paths ..\kcd-pak-builder^
    --paths ..\kcd-asset-finder^
    --paths ..\kcd-utils^
    --icon=.\kcd_mod_suite\resources\icon.ico^
    .\main.py