
import sys
import os
import subprocess

import wx

class MainFrame(wx.Frame):

    def __init__(self, parent, id):
        wx.Frame.__init__(self, parent, id, 'Log Collecter', size = (400,450))
		
        mypanel = wx.Panel(self)
        vbox = wx.GridSizer(5, 2, 0, 0)
        self.txtc1 = wx.TextCtrl(mypanel, -1, 'C:\Perflogs\QA')
        self.txtc2 = wx.TextCtrl(mypanel, -1, 'D')
        self.txtc3 = wx.TextCtrl(mypanel, -1, 'Y')
        self.txtc4 = wx.TextCtrl(mypanel, -1, 'D:\Logs\\')
        vbox.AddMany([ (wx.StaticText(mypanel, -1, 'Folder with logs'), 0, wx.ALIGN_CENTER), (self.txtc1, 0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL),
                       (wx.StaticText(mypanel, -1, 'Disk on your PC...'), 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL), (self.txtc2,0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL),
                       (wx.StaticText(mypanel, -1, 'will be mapped as:'), 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL), (self.txtc3,0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL),
                       (wx.StaticText(mypanel, -1, 'Path to converted log on your PC'), 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL), (self.txtc4,0, wx.ALIGN_LEFT|wx.ALIGN_CENTER_VERTICAL)] )
        #Buttons Collect and exit
        collectbtn = wx.Button(mypanel, label= 'Collect!', size= (100, 40))
        exitbtn = wx.Button(mypanel, label= 'Exit', size= (100, 40))
        vbox.Add(collectbtn, 0, wx.ALIGN_CENTER, 45)
        vbox.Add(exitbtn, 0, wx.ALIGN_CENTER, 45)
        self.Bind(wx.EVT_BUTTON, self.make_cool, collectbtn)
        self.Bind(wx.EVT_BUTTON, self.exit, exitbtn)
        self.Bind(wx.EVT_CLOSE, self.closewindow)

        mypanel.SetSizer(vbox)

        self.CreateStatusBar()
        #File and Disk menus
        filemenu = wx.Menu()
        open = filemenu.Append(wx.NewId(), 'Open', 'Open file with settings')
        self.Bind(wx.EVT_MENU, self.openbox, open)
        filemenu.Append(wx.NewId(), 'About', 'About program')

        diskmenu = wx.Menu()
        mdisk = diskmenu.Append(wx.NewId(), 'Map disk..', 'Map disk with command "net use"')
        self.Bind(wx.EVT_MENU, self.map_disk, mdisk)
        umdisk = diskmenu.Append(wx.NewId(), 'Unmap disk..', 'Delete  mapped disk')
        self.Bind(wx.EVT_MENU, self.unmap_disk, umdisk)
        #Menubar
        menubar = wx.MenuBar()
        menubar.Append(filemenu, 'File') 
        menubar.Append(diskmenu, 'Disk')
        self.SetMenuBar(menubar) 

    def unmap_disk(self, event):
        unmap_disk_box = wx.TextEntryDialog(None, 'Enter disk which must be deleted', 'Ummap disk', '')
        if unmap_disk_box.ShowModal() == wx.ID_OK:
            answer = unmap_disk_box.GetValue()
            nu = NetUse(None, answer + ':')
            nu.unmap()

    def map_disk(self, event):
        MyDialog(None, -1, 'Mapping disk')

  
    def openbox(self, event):
        box  = wx.MessageDialog(frame, 'Still not implemented functionality', 'Title', wx.YES_NO)
        box.Destroy()

    def make_cool(self, event):
        logcollecter = LogCollecter(self.txtc1.GetValue(), self.txtc4.GetValue(), self.txtc2.GetValue(), self.txtc3.GetValue())
        logcollecter.relog()

    def exit(self, event):
        self.Close(True)

    def closewindow(self, event):
        self.Destroy()

