import wx
import requests
import time
import re
import os

class inputPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        url_text = wx.StaticText(self, wx.ID_ANY, u'URL', style=wx.TE_CENTER)
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        url_text.SetFont(font)
        self.SetBackgroundColour('#afeeee')
        self.url_input = wx.TextCtrl(self, wx.ID_ANY, size=(300, 30))
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        self.url_input.SetFont(font)
        button = wx.Button(self, wx.ID_ANY, u'CHECK')
        button.Bind(wx.EVT_BUTTON, self.buttonEvent)
        layout2 = wx.BoxSizer(wx.HORIZONTAL)
        layout2.Add(self.url_input, flag=wx.EXPAND | wx.ALL, border=10)
        layout2.Add(button, flag=wx.EXPAND | wx.ALL, border=10)
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(url_text, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=15)
        layout.Add(layout2, flag=wx.EXPAND | wx.ALL, border=15)
        self.SetSizer(layout)

    def buttonEvent(self, event):
        url = self.url_input.GetValue()
        pp = self.respanel
        pp.addText(url)
        return True


class PrintPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY)
        res_text = wx.StaticText(self, wx.ID_ANY, u'\u8abf\u67fb\u7d50\u679c', style=wx.TE_CENTER)
        font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        res_text.SetFont(font)
        self.layout = wx.BoxSizer(wx.VERTICAL)
        self.layout.Add(res_text, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizer(self.layout)


class ResPanel(wx.Panel):

    def __init__(self, parent):
        wx.Panel.__init__(self, parent, wx.ID_ANY, size=(500, 500))
        self.layout = wx.BoxSizer(wx.VERTICAL)
        text = wx.StaticText(self, wx.ID_ANY, u'\u3053\u3053\u306b\u7d50\u679c\u304c\u8868\u793a\u3055\u308c\u307e\u3059', style=wx.TE_CENTER)
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        text.SetFont(font)
        self.layout.Add(text, flag=wx.EXPAND | wx.ALL, border=10)
        self.SetSizer(self.layout)

    def addText(self, url):
        self.clear(True)
        text = wx.StaticText(self, wx.ID_ANY, u'\u8abf\u67fb\u4e2d\u3000', style=wx.TE_CENTER)
        font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
        text.SetFont(font)
        self.layout.Add(text, flag=wx.GROW)
        self.layout.Layout()
        self.SetSizer(self.layout)
        functions = Functions()
        count = 0
        if not functions.validateURL(url):
            self.clear(True)
            text = wx.StaticText(self, wx.ID_ANY, u'\u3084\u308a\u76f4\u3057\u3066\u304f\u3060\u3055\u3044', style=wx.TE_CENTER)
            font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            text.SetFont(font)
            self.layout.Add(text, flag=wx.GROW)
            self.layout.Layout()
            self.SetSizer(self.layout)
            return
        try:
            res = functions.urlCheck(url)
        except:
            self.clear(True)
            text = wx.StaticText(self, wx.ID_ANY, u'\u3084\u308a\u76f4\u3057\u3066\u304f\u3060\u3055\u3044', style=wx.TE_CENTER)
            font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            text.SetFont(font)
            self.layout.Add(text, flag=wx.GROW)
            self.layout.Layout()
            self.SetSizer(self.layout)
            functions.showDialog(u'\u30a8\u30e9\u30fc', u'\u30a8\u30e9\u30fc\u304c\u767a\u751f\u3057\u307e\u3057\u305f\u3002\n\n\u30a6\u30a7\u30d6\u30b5\u30a4\u30c8\u304c\u898b\u3064\u304b\u308a\u307e\u305b\u3093\u3002')
            return False

        if res.status_code != 200:
            self.clear(True)
            text = wx.StaticText(self, wx.ID_ANY, u'\u3084\u308a\u76f4\u3057\u3066\u304f\u3060\u3055\u3044', style=wx.TE_CENTER)
            font = wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            text.SetFont(font)
            self.layout.Add(text, flag=wx.GROW)
            self.layout.Layout()
            self.SetSizer(self.layout)
            functions.showDialog(u'\u30a8\u30e9\u30fc', u'\u30a8\u30e9\u30fc\u304c\u767a\u751f\u3057\u307e\u3057\u305f\u3002\n\nHTTP\u30b9\u30c6\u30fc\u30bf\u30b9\u30b3\u30fc\u30c9\uff1a' + unicode(res.status_code))
            return False
        for res in functions.RedirectChk(res):
            if count == 0:
                self.clear(True)
            text = wx.StaticText(self, wx.ID_ANY, res)
            font = wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL)
            text.SetFont(font)
            self.layout.Add(text, flag=wx.EXPAND | wx.TOP | wx.LEFT | wx.RIGHT, border=5)
            self.layout.Layout()
            count = 1

        self.SetSizer(self.layout)

    def clear(self, event):
        self.layout.Clear(True)


class Functions(object):

    def __init__(self):
        self.urlRe = re.compile('^http(s)?://([\\w-]+\\.)+[\\w-]+')

    def RedirectChk(self, res):
        count = 0
        for his in res.history:
            count = count + 1
            yield str(count) + ':   ' + his.url

        yield str(count + 1) + ':   ' + res.url

    def urlCheck(self, url):
        return requests.get(url, allow_redirects=True, verify=False)

    def validateURL(self, url):
        if not self.urlRe.match(url):
            self.showDialog(u'\u30a8\u30e9\u30fc', u'URL\u4e0d\u6b63\n\n\uff08\u65e5\u672c\u8a9eURL\u306b\u306f\u5bfe\u5fdc\u3057\u3066\u3044\u307e\u305b\u3093\u3002\uff09')
            return False
        return True

    def showDialog(self, title, msg):
        box = wx.MessageDialog(None, unicode(msg), unicode(title), wx.OK)
        return box.ShowModal()


class MainApp(wx.App):

    def OnInit(self):
        self.init_frame()
        return True

    def init_frame(self):
        self.frm_main = wx.Frame(None)
        self.frm_main.SetTitle('Redirect Checker')
        self.frm_main.SetSize((500, 500))
        path = '.\\img\\top.ico'
        icon = wx.Icon(path, wx.BITMAP_TYPE_ICO)
        self.frm_main.SetIcon(icon)
        inputpanel = inputPanel(self.frm_main)
        printpanel = PrintPanel(self.frm_main)
        respanel = ResPanel(self.frm_main)
        inputpanel.respanel = respanel
        layout = wx.BoxSizer(wx.VERTICAL)
        layout.Add(inputpanel, flag=wx.GROW)
        layout.Add(printpanel, flag=wx.GROW)
        layout.Add(respanel, flag=wx.GROW)
        self.frm_main.SetSizer(layout)
        self.frm_main.Show()
        return


if __name__ == '__main__':
    app = MainApp()
    app.MainLoop()