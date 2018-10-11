from guicreater import guiCreater
#Console print messages can switch off and on hier
global printMessages
printMessages = False
window = guiCreater.Gui()
window.mainloop()
window.__exit__()
