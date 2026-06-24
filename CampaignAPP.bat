color a
@echo off
cd /d %~dp0
 streamlit run final_working.py --server.address 192.168.10.180  --server.port 8508
pause