class MyDialog(wx.Dialog):
    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(270, 230))
        wx.StaticBox(self, -1, 'Choose disks', (5, 5), size=(240, 170))
        wx.StaticText(self, -1,'Your PC disk', (15, 30))
        self.ld = wx.TextCtrl(self, -1, 'D', (125, 30), (15, -1))
        wx.StaticText(self, -1, 'Will be mapped as', (15, 95))
        self.rd = wx.TextCtrl(self, -1, 'Y', (125, 95), (15, -1))
        #Buttons OK and Cancel
        self.ok = wx.Button(self, wx.ID_OK, 'Ok', pos=(15, 150), size=(90, -1))
        self.cancel = wx.Button(self, 1, 'Cancel', pos=(155, 150), size=(90, -1))
        self.Bind(wx.EVT_BUTTON, self.onClose, self.cancel)
        self.Bind(wx.EVT_BUTTON, self.onOk, self.ok)
        self.Centre()
        self.ShowModal()

    def onClose(self, event):
        self.Close()

    def onOk(self, event):
        self.localdisk = str(self.ld.GetValue())
        self.remdisk = str(self.rd.GetValue()) + ':'
        nu = NetUse(self.localdisk,  self.remdisk)
        nu.map()
        #self.Close()

class LogCollecter(object):


    def __init__(self, input_path, output_path, disk, remote_disk):
        self.input_path = input_path
        self.disk = disk
        self.remote_disk = remote_disk + ':'
        self.output_path = remote_disk[0]+output_path[1:]

    def relog(self):
        #Open directory
        result = []
        paths = os.listdir(self.input_path)  # list of paths in that dir
        for folder in paths:
            if os.path.isdir(os.path.join(self.input_path, folder)) == True:
                result.append(os.path.abspath(os.path.join(self.input_path, folder)))
            print 'founded folder', folder
        result.sort()
        if len(result) == 0:
            print 'There are no directories in %s' % self.input_path
            return False
        file_names = os.listdir(result[-1])
        print 'All files in last directory  ->', file_names
        true_names = filter(lambda name: name.endswith('.blg'), file_names)
        true_names.sort()
        print 'Sorted .blg files: ->', true_names
        if len(true_names) == 0:
            print 'There are no *.blg file in last directory %s' % result[-1]
            return False
        blg = os.path.abspath(os.path.join(result[-1], true_names[-1]))
        #for RDC : net use 'remote_disk_letter' \\tsclient\'your disk letter'
        nu = NetUse(self.disk,self.remote_disk)
        if not nu.ismapped():
            nu.map()
        #Relog command
        self.output_path += os.path.splitext(os.path.basename(blg))[0] + '.csv'
        args = "relog %s -f csv -o %s" % (blg, self.output_path)
        if (os.path.isfile(blg) and nu.ismapped()):
            print "Will be executed next command:", args
            cmd = "relog %s -f csv -o %s -y" %(blg,self.output_path)
            print "Command ' %s ' will be executed" % cmd
            try:
                subprocess.check_output(["relog", blg, '-f', 'csv', '-o', self.output_path, '-y'],
                                        stderr=subprocess.STDOUT, shell=False)
            except subprocess.CalledProcessError, e:
                print 'Relog failed!\n', e.output
            else:
                print "Converted log file is in  directory %s" %self.output_path
        else:
            print 'Path not found. Relog stopped.'
        # Unmap used disk
        if nu.ismapped():
            nu.unmap()

class NetUse(object):

    def __init__(self, locdisk, remdisk):
        self.locdisk = locdisk
        self.remdisk = remdisk

    def ismapped(self):
        if os.path.exists(str(self.remdisk)):
            return True
        else:
            return False

    def map(self):
        arg1 = str(self.remdisk)
        arg2 = '\\\\tsclient\\' + str(self.locdisk)
        print arg1, arg2
        cmd = "net use %s %s"  %(arg1, arg2)
        print "Command ' %s ' will be executed" % cmd
        try:
            subprocess.check_output(["net", "use", arg1, arg2],  stderr=subprocess.STDOUT, shell=False)
        except subprocess.CalledProcessError, e:
            print 'Net used failed!\n', e.output
        else:
            print "Disk %s was mapped as %s" %(arg2, arg1)

    def unmap(self):
        cmd = "net use %s /delete"  %(self.remdisk)
        print "Command ' %s ' will be executed" %(cmd)
        try:
            subprocess.check_output(["net", "use", self.remdisk, '/delete'],  stderr=subprocess.STDOUT, shell=False)
        except subprocess.CalledProcessError, e:
            print 'Net used failed!\n', e.output
        else:
            print "Disk %s was deleted" %(self.remdisk)

lc = wx.App()
frame = MainFrame(parent=None, id=-1)
frame.Show()
lc.MainLoop()
