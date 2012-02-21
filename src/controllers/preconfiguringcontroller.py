import os
import wx
from src.modules.settings import config, setandgetsettings
from src.gui.preconfiguringframe import PreconfiguringFrame

class PreconfiguringController:

    def __init__(self):

        self.view = PreconfiguringFrame()
        listChoices = []
        for k, v in config.langForTran.iteritems():
            listChoices.append(v)
        listChoices.sort()
        self.view.p_listBoxComTran.Set(listChoices)
        self.view.p_listBoxNatLang.Set(listChoices)



        # Connect Events
        self.view.Bind( wx.wizard.EVT_WIZARD_CANCEL, self.event_wizard_cancel )
        self.view.Bind( wx.wizard.EVT_WIZARD_FINISHED, self.event_wizard_finished )

        self.view.p_sliderSizeText.Bind( wx.EVT_SCROLL, self.eventSlider )

        self.view.p_textCtrlAddress.Bind( wx.EVT_KILL_FOCUS, self.eventKillFokus )
        self.view.p_textCtrlAddress.Bind( wx.EVT_SET_FOCUS, self.eventSetFokus )
        self.view.p_textCtrlPort.Bind( wx.EVT_KILL_FOCUS, self.eventKillFokus )
        self.view.p_textCtrlPort.Bind( wx.EVT_SET_FOCUS, self.eventSetFokus )
        self.view.p_textCtrlLogin.Bind( wx.EVT_KILL_FOCUS, self.eventKillFokus )
        self.view.p_textCtrlLogin.Bind( wx.EVT_SET_FOCUS, self.eventSetFokus )
        self.view.p_textCtrlPass.Bind( wx.EVT_KILL_FOCUS, self.eventKillFokus )
        self.view.p_textCtrlPass.Bind( wx.EVT_SET_FOCUS, self.eventSetFokus )

        self.view.RunWizard(self.view.p_wizPageNatLang)


    def eventKillFokus( self, event ):
        if event.EventObject.Value == "":
            event.EventObject.Name="0"+event.EventObject.Name[1:]
            event.EventObject.ForegroundColour= wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT )
            event.EventObject.Value=event.EventObject.Name[1:]
        else:
            event.EventObject.Name="1"+event.EventObject.Name[1:]
        event.Skip()


    def eventSetFokus( self, event ):
        if event.EventObject.Name[0]=="0":
            event.EventObject.Value=""
            event.EventObject.ForegroundColour= wx.SystemSettings.GetColour( wx.SYS_COLOUR_WINDOWTEXT )
        event.Skip()

    def eventSlider( self, event ):
        self.view.p_staticTextSizeText.SetFont( wx.Font( self.view.p_sliderSizeText.Value+8, wx.SWISS, wx.NORMAL,
            wx.NORMAL ) )
        event.Skip()

    def event_wizard_finished( self, event ):
        if not self.view.p_radioBtnGoogle:
            config.useGoogle=False
            config.useBing=True
        else :
            config.useGoogle=True
            config.useBing=False
        if self.view.p_listBoxComTran.GetSelection():
            config.langList=self.view.p_listBoxComTran.GetSelection()
        if self.view.p_listBoxNatLang.GetSelection():
            config.defaultLangTo=self.view.p_listBoxNatLang.GetSelection()
        config.translatedTextSize=self.view.p_sliderSizeText.Value+8
        if os.name =="nt" and self.view.p_textCtrlAddress.Value != "" or "Address":
            config.useProxy=True
            config.proxyAddress=self.view.p_textCtrlAddress.Value
            config.proxyPort=self.view.p_textCtrlPort.Value
            config.proxyLogin=self.view.p_textCtrlLogin.Value
            config.proxyPassword=self.view.p_textCtrlPass.Value
        self.view.Destroy()

    def event_wizard_cancel( self, event ):
        self.view.Destroy()