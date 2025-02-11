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
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"KCD PAK Builder"), pos = wx.DefaultPosition, size = wx.Size( 600,500 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer61 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel3 = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        bSizer4 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"PAK Output Directory"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1.Wrap( -1 )

        bSizer4.Add( self.m_staticText1, 3, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.dp_pak_out_dir = wx.DirPickerCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, _(u"Select .pak Output Directory"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST )
        self.dp_pak_out_dir.SetToolTip( _(u"The Directory that your .pak file will be saved to") )

        bSizer4.Add( self.dp_pak_out_dir, 7, wx.ALL, 5 )


        bSizer8.Add( bSizer4, 0, wx.EXPAND, 5 )

        bSizer41 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText11 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"PAK Filename"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )

        bSizer41.Add( self.m_staticText11, 3, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.text_pak_filename = wx.TextCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_pak_filename.SetToolTip( _(u"The .pak filename to use.\nNote: The .pak extension is optional and will be added if not specified") )

        bSizer41.Add( self.text_pak_filename, 7, wx.ALL, 5 )


        bSizer8.Add( bSizer41, 0, wx.EXPAND, 5 )

        bSizer5 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText2 = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Directory To Pack"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText2.Wrap( -1 )

        bSizer5.Add( self.m_staticText2, 3, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.dp_target_dir = wx.DirPickerCtrl( self.m_panel3, wx.ID_ANY, wx.EmptyString, _(u"Select Target Directory"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST )
        self.dp_target_dir.SetToolTip( _(u"The path of the directory to pack") )

        bSizer5.Add( self.dp_target_dir, 7, wx.ALL, 5 )


        bSizer8.Add( bSizer5, 0, wx.EXPAND, 5 )

        bSizer81 = wx.BoxSizer( wx.HORIZONTAL )


        bSizer81.Add( ( 0, 0), 1, wx.EXPAND, 5 )


        bSizer8.Add( bSizer81, 0, wx.EXPAND, 5 )

        self.btn_toggle_options = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Show Additional Options"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_toggle_options.SetToolTip( _(u"Show/Hide Additional options") )

        bSizer8.Add( self.btn_toggle_options, 0, wx.ALL|wx.EXPAND, 5 )

        self.panel_options = wx.Panel( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_THEME|wx.TAB_TRAVERSAL )
        bSizer16 = wx.BoxSizer( wx.VERTICAL )

        bSizer12 = wx.BoxSizer( wx.HORIZONTAL )

        self.cb_save_output_dir = wx.CheckBox( self.panel_options, wx.ID_ANY, _(u"Remember Output Path"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cb_save_output_dir.SetValue(True)
        self.cb_save_output_dir.SetToolTip( _(u"Save/Remember the PAK Output Directory") )

        bSizer12.Add( self.cb_save_output_dir, 0, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.cb_save_filename = wx.CheckBox( self.panel_options, wx.ID_ANY, _(u"Remember Filename"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cb_save_filename.SetValue(True)
        self.cb_save_filename.SetToolTip( _(u"Save/Remember the PAK Filename") )

        bSizer12.Add( self.cb_save_filename, 0, wx.ALL, 5 )

        self.cb_save_target_dir = wx.CheckBox( self.panel_options, wx.ID_ANY, _(u"Remember Target Directory"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cb_save_target_dir.SetValue(True)
        self.cb_save_target_dir.SetToolTip( _(u"Save/Remember the Target Directory") )

        bSizer12.Add( self.cb_save_target_dir, 0, wx.ALL, 5 )


        bSizer16.Add( bSizer12, 0, wx.EXPAND, 5 )

        bSizer13 = wx.BoxSizer( wx.VERTICAL )

        self.cb_ignore_nested_paks = wx.CheckBox( self.panel_options, wx.ID_ANY, _(u"Skip .pak files"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.cb_ignore_nested_paks.SetValue(True)
        self.cb_ignore_nested_paks.SetToolTip( _(u"Skip and do not pack any .pak files that are found in the Target Directory (recommended)") )

        bSizer13.Add( self.cb_ignore_nested_paks, 0, wx.ALL, 5 )


        bSizer16.Add( bSizer13, 0, wx.EXPAND, 5 )


        self.panel_options.SetSizer( bSizer16 )
        self.panel_options.Layout()
        bSizer16.Fit( self.panel_options )
        bSizer8.Add( self.panel_options, 0, wx.EXPAND |wx.ALL, 5 )

        bSizer6 = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_start_pak = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Build PAK"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_start_pak.SetToolTip( _(u"Builds the .pak file") )

        bSizer6.Add( self.btn_start_pak, 1, wx.ALL, 5 )

        self.btn_stop_pak = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Cancel"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_stop_pak.Enable( False )
        self.btn_stop_pak.SetToolTip( _(u"Cancel the Build") )

        bSizer6.Add( self.btn_stop_pak, 1, wx.ALL, 5 )


        bSizer8.Add( bSizer6, 0, wx.EXPAND, 5 )

        bs_status = wx.BoxSizer( wx.HORIZONTAL )

        self.label_status = wx.StaticText( self.m_panel3, wx.ID_ANY, _(u"Waiting..."), wx.DefaultPosition, wx.DefaultSize, wx.ALIGN_CENTER_HORIZONTAL )
        self.label_status.Wrap( -1 )

        bs_status.Add( self.label_status, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer8.Add( bs_status, 0, wx.EXPAND, 5 )

        self.pak_pg_bar = wx.Gauge( self.m_panel3, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.pak_pg_bar.SetValue( 0 )
        bSizer8.Add( self.pak_pg_bar, 0, wx.ALL|wx.EXPAND, 5 )

        sbSizer1 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, _(u"Log") ), wx.VERTICAL )

        self.output_log = wx.TextCtrl( sbSizer1.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_DONTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
        self.output_log.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNFACE ) )
        self.output_log.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )

        sbSizer1.Add( self.output_log, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer8.Add( sbSizer1, 1, wx.EXPAND, 5 )


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


