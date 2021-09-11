# -*- coding: utf-8 -*-
import urllib.request,wx



def av_or_bv(inp):
    
    # 将参数去除
    if inp.find('?') == -1:
        pass
    else:
        inp = inp[:inp.find('?')]

    # 转换不带av和BV的视频地址
    if inp.find('av') == -1 and inp.find('BV') == -1:
        try:
            b = int(inp)
            return 'aid='+str(b)
        except ValueError:
            return 'bvid='+inp

    # 转换带av和BV的视频地址
    elif inp.find('BV') == -1:
        return 'aid='+inp[inp.find('av')+2:]

    elif inp.find('av') == -1:
        return 'bvid='+inp[inp.find('BV')+2:]



def bilibili(video_name,file):

    # 开始请求
    url = av_or_bv(video_name)
    url = 'https://api.bilibili.com/x/web-interface/view?'+url
    req = urllib.request.Request(url)

    global end

    try:
        with urllib.request.urlopen(req) as response:
            data = response.read()
            json_data = data.decode()

            if json_data.find('"message":"0"') != -1:
                # 请求成功，获得数据
                global videoname
                # 解析视频标题
                videoname = json_data[(json_data.find('title')+8):(json_data.find('pubdate')-3)]
                # 解析视频封面
                pic = json_data[(json_data.find('pic')+6):(json_data.find('title')-3)]

                with urllib.request.urlopen(pic) as response_pic:
                    data_pic = response_pic.read()

                    # 写入图片数据
                    if file == '':
                        file = 'D:\\bilibilidownload\\'+videoname+'.png'
                        with open(file,'wb') as f:
                            f.write(data_pic)
                            end = 0
                    else:
                        try:
                            with open(file,'wb') as f:
                                f.write(data_pic)
                                end = 0

                        except FileNotFoundError:
                            file = file+videoname+'.png'
                            with open(file,'wb') as f:
                                f.write(data_pic)
                                end = 0
            else:
                # 请求失败
                end = 1
    except UnicodeEncodeError:
        end = 2



class getbilibili(wx.Frame):
    def __init__(self):
        # 界面布局
        super().__init__(None,title = '哔哩哔哩视频封面下载器',size = (600,250))
        panel = wx.Panel(parent = self)

        self.statictext = wx.StaticText(parent = panel,label = '点击下方按钮开始下载')
        button = wx.Button(parent = panel,label = '开始下载')
        self.Bind(wx.EVT_BUTTON,self.on_click,button)

        global enter1,enter2
        enter1 = wx.TextCtrl(panel)
        enter2 = wx.TextCtrl(panel)

        v = wx.StaticText(panel,label = '输入哔哩哔哩视频地址：')
        location = wx.StaticText(panel,label = '输入封面保存的地址：')

        vbox = wx.BoxSizer(wx.VERTICAL)

        vbox. Add(v,flag = wx.EXPAND|wx.LEFT,border = 10)
        vbox. Add(enter1,flag = wx.EXPAND|wx.ALL,border = 10)

        vbox. Add(location,flag = wx.EXPAND|wx.LEFT,border = 10)
        vbox. Add(enter2,flag = wx.EXPAND|wx.ALL,border = 10)

        vbox.Add(self.statictext,proportion = 100,flag = wx.ALIGN_CENTER_HORIZONTAL|wx.FIXED_MINSIZE|wx.TOP,border = 10)
        vbox.Add(button,proportion = 1,flag = wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM,border = 10)

        panel.SetSizer(vbox)

        enter2.SetValue('D:\\bilibilidownload\\')

    def on_click(self,event):
        # 下载按钮
        if enter1.GetValue() == '':
            self.statictext.SetLabelText('请输入视频地址哦')
        else:
            bilibili(enter1.GetValue(),enter2.GetValue())
            if end == 0:
                self.statictext.SetLabelText('下载成功啦！')
            elif end == 1:
                self.statictext.SetLabelText('请求错误了哦，检查一下视频地址正确了吗')
            elif end == 2:
                self.statictext.SetLabelText('请不要输入中文哦')
            else:
                self.statictext.SetLabelText('出大问题啦')



app = wx.App()
bilibiliwindows = getbilibili()
bilibiliwindows.Show()
app.MainLoop()
