import os
from datetime import datetime
import subprocess
import shutil



# 打包應用程式並且將須需要用到的檔案複製到指定目錄
#


VERSION = '1.2'
BUILD_TIME = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
MAKE_RESULT_DIR = f'.MAKE_RESULT/{BUILD_TIME}/馬達測試系統V{VERSION}'
os.makedirs(MAKE_RESULT_DIR, exist_ok=True)


# EXEC COMMAND pyinstaller --onefile main.py

# 執行 pyinstaller 並指定輸出與中間檔路徑
subprocess.run([
    'pyinstaller', '--onefile', 'main.py',
    '--distpath', MAKE_RESULT_DIR,
    '--workpath', os.path.join(MAKE_RESULT_DIR, 'work'),
    '--specpath', os.path.join(MAKE_RESULT_DIR, 'spec'),
    '--noconfirm', '--clean'
], check=True)

print(f'[make.py] remove work and spec directories in {MAKE_RESULT_DIR}...')
shutil.rmtree(
    os.path.join(MAKE_RESULT_DIR, 'work'), ignore_errors=True
)
shutil.rmtree(
    os.path.join(MAKE_RESULT_DIR, 'spec'), ignore_errors=True
)


# cp resources

# 1 device.ini
print(f'[make.py] copy device.ini to {MAKE_RESULT_DIR}...')
shutil.copy('device.ini', MAKE_RESULT_DIR)
# 2 dir font
print(f'[make.py] copy font directory to {MAKE_RESULT_DIR}...')
shutil.copytree('font', os.path.join(MAKE_RESULT_DIR, 'font'))
# 3 report template
print(f'[make.py] copy report_template directory to {MAKE_RESULT_DIR}...')
shutil.copytree('report_template', os.path.join(MAKE_RESULT_DIR, 'report_template'))
# convert.exe
print(f'[make.py] copy convert.exe to {MAKE_RESULT_DIR}...')
shutil.copy('convert.exe', MAKE_RESULT_DIR)

print(f'[make.py] successfully created the application in {MAKE_RESULT_DIR}.')