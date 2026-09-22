from tkinter import Tk,Frame,Label,Event,messagebox,Button,filedialog
import random,os,csv

class Game_2048():

    last_spawnnode :list = [0,0]
    Win : bool = False
    Move_bool : bool = True
    Last_Grid = []
    __list_empty_node : list = []
    __debug : bool = False;
    check_key = {"w":True,"a":True,"s":True,"d":True}
    def __init__(self,MapSize:int,Target:int):
        os.system("cls")
        self.Window = Tk()
        self.Window.title("2048")
        self.GridFrame = Frame(self.Window)
        self.ButtonFrame = Frame(self.Window)
        self.Undo_Button = Button(self.ButtonFrame,text="Undo",command=self.Undo_Func,font=(12))
        self.Save_Button = Button(self.ButtonFrame,text="Save",font=(12),command=self.Save_Func)
        self.Load_Button = Button(self.ButtonFrame,text="Load",font=(12),command=self.Load_Func)
        self.Reset_Button = Button(self.ButtonFrame,text="Reset",font=(12),command=self.ask_Reset)
        self.Tutor_Button = Button(self.ButtonFrame,text="Tutor",font=(12),command=self.Tutor_Func)
        self.GridSize = MapSize
        self.TargetValue = Target
        self.Label_Grid,self.Grid_Node = self.GenerateGrid(self.GridSize,12,6)
        self.GridFrame.pack(side="left")
        self.ButtonFrame.pack(side="right",anchor="n")
        self.Undo_Button.pack(fill="x")
        self.Save_Button.pack(fill="x")
        self.Load_Button.pack(fill="x")
        self.Reset_Button.pack(fill="x")
        self.Tutor_Button.pack(fill="x")
        self.Window.bind("<Key>",self.Move)
        self.Spawn_Node(2)
        self.Spawn_Node(2)

        self.Window.mainloop()

    def Tutor_Func(self):
        messagebox.showinfo(message="Gerakkan Kotak dengan Tombol W,A,S,D.\n W untuk ke atas,\nA untuk ke kiri,\ndst\n\n Rules:Gabungkan kotak yang sama sampai angka 2048\n\nAplikasi ini dibuat oleh: FS (void)",title="Tutorial")

    def GenerateGrid(self,n:int,lebar:int,tinggi:int):
        Result_Gird = [[None for _ in range(n)] for _ in range(n)]
        Result_Node = [[0 for _ in range(n)] for _ in range(n)]
        for rows in range(n):
            for columns in range(n):
               Result_Gird[rows][columns] = Label(
                   self.GridFrame,
                   width=lebar,
                   height=tinggi,
                   bg="#cdc1b4",
                   borderwidth=2,
                   relief='solid',
                   font=('Arial', 14))
               Result_Gird[rows][columns].grid(row=rows,column=columns)

        return Result_Gird,Result_Node

    def Custom_Spawn(self,InputNum:int,row:int,column:int):
            current = self.Grid_Node[row][column]
            if(current == 0):
                self.Update(InputNum,self.Label_Grid[row][column])
                self.Grid_Node[row][column] = InputNum



    def Spawn_Node(self,Value:int):
        for i in range(self.GridSize**2):
            random_row = random.randint(0,self.GridSize-1)
            random_column = random.randint(0,self.GridSize-1)
            current = self.Grid_Node[random_row][random_column]
            new = [random_row,random_column]
            if(new == self.last_spawnnode):
                continue
            if(current == 0):
                self.Update(Value,self.Label_Grid[random_row][random_column])
                self.Grid_Node[random_row][random_column] = Value
                self.last_spawnnode = new
                break

    def Move(self,event:Event):
        #print(self.Move)

        key = event.keysym
        if(self.Move_bool == True):

            self.Move_bool = False
            if(self.check_key.get(key) == None):
                return
            if (self.check_key[key] == False):
                if(self.check_key["w"] == self.check_key["a"] == self.check_key["s"] == self.check_key["d"] == False):
                    self.Game_Over()
                return
            self.Last_Grid = [row[:] for row in self.Grid_Node]
            match key:
                case "a":
                    self.Move_Left()
                case "d":
                    self.Move_Right()
                case "w":
                    self.Move_up()
                case "s":
                    self.Move_Down()
            if(self.Last_Grid != self.Grid_Node):
                self.Update_Grid()
               # self.Spawn_Node(2)
                list_pilih : list = random.choice(self.__list_empty_node)
                print(f"Update pos choice: ({list_pilih[0]},{list_pilih[1]})")
                self.Custom_Spawn(2,list_pilih[0],list_pilih[1])
                self.check_key["w"] = True
                self.check_key["a"] = True
                self.check_key["s"] = True
                self.check_key["d"] = True
                self.Game_Win()
            else:
                self.check_key[key] = False
                if(self.check_key["w"] == self.check_key["a"] == self.check_key["s"] == self.check_key["d"] == False):
                    self.Game_Over()
        self.Move_bool = True



    def Move_up(self):
        column = []
        for j in range(self.GridSize):
            column = [row[j] for row in self.Grid_Node]
            column = self.Slide_And_Combine(column,"LEFT")
            for i,num in enumerate(column):
                self.Grid_Node[i][j] = num

    def Move_Down(self):
        column = []
        for j in range(self.GridSize):
            column = [row[j] for row in self.Grid_Node]
            column = self.Slide_And_Combine(column,"RIGHT")
            for i,num in enumerate(column):
                self.Grid_Node[i][j] = num

    def Move_Left(self):
        for a,i in  enumerate(self.Grid_Node):
            self.Grid_Node[a] = self.Slide_And_Combine(i,"LEFT")

    def Move_Right(self):
        for a,i in  enumerate(self.Grid_Node):
            self.Grid_Node[a] = self.Slide_And_Combine(i,"RIGHT")

    def Slide_And_Combine(self,row:list[int],align:str):
        new = [tile for tile in row if tile != 0]
        if(len(new) == 0):
            return row
        if(align == "LEFT"):
            for i in range(len(new)-1):
                    if new[i] == new[i+1]:
                        new[i] *= 2
                        new[i+1] = 0
                        if(new[i] >= self.TargetValue):
                            self.Win = True
        else:
             i = len(new)-1
             while i > 0:
                  if new[i] == new[i-1]:
                        new[i] *= 2
                        new[i-1] = 0
                        if(new[i] >= self.TargetValue):
                            self.Win = True
                  i-=1
        new = [tile for tile in new if tile != 0]
        while len(new) < len(row):
            if(align == "LEFT"):
                new.append(0)
            else:
                new.insert(0,0)

        return new

    def Undo_Func(self):
        if(self.Grid_Node == self.Last_Grid or len(self.Last_Grid) == 0):
            return
        self.Grid_Node = self.Last_Grid
        self.Update_Grid()

    def Save_Map_Game(self,data,namefile):
        with open(namefile, mode='w',newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)


    def Save_Func(self):

        filepath = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Simpan Game 2048 sebagai CSV"
        )
        if not filepath:
            return

        self.Save_Map_Game(self.Grid_Node,filepath)

    def Load_Func(self):
        filepath = filedialog.askopenfilename(
        defaultextension=".csv",
        filetypes=[("CSV files", "*.csv")],
        title="Load game"
        )
        if not filepath:
            return
        with open(filepath, mode='r') as file:
            reader = csv.reader(file)
            grid = [[int(cell) for cell in row] for row in reader]
            self.Grid_Node = grid
            self.Update_Grid()
    def ask_Reset(self):
        ans = messagebox.askyesno(title="Reset Game",message="Apakah Kamu mau mengulang game?\n tindakan ini tidak bisa diulang")
        if(ans == False):
            return
        self.Reset()

    def Reset(self):

        for row,a in enumerate(self.Label_Grid):
            for column,b in enumerate(a):
                self.Grid_Node[row][column] = 0
                self.Update(0,b)
        self.check_key["w"] = True
        self.check_key["a"] = True
        self.check_key["s"] = True
        self.check_key["d"] = True
        self.Spawn_Node(2)
        self.Spawn_Node(2)

    def Game_Win(self):
        if(self.Win != True):
            return
        answer = messagebox.askyesno(title="Kamu Menang",message=f"Kamu Telah mencapai/melebihi angka {self.TargetValue}, Apakah kamu mau melanjutkan?")
        if(answer):
            self.Win = False
            self.TargetValue *= 2
            return
        else:
            messagebox.showinfo(title="Terima Kasih", message="Terima Kasih Sudah Bermain :D")
            self.Window.destroy()

    def Game_Over(self):
        ans = messagebox.askretrycancel(title="Kalah",message="Kamu Kalah\nApakah kamu mau coba lagi?")
        if(ans != True):
            messagebox.showinfo(title="Terima Kasih", message="Terima Kasih Sudah Bermain :D")
            self.Window.destroy()
        else:
            self.Reset()
            self.Last_Grid = []

    def Update_Grid(self):
        self.__list_empty_node = []
        for row in range(self.GridSize):
            for columns in range(self.GridSize):
                self.Update(self.Grid_Node[row][columns],self.Label_Grid[row][columns])
                if (self.Grid_Node[row][columns] == 0):
                    self.__list_empty_node.append([row,columns])
                    if(self.__debug == True):
                        self.Label_Grid[row][columns].config(text=f"{row},{columns}")
        print(self.__list_empty_node)
    def Update(self,InputValue:int,Widget:Label):
        if InputValue in self.color_mapping:
            color_info = self.color_mapping[InputValue]
            Widget.config(bg=color_info["bg"],fg=color_info["fg"],text=InputValue if InputValue != 0 else f"")
        else:
        # Handling untuk nilai yang melebihi apa yang ada di dictionary
            Widget.config(bg="#3c3a32", fg="#f9f6f2", text=InputValue)

    color_mapping = {
        #Color Node Mapping
    0: {"bg": "#cdc1b4", "fg": "#776e65"},
    2: {"bg": "#eee4da", "fg": "#776e65"},
    4: {"bg": "#ede0c8", "fg": "#776e65"},
    8: {"bg": "#f2b179", "fg": "#f9f6f2"},
    16: {"bg": "#f59563", "fg": "#f9f6f2"},
    32: {"bg": "#f67c5f", "fg": "#f9f6f2"},
    64: {"bg": "#f65e3b", "fg": "#f9f6f2"},
    128: {"bg": "#edcf72", "fg": "#f9f6f2"},
    256: {"bg": "#edcc61", "fg": "#f9f6f2"},
    512: {"bg": "#edc850", "fg": "#f9f6f2"},
    1024: {"bg": "#edc53f", "fg": "#f9f6f2"},
    2048: {"bg": "#edc22e", "fg": "#f9f6f2"},
    4096: {"bg": "#3c3a32", "fg": "#f9f6f2"},
    8192: {"bg": "#6a0dad", "fg": "#f9f6f2"},
    16384: {"bg": "#a93226", "fg": "#f9f6f2"},
    32768: {"bg": "#191970", "fg": "#f9f6f2"},
    65536: {"bg": "#2ecc71", "fg": "#f9f6f2"}

}
Game_2048(4,2048)
