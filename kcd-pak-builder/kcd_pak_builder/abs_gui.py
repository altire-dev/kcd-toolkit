# -*- coding: utf-8 -*-

###########################################################################
## Python code generated with wxFormBuilder (version 4.2.1-0-g80c4cb6)
## http://www.wxformbuilder.org/
##
## PLEASE DO *NOT* EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

import gettext
_ = gettext.gettext

###########################################################################
## Class MainFrame
###########################################################################

class MainFrame ( wx.Frame ):

    def __init__( self, parent ):
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = wx.EmptyString, pos = wx.DefaultPosition, size = wx.Size( 500,300 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer61 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel3 = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"PAK Output Path"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        bSizer4.Add( self.m_staticText1, 3, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.fp_pak_out_path = wx.FilePickerCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, _(u"Select a file"), _(u".pak"), wx.DefaultPosition, wx.DefaultSize, wx.FLP_OVERWRITE_PROMPT|wx.FLP_SAVE|wx.FLP_USE_TEXTCTRL )
        bSizer4.Add( self.fp_pak_out_path, 7, wx.ALL, 5 )


        bSizer8.Add( bSizer4, 0, wx.EXPAND, 5 )

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText2 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Directory To Pack"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        bSizer5.Add( self.m_staticText2, 3, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.dp_target_dir = wx.DirPickerCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST )
        bSizer5.Add( self.dp_target_dir, 7, wx.ALL, 5 )


        bSizer8.Add( bSizer5, 0, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_start_pak = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Build PAK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.btn_start_pak, 1, wx.ALL, 5 )

        self.btn_stop_pak = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.btn_stop_pak, 1, wx.ALL, 5 )


        bSizer8.Add( bSizer6, 0, wx.EXPAND, 5 )

        bs_status = wx.BoxSizer( wx.HORIZONTAL )

        self.label_status = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"WAITING..."), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label_status.Wrap( -1 )

        bs_status.Add( self.label_status, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer8.Add( bs_status, 0, wx.EXPAND, 5 )

        self.pak_pg_bar = wx.Gauge( self.m_panel3, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.pak_pg_bar.SetValue( 0 )
        bSizer8.Add( self.pak_pg_bar, 0, wx.ALL|wx.EXPAND, 5 )

        self.m_textCtrl2 = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE|wx.TE_READONLY )
        bSizer8.Add( self.m_textCtrl2, 0, wx.ALL|wx.EXPAND, 5 )


        self.m_panel3.SetSizer( bSizer8 )
        self.m_panel3.Layout()
        bSizer8.Fit( self.m_panel3 )
        bSizer61.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 5 )


        self.m_panel2.SetSizer( bSizer61 )
        self.m_panel2.Layout()
        bSizer61.Fit( self.m_panel2 )
        bSizer3.Add( self.m_panel2, 1, wx.EXPAND |wx.ALL, 0 )


        self.SetSizer( bSizer3 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


