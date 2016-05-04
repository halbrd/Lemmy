@Echo off
chcp 65001
:Start

python RunLemmy.py
timeout 3

goto Start