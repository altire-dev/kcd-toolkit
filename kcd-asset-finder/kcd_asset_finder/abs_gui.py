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
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"KCD Asset Finder"), pos = wx.DefaultPosition, size = wx.Size( 650,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.MainPanel = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer17 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel3 = wx.Panel( self.MainPanel, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer61 = wx.BoxSizer( wx.VERTICAL )

        self.Panel_KCD2Path = wx.Panel( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer6111 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText711 = wx.StaticText( self.Panel_KCD2Path, wx.ID_ANY, _(u"KCD2 Path *"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText711.Wrap( -1 )

        bSizer6111.Add( self.m_staticText711, 2, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.dp_kcd2_path = wx.DirPickerCtrl( self.Panel_KCD2Path, wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST )
        self.dp_kcd2_path.SetToolTip( _(u"Path to the KCD2 Installation") )

        bSizer6111.Add( self.dp_kcd2_path, 7, wx.ALL, 5 )


        self.Panel_KCD2Path.SetSizer( bSizer6111 )
        self.Panel_KCD2Path.Layout()
        bSizer6111.Fit( self.Panel_KCD2Path )
        bSizer61.Add( self.Panel_KCD2Path, 0, wx.EXPAND |wx.ALL, 0 )

        bSizer611 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText71 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Search"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText71.Wrap( -1 )

        bSizer611.Add( self.m_staticText71, 2, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        choice_search_typeChoices = [ _(u"Contains"), _(u"Does not Contain"), _(u"Regex") ]
        self.choice_search_type = wx.Choice( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_search_typeChoices, 0 )
        self.choice_search_type.SetSelection( 0 )
        bSizer611.Add( self.choice_search_type, 2, wx.ALL, 5 )

        self.text_search = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_PROCESS_ENTER )
        self.text_search.SetToolTip( _(u"Asset search string") )

        bSizer611.Add( self.text_search, 5, wx.ALL, 5 )


        bSizer61.Add( bSizer611, 0, wx.EXPAND, 5 )

        bSizer10 = wx.BoxSizer( wx.VERTICAL )


        bSizer61.Add( bSizer10, 1, wx.EXPAND, 5 )

        bSizer15 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText7 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Asset Type"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7.Wrap( -1 )

        bSizer15.Add( self.m_staticText7, 2, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        choice_asset_typeChoices = [ _(u"Any"), _(u"Texture"), _(u"Material"), _(u"Blend Space"), _(u"Geometry File (CGF)"), _(u"Skin"), _(u"XML"), _(u"Audio"), _(u"Flash Content"), _(u"Character Animations"), _(u"DBA") ]
        self.choice_asset_type = wx.Choice( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, choice_asset_typeChoices, 0 )
        self.choice_asset_type.SetSelection( 0 )
        self.choice_asset_type.SetToolTip( _(u"Asset type filter") )

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

        self.label_percentage = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.label_percentage.Wrap( -1 )

        self.label_percentage.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )

        bSizer8.Add( self.label_percentage, 0, wx.ALL, 5 )


        sbSizer2.Add( bSizer8, 1, wx.EXPAND, 5 )

        self.pb_search = wx.Gauge( sbSizer2.GetStaticBox(), wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.pb_search.SetValue( 0 )
        sbSizer2.Add( self.pb_search, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer61.Add( sbSizer2, 0, wx.EXPAND, 5 )

        sbSizer5 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, _(u"Results") ), wx.VERTICAL )

        self.tree_widget = wx.TreeCtrl( sbSizer5.GetStaticBox(), wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TR_DEFAULT_STYLE|wx.TR_MULTIPLE )
        sbSizer5.Add( self.tree_widget, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer61.Add( sbSizer5, 1, wx.EXPAND, 5 )

        bSizer9 = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_expand_all = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Expand All"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.btn_expand_all, 1, wx.ALL, 5 )

        self.btn_collapse_all = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Collapse All"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer9.Add( self.btn_collapse_all, 1, wx.ALL, 5 )


        bSizer61.Add( bSizer9, 0, wx.EXPAND, 5 )

        self.Panel_Export = wx.Panel( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.Panel_Export, wx.ID_ANY, _(u"Asset Export") ), wx.VERTICAL )

        bSizer16 = wx.BoxSizer( wx.VERTICAL )

        bSizer19 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText7111 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Export Path"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText7111.Wrap( -1 )

        bSizer19.Add( self.m_staticText7111, 3, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.dp_export_path = wx.DirPickerCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, _(u"Select a folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST )
        self.dp_export_path.Enable( False )
        self.dp_export_path.SetToolTip( _(u"Asset export destination folder") )

        bSizer19.Add( self.dp_export_path, 7, wx.ALL, 5 )


        bSizer16.Add( bSizer19, 1, wx.EXPAND, 5 )

        bSizer18 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText71111 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Preserve Asset Paths"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText71111.Wrap( -1 )

        bSizer18.Add( self.m_staticText71111, 3, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )

        self.checkbox_preserve_paths = wx.CheckBox( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.checkbox_preserve_paths.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.checkbox_preserve_paths.Enable( False )
        self.checkbox_preserve_paths.SetToolTip( _(u"Preserves and creates the folder structure of extracted assets in the export destination") )

        bSizer18.Add( self.checkbox_preserve_paths, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5 )


        bSizer16.Add( bSizer18, 1, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_export = wx.Button( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Export Selected"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_export.Enable( False )

        bSizer6.Add( self.btn_export, 1, wx.ALL, 5 )


        bSizer16.Add( bSizer6, 1, wx.EXPAND, 5 )


        sbSizer3.Add( bSizer16, 1, wx.EXPAND, 5 )


        self.Panel_Export.SetSizer( sbSizer3 )
        self.Panel_Export.Layout()
        sbSizer3.Fit( self.Panel_Export )
        bSizer61.Add( self.Panel_Export, 0, wx.EXPAND |wx.ALL, 5 )


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


###########################################################################
## Class MessageDialog
###########################################################################

class MessageDialog ( wx.Dialog ):

    def __init__( self, parent ):
        wx.Dialog.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"Info"), pos = wx.DefaultPosition, size = wx.Size( 300,150 ), style = wx.DEFAULT_DIALOG_STYLE )

        self.SetSizeHints( wx.Size( 300,150 ), wx.DefaultSize )

        bSizer25 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel5 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer26 = wx.BoxSizer( wx.VERTICAL )

        bSizer27 = wx.BoxSizer( wx.VERTICAL )

        self.dialog_text = wx.StaticText( self.m_panel5, wx.ID_ANY, _(u"This is the Dialog Message"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.dialog_text.Wrap( -1 )

        bSizer27.Add( self.dialog_text, 1, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        bSizer26.Add( bSizer27, 1, wx.EXPAND, 5 )

        bSizer28 = wx.BoxSizer( wx.VERTICAL )

        self.btn_ok = wx.Button( self.m_panel5, wx.ID_ANY, _(u"OK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        bSizer28.Add( self.btn_ok, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )


        bSizer26.Add( bSizer28, 0, wx.EXPAND, 5 )


        self.m_panel5.SetSizer( bSizer26 )
        self.m_panel5.Layout()
        bSizer26.Fit( self.m_panel5 )
        bSizer25.Add( self.m_panel5, 1, wx.EXPAND |wx.ALL, 10 )


        self.SetSizer( bSizer25 )
        self.Layout()

        self.Centre( wx.BOTH )

    def __del__( self ):
        pass


