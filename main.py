#!/usr/bin/python3
# coding=utf-8
from guicreater import guiCreater
#Console print messages can switch off and on hier
window = guiCreater.Gui()
window.localtime()
window.visualizationData()
#window.switchOffHysteresis()
window.mainloop()
window.__exit__()
