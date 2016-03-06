set ws=wscript.createobject("wscript.shell")
ws.run "start.bat /start",0
ws.run "backup.bat /start",0
wscript.quit