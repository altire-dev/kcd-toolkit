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
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"KCD Asset Finder"), pos = wx.DefaultPosition, size = wx.Size( 600,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.MainPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer17 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel3 = wx.Panel( self.MainPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer61 = wx.BoxSizer( wx.VERTICAL )

        bSizer611 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText71 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Search"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText71.Wrap( -1 )

        bSizer611.Add( self.m_staticText71, 3, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.text_search = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer611.Add( self.text_search, 7, wx.ALL, 5 )


        bSizer61.Add( bSizer611, 0, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText7 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Asset Type"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        bSizer15.Add( self.m_staticText7, 3, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        choice_asset_typeChoices = [ _(u"Any"), _(u"Texture"), _(u"Material") ]
        self.choice_asset_type = wx.Choice( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_asset_typeChoices, 0 )
        self.choice_asset_type.SetSelection( 0 )
        bSizer15.Add( self.choice_asset_type, 7, wx.ALL, 5 )


        bSizer61.Add( bSizer15, 0, wx.EXPAND, 5 )

        bSizer7 = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_search = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Search"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer7.Add( self.btn_search, 1, wx.ALL|wx.EXPAND, 5 )

        self.btn_cancel = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_cancel.Enable( False )

        bSizer7.Add( self.btn_cancel, 1, wx.ALL, 5 )


        bSizer61.Add( bSizer7, 0, wx.EXPAND, 5 )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, _(u"Status") ), wx.VERTICAL )

        bSizer8 = wx.BoxSizer( wx.HORIZONTAL )

        self.label_status = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Waiting..."), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label_status.Wrap( -1 )

        bSizer8.Add( self.label_status, 1, wx.ALL, 5 )

        self.label_percentage = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_RIGHT )
        self.label_percentage.Wrap( -1 )

        self.label_percentage.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer8.Add( self.label_percentage, 1, wx.ALL, 5 )


        sbSizer2.Add( bSizer8, 1, wx.EXPAND, 5 )

        self.pb_search = wx.Gauge( sbSizer2.GetStaticBox(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.pb_search.SetValue( 0 )
        sbSizer2.Add( self.pb_search, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer61.Add( sbSizer2, 0, wx.EXPAND, 5 )

        sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, _(u"Results") ), wx.VERTICAL )

        self.results_tree = wx.TreeCtrl( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE )
        sbSizer5.Add( self.results_tree, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer61.Add( sbSizer5, 1, wx.EXPAND, 5 )

        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_expand_all = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Expand All"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.btn_expand_all, 1, wx.ALL, 5 )

        self.btn_collapse_all = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Collapse All"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.btn_collapse_all, 1, wx.ALL, 5 )


        bSizer61.Add( bSizer9, 0, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_button1 = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Save Results"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_button1, 1, wx.ALL, 5 )

        self.m_button2 = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Export Selected"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer6.Add( self.m_button2, 1, wx.ALL, 5 )


        bSizer61.Add( bSizer6, 0, wx.EXPAND, 5 )


        self.m_panel3.SetSizer( bSizer61 )
        self.m_panel3.Layout()
        bSizer61.Fit( self.m_panel3 )
        bSizer17.Add( self.m_panel3, 1, wx.EXPAND |wx.ALL, 10 )


        self.MainPanel.SetSizer( bSizer17 )
        self.MainPanel.Layout()
        bSizer17.Fit( self.MainPanel )
        bSizer3.Add( self.MainPanel, 1, wx.EXPAND |wx.ALL, 0 )


        self.SetSizer( bSizer3 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


