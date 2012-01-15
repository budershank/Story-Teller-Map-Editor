import  wx
import  wx.grid             as  gridlib
import os

#----------------------------------------------------------------------
ID_New  = wx.NewId()
ID_Save = wx.NewId()
ID_SaveAs = wx.NewId()
ID_Close = wx.NewId()
ID_Exit = wx.NewId()
ID_ShowGrid = wx.NewId()


#----------------------------------------------------------------------


class NameSizeDialog(wx.Dialog):
    def __init__(
            self, parent, ID, title, pos, size,
            style=wx.DEFAULT_DIALOG_STYLE,
            useMetal=False,
            ):

        #Precreate, required for creating custom dialog i guess
        pre = wx.PreDialog()
        pre.SetExtraStyle(wx.DIALOG_EX_CONTEXTHELP)
        pre.Create(parent, ID, title, pos, size, style)
        self.PostCreate(pre)



        #start building custom dialog
        sizer = wx.BoxSizer(wx.VERTICAL)

        labelHeader = wx.StaticText(self, -1, "Create New Map")
        sizer.Add(labelHeader, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        boxMapName = wx.BoxSizer(wx.HORIZONTAL)

        labelMapName = wx.StaticText(self, -1, "Map Name")
        boxMapName.Add(labelMapName, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        txtMapName = wx.TextCtrl(self, -1, "", size=(80,-1))
        self.txtMapName = txtMapName
        boxMapName.Add(txtMapName, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(boxMapName, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Tiles X:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        txtTilesX = wx.TextCtrl(self, -1, "", size=(80,-1))
        self.txtTilesX = txtTilesX
        txtTilesX.SetHelpText("Numbers Only")
        box.Add(txtTilesX, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        box = wx.BoxSizer(wx.HORIZONTAL)

        label = wx.StaticText(self, -1, "Tiles Y:")
        box.Add(label, 0, wx.ALIGN_CENTRE|wx.ALL, 5)

        txtTilesY = wx.TextCtrl(self, -1, "", size=(80,-1))
        self.txtTilesY = txtTilesY
        txtTilesY.SetHelpText("Numbers Only")
        box.Add(txtTilesY, 1, wx.ALIGN_CENTRE|wx.ALL, 5)

        sizer.Add(box, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)

        line = wx.StaticLine(self, -1, size=(20,-1), style=wx.LI_HORIZONTAL)
        sizer.Add(line, 0, wx.GROW|wx.ALIGN_CENTER_VERTICAL|wx.RIGHT|wx.TOP, 5)

        btnsizer = wx.StdDialogButtonSizer()
        
        if wx.Platform != "__WXMSW__":
            btn = wx.ContextHelpButton(self)
            btnsizer.AddButton(btn)
        
        btn = wx.Button(self, wx.ID_OK)
        
        btn.SetDefault()
        btnsizer.AddButton(btn)

        btn = wx.Button(self, wx.ID_CANCEL)
        
        btnsizer.AddButton(btn)
        btnsizer.Realize()

        sizer.Add(btnsizer, 0, wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)
        
        self.SetSizer(sizer)


#This is what allows you to put images into a cell
class MyImageRenderer(wx.grid.PyGridCellRenderer):
     def __init__(self, img):
          wx.grid.PyGridCellRenderer.__init__(self)
          self.img = img
          
         
     def Draw(self, grid, attr, dc, rect, row, col, isSelected):
          
          image = wx.MemoryDC()
          image.SelectObject(self.img)
          dc.SetBackgroundMode(wx.SOLID)
          dc.DrawRectangleRect(rect)
          width, height = 64, 64

          dc.Blit(rect.x, rect.y, width, height, image, 0, 0, wx.COPY, True, 0, 0)


class MapGrid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)



   
        self.moveTo = None

        
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.SetDefaultColSize(64)
        self.SetDefaultRowSize(64)
        self.CreateGrid(parent.tilesX, parent.tilesY)
        self.EnableDragColSize(False)
        self.EnableDragColMove(False)
        self.EnableDragGridSize(False)
        self.EnableDragRowSize(False)
        self.EnableEditing(False)
        self.EnableCellEditControl(False)

        #THis will set the background for all tiles on creation
        img = wx.Bitmap(tileSelected, wx.BITMAP_TYPE_PNG)
        defaultImageRenderer = MyImageRenderer(img)
        self.SetDefaultRenderer(defaultImageRenderer)

    def OnCellLeftClick(self, evt):
       

        img = wx.Bitmap(tileSelected, wx.BITMAP_TYPE_PNG)
        
        imageRenderer = MyImageRenderer(img)
        self.SetCellRenderer(evt.GetRow(), evt.GetCol(), imageRenderer)
        self.SetCellValue(evt.GetRow(), evt.GetCol(), tileID)
        self.ClearSelection()
        self.ForceRefresh()
        evt.Skip()

class TileGrid(gridlib.Grid): ##, mixins.GridAutoEditMixin):
    def __init__(self, parent):
        gridlib.Grid.__init__(self, parent, -1)
        
        
        self.moveTo = None

        
        self.Bind(gridlib.EVT_GRID_CELL_LEFT_CLICK, self.OnCellLeftClick)
        self.Bind(gridlib.EVT_GRID_SELECT_CELL, self.OnSelectChange)
        self.SetDefaultColSize(64)
        self.SetDefaultRowSize(64)
        
        self.SetColLabelSize(0)
        self.SetRowLabelSize(0)
        self.CreateGrid(20, 2)
        self.SetColSize(1, 26)
        self.EnableDragColSize(False)
        self.EnableDragColMove(False)
        self.EnableDragGridSize(False)
        self.EnableDragRowSize(False)
        self.EnableEditing(False)
        self.EnableCellEditControl(False)
        self.SetSelectionMode(wx.grid.Grid.wxGridSelectRows )
        print self.GetSelectionMode()
        self.SetSelectionBackground(wx.BLACK)
        self.SetDefaultCellFont(wx.Font(16, wx.SWISS, wx.NORMAL, wx.BOLD))
        self.SelectRow(0)
        
        #Load images, this will need to be reworked to load from a source
        imgGrass = wx.Bitmap("grass.png", wx.BITMAP_TYPE_PNG)
        
        imageRenderer = MyImageRenderer(imgGrass)
        self.SetCellRenderer(0,0, imageRenderer)
        self.SetCellValue(0,1, "G")
        self.SetCellValue(0,0, "grass.png")
        
        imgWater = wx.Bitmap("water.png", wx.BITMAP_TYPE_PNG)
        imageRenderer = MyImageRenderer(imgWater)
        self.SetCellRenderer(1,0, imageRenderer)
        self.SetCellValue(1,1, "W")
        self.SetCellValue(1,0, "water.png")

        imgDirt = wx.Bitmap("dirt.png", wx.BITMAP_TYPE_PNG)
        imageRenderer = MyImageRenderer(imgDirt)
        self.SetCellRenderer(2,0, imageRenderer)
        self.SetCellValue(2,1, "D")
        self.SetCellValue(2,0, "dirt.png")


        self.ForceRefresh()
        global tileSelected
        tileSelected = self.GetCellValue(0, 0)
        global tileID
        tileID= self.GetCellValue(1, 1)
        
    def OnSelectChange(self, evt):
        global tileSelected
        tileSelected = self.GetCellValue(evt.GetRow(), 0)
        global tileID
        tileID= self.GetCellValue(evt.GetRow(), 1)
        print tileSelected
        

    def OnCellLeftClick(self, evt):
        

        #img = wx.Bitmap("smiles.png", wx.BITMAP_TYPE_PNG)
        
        #imageRenderer = MyImageRenderer(img)
        #self.SetCellRenderer(evt.GetRow(), evt.GetCol(), imageRenderer)
       # self.ClearSelection()
       # self.ForceRefresh() 
        evt.Skip()



class TileWindow(wx.MDIChildFrame):
    def __init__(self, parent):
        print "bah"
                

#This is the first window to load
class MyParentFrame(wx.MDIParentFrame):
    def __init__(self):
        wx.MDIParentFrame.__init__(self, None, -1, "Storyteller Map Maker", size=(600,600))
         #not used by me.
        self.winCount = 0

        #Create the menu
        menu = wx.Menu()
        menu.Append(ID_New, "&New Map")        
        menu.AppendSeparator()
        menu.Append(ID_Exit, "E&xit")
        menubar = wx.MenuBar()
        menubar.Append(menu, "&File")        
        self.SetMenuBar(menubar)

        #Status Bar(not used yet)
        self.CreateStatusBar()

        
        self.Bind(wx.EVT_MENU, self.OnNewWindow, id=ID_New)
        self.Bind(wx.EVT_MENU, self.OnExit, id=ID_Exit)

        self.Maximize()


        #Make tile window
        myTup =self.GetClientSize()
        winTools = wx.MDIChildFrame(self)
       
       # winTools = wx.Window(-1)
        winTools.SetPosition(wx.Point(0,0))
        winTools.SetSize(wx.Size(90, myTup[1]))
        
        
      
        
        winTools.SetMaxSize(wx.Size(90, myTup[1] ))
       # winTools.Maximize()
        #self.SetDimensions(0, 0, 100, 600, sizeFlags = wx.ACCEL_ALTSIZE_AUTO)
        
        tileGrid = TileGrid(winTools)
      #  ToolWindow = TileWindow(winTools)
    

    
    def OnExit(self, evt):
        self.Close(True)


    def OnNewWindow(self, evt): 
        self.TilesX = 1
        self.TilesY = 1
        self.MapName = "Map"
        dlg = NameSizeDialog(self, -1, "Create Map",  pos = (-1, -1), size =(220, 220),
                              style = wx.DEFAULT_DIALOG_STYLE,useMetal=False,)
        val =dlg.ShowModal()
        if val == wx.ID_OK:
            myTup =self.GetClientSize()
            win = wx.MDIChildFrame(self, -1, dlg.txtMapName.GetLineText(0))
            win.winCount = self.winCount + 1
            
            win.tilesX = int(dlg.txtTilesX.GetLineText(0))
            win.tilesY = int(dlg.txtTilesY.GetLineText(0))
            win.mapName = dlg.txtMapName.GetLineText(0)
    

        
            win.SetPosition(wx.Point(120, 0))
            win.SetSize(wx.Size(myTup[0]-200, myTup[1]-120))
            mapGrid = MapGrid(win)
        dlg.Destroy()

        

        
        #win.Show(True)




#----------------------------------------------------------------------

if __name__ == '__main__':
    class MyApp(wx.App):
        def OnInit(self):
            wx.InitAllImageHandlers()
            frame = MyParentFrame()
            frame.Show(True)
            self.SetTopWindow(frame)
            return True


    app = MyApp(False)
    app.MainLoop()



