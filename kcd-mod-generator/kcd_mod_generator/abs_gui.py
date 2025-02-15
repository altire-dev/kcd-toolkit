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
        wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = _(u"KCD Mod Generator"), pos = wx.DefaultPosition, size = wx.Size( 600,700 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )

        self.SetSizeHints( wx.DefaultSize, wx.DefaultSize )

        bSizer3 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel2 = wx.Panel( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer61 = wx.BoxSizer( wx.VERTICAL )

        self.m_panel3 = wx.Panel( self.m_panel2, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.TAB_TRAVERSAL )
        bSizer8 = wx.BoxSizer( wx.VERTICAL )

        sbSizer2 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, _(u"General") ), wx.VERTICAL )

        bSizer13 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText11112 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"KCD2 Path *"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11112.Wrap( -1 )

        bSizer13.Add( self.m_staticText11112, 3, wx.ALL, 5 )

        self.dp_kcd2_path = wx.DirPickerCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, _(u"Select KCD2 Installation Folder"), wx.DefaultPosition, wx.DefaultSize, wx.DIRP_DEFAULT_STYLE|wx.DIRP_DIR_MUST_EXIST )
        bSizer13.Add( self.dp_kcd2_path, 7, wx.ALL, 5 )


        sbSizer2.Add( bSizer13, 1, wx.EXPAND, 5 )

        bSizer4111 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText1111 = wx.StaticText( sbSizer2.GetStaticBox(), wx.ID_ANY, _(u"Author *"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText1111.Wrap( -1 )

        bSizer4111.Add( self.m_staticText1111, 3, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.text_mod_author = wx.TextCtrl( sbSizer2.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_mod_author.SetToolTip( _(u"Mod Author Name") )

        bSizer4111.Add( self.text_mod_author, 7, wx.ALL, 5 )


        sbSizer2.Add( bSizer4111, 0, wx.EXPAND, 5 )


        bSizer8.Add( sbSizer2, 0, wx.EXPAND, 5 )

        sbSizer3 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, _(u"Mod") ), wx.VERTICAL )

        bSizer41 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText11 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"ID *"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11.Wrap( -1 )

        bSizer41.Add( self.m_staticText11, 3, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.text_mod_id = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_mod_id.SetToolTip( _(u"The Mod's ID") )

        bSizer41.Add( self.text_mod_id, 7, wx.ALL, 5 )


        sbSizer3.Add( bSizer41, 0, wx.EXPAND, 5 )

        bSizer411 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText111 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Name *"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText111.Wrap( -1 )

        bSizer411.Add( self.m_staticText111, 3, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.text_mod_name = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_mod_name.SetToolTip( _(u"The Mod's name") )

        bSizer411.Add( self.text_mod_name, 7, wx.ALL, 5 )


        sbSizer3.Add( bSizer411, 0, wx.EXPAND, 5 )

        bSizer41111 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText11111 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Version *"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText11111.Wrap( -1 )

        bSizer41111.Add( self.m_staticText11111, 3, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.text_mod_version = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"1.0.0"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_mod_version.SetToolTip( _(u"The Mod's version number") )

        bSizer41111.Add( self.text_mod_version, 7, wx.ALL, 5 )


        sbSizer3.Add( bSizer41111, 0, wx.EXPAND, 5 )

        bSizer411111 = wx.BoxSizer( wx.HORIZONTAL )

        self.m_staticText111111 = wx.StaticText( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Supported KCD2 Version"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.m_staticText111111.Wrap( -1 )

        bSizer411111.Add( self.m_staticText111111, 3, wx.ALIGN_CENTER|wx.ALL, 5 )

        self.text_kcd2_version = wx.TextCtrl( sbSizer3.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, 0 )
        self.text_kcd2_version.SetToolTip( _(u"The KCD2 version number that this Mod supports (optional)") )

        bSizer411111.Add( self.text_kcd2_version, 7, wx.ALL, 5 )


        sbSizer3.Add( bSizer411111, 0, wx.EXPAND, 5 )

        sbSizer4 = wx.StaticBoxSizer( wx.StaticBox( sbSizer3.GetStaticBox(), wx.ID_ANY, _(u"Description") ), wx.HORIZONTAL )

        self.text_mod_desc = wx.TextCtrl( sbSizer4.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_MULTILINE )
        self.text_mod_desc.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.text_mod_desc.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        self.text_mod_desc.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )
        self.text_mod_desc.SetToolTip( _(u"The Mod's description") )

        sbSizer4.Add( self.text_mod_desc, 1, wx.ALL|wx.EXPAND, 5 )


        sbSizer3.Add( sbSizer4, 1, wx.EXPAND, 5 )


        bSizer8.Add( sbSizer3, 2, wx.EXPAND, 5 )

        bSizer6 = wx.BoxSizer( wx.VERTICAL )

        self.pg_bar = wx.Gauge( self.m_panel3, wx.ID_ANY, 100, wx.DefaultPosition, wx.DefaultSize, wx.GA_HORIZONTAL )
        self.pg_bar.SetValue( 0 )
        bSizer6.Add( self.pg_bar, 0, wx.ALL|wx.EXPAND, 5 )

        bSizer11 = wx.BoxSizer( wx.HORIZONTAL )

        self.btn_generate_mod = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Generate Mod"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_generate_mod.SetToolTip( _(u"Initialise and sets up the Mod") )

        bSizer11.Add( self.btn_generate_mod, 1, wx.ALL|wx.EXPAND, 5 )

        self.btn_open_folder = wx.Button( self.m_panel3, wx.ID_ANY, _(u"Open Mod Folder"), wx.DefaultPosition, wx.DefaultSize, 0 )
        self.btn_open_folder.Enable( False )

        bSizer11.Add( self.btn_open_folder, 0, wx.ALL, 5 )


        bSizer6.Add( bSizer11, 1, wx.EXPAND, 5 )


        bSizer8.Add( bSizer6, 0, wx.EXPAND, 5 )

        self.m_staticline1 = wx.StaticLine( self.m_panel3, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LI_HORIZONTAL )
        bSizer8.Add( self.m_staticline1, 0, wx.EXPAND |wx.ALL, 5 )

        sbSizer41 = wx.StaticBoxSizer( wx.StaticBox( self.m_panel3, wx.ID_ANY, _(u"Output Log") ), wx.HORIZONTAL )

        self.text_output_log = wx.TextCtrl( sbSizer41.GetStaticBox(), wx.ID_ANY, wx.EmptyString, wx.DefaultPosition, wx.DefaultSize, wx.TE_DONTWRAP|wx.TE_MULTILINE|wx.TE_READONLY )
        self.text_output_log.SetFont( wx.Font( 11, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, False, wx.EmptyString ) )
        self.text_output_log.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_HIGHLIGHTTEXT ) )
        self.text_output_log.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_GRAYTEXT ) )

        sbSizer41.Add( self.text_output_log, 1, wx.ALL|wx.EXPAND, 5 )


        bSizer8.Add( sbSizer41, 1, wx.EXPAND, 5 )


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


