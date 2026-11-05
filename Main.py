#  Creator: Fajar Sudarta

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
    __MIN_SIZE = 2
    __MAX_SIZE = 5
    __Highest_Score = 0
    fail = False
#Mapsize merupakan ukuran grid node yaitu 4x4,
# Target merupakan target score yang mau dicapai
    def __init__(self,MapSize:int,Target:int):
        # Inisilisasi
        os.system("cls")
        self.Window = Tk()
        self.Window.title("2048")
        self.GridFrame = Frame(self.Window)
        self.ButtonFrame = Frame(self.Window)
        # Inisialiasi Button
        self.Undo_Button = Button(self.ButtonFrame,text="Undo",command=self.Undo_Func,font=(12))
        self.Save_Button = Button(self.ButtonFrame,text="Save",font=(12),command=self.Save_Func)
        self.Load_Button = Button(self.ButtonFrame,text="Load",font=(12),command=self.Load_Func)
        self.Reset_Button = Button(self.ButtonFrame,text="Reset",font=(12),command=self.ask_Reset)
        self.Tutor_Button = Button(self.ButtonFrame,text="Tutor",font=(12),command=self.Tutor_Func)
        self.GridSize = MapSize
        self.TargetValue = Target

        #generate map 2048
        print(MapSize)
        if(MapSize < self.__MIN_SIZE or MapSize > self.__MAX_SIZE):
            print("Error")
            messagebox.showwarning(title="warning: melibihi aturan",message=f"Ukuran map telah melebihi batas ataupun telah keluar dari batas minimal\nMinimal ukuran: 2x2\nMaksimal Ukuran: 5\n ukuran yang dinput: {MapSize}")
            self.Window.destroy()
        self.Label_Grid,self.Grid_Node = self.GenerateGrid(self.GridSize,12,6)
        # self.Label_Grid adalah array 2 dimensi yang menyimpan widget atau objek node yang menjadi tampilan di Aplikasi
        # sedangkan self.Grid_Node merupakan data asli dari sesi permainan yang bertipe data interger 2 dimensi

      # meletakkan objek ke aplikasi langsung
        self.GridFrame.pack(side="left")
        self.ButtonFrame.pack(side="right",anchor="n")
        self.Undo_Button.pack(fill="x")
        self.Save_Button.pack(fill="x")
        self.Load_Button.pack(fill="x")
        self.Reset_Button.pack(fill="x")
        self.Tutor_Button.pack(fill="x")

        # menghubungkan function move ke tombol keyboard ketika tombol dipencet, move function tereksekusi
        self.Window.bind("<Key>",self.Move)

       # Meng spawn node secara random di awal2 permainan
        self.Spawn_Node(2)
        self.Spawn_Node(2)

        # self.Spawn_Node(1024)
        # self.Spawn_Node(1024)
        # self.Custom_Spawn(2,0,0)
        # self.Custom_Spawn(2,0,1)
        # self.Custom_Spawn(2,0,2)
        # self.Custom_Spawn(2,0,3)

        self.Window.mainloop()

    def Tutor_Func(self):
        messagebox.showinfo(message="Gerakkan Kotak dengan Tombol W,A,S,D.\n W untuk ke atas,\nA untuk ke kiri,\ndst\n\n Rules:Gabungkan kotak yang sama sampai angka 2048\n\nAplikasi ini dibuat oleh: FS (void)",title="Tutorial")

# Fungsi ini mengenerate map dari game 2048, parameter n merupakan ukuran map dari 2048
#  jika n = 4 maka map game ukurannya 4x4,
# Parameter lebar_node dan tinggi_node adalah ukuran dari tiap node itu.
    def GenerateGrid(self,n:int,lebar_node:int,tinggi_node:int):

        # result_grid adalah data objek antarmuka aplikasi
        Result_Grid = [[None for _ in range(n)] for _ in range(n)]
        # result_node adalah data nilai internal dari sesi gameplay
        Result_Node = [[0 for _ in range(n)] for _ in range(n)]
        for rows in range(n):
            for columns in range(n):

               Result_Grid[rows][columns] = Label(
                   self.GridFrame,
                   width=lebar_node,
                   height=tinggi_node,
                   bg="#cdc1b4",
                   borderwidth=2,
                   relief='solid',
                   font=('Arial', 15, 'bold')
               )
               Result_Grid[rows][columns].grid(row=rows,column=columns)
        return Result_Grid,Result_Node

# Melakukan spawn node secara custom, Inputnum adalah skor, row dan column menunjukkan posis pada map
    def Custom_Spawn(self,InputNum:int,row:int,column:int):
            current = self.Grid_Node[row][column]
            self.Update(InputNum,self.Label_Grid[row][column])
            self.Grid_Node[row][column] = InputNum


# Random spawn merupakan pembungkus dari custom spawn mendapatkan nilai posisi yang random
    def Spawn_Node(self,Value:int):
        #terkadang ada satu kasus dimana nilai random yang dipilih adalah koordinat posis yang sudah ada nilai
        # maka dari itu fungsi ini akan melakukan looping sampai ketemu tempat yang kosong lalu akan break dari looping
        while(True):
            random_row = random.randint(0,self.GridSize-1)
            random_column = random.randint(0,self.GridSize-1)
            # jika menemukan posisi yang
            if(self.Grid_Node[random_row][random_column] == 0):
                #Memanggil Custom_Spawn sebagai backend
                self.Custom_Spawn(Value,random_row,random_column)
                break

    # mekanisme dari pengecekan kekalahan dilihat dari setiap status tombol WASD.
    # check_key = {"w":True,"a":True,"s":True,"d":True}
    # key diawali dengan pengecekan per tombol yang dipencet jika yang dipencet adalah w maka kotak node akan naik ke atas tetapi jika dipencet terus menerus
    #  lalu akhirnya tombol w tidak membarikan perubahan angka pada map permainan, maka tombol w dilabeli false karna
    #
    # menggunakan konsep dasar  ini yang digunakan untuk mengecek tiap tombol di dalam permainan
    #
    # Mekanisme move function akan selau mengecek apakah semua key bernilai false jika iya maka player
    #  dinyatakan kalah dalam perrmainan karna player yang membuat dirinya  sendiri stuck dalam permainan
    def Move(self,event:Event):
        # #print(self.Move)
        # mekanisme untuk mencegah callback function dipanggil dua kali sebelum function move selesai diproses
        if not self.Move_bool:
            return

        self.Move_bool = False

        try:
            key = event.keysym

            if key not in self.check_key:
                return
            # mengecek Apakah key yang dipencet sama dengan false
            # jika iya maka tombol akan terkunci dan tidak bisa membuat pergerakan. untuk mencegah "Un-neccesary process"
            if not self.check_key[key]:
                # lalu mengecek ke semua kunci apakah false, maka game over
                if not any(self.check_key.values()):
                    self.Game_Over()
                return
            # ini adalah mekanis dalam undo menyimpan data sebelumnya sebenarnya hanya menyimpan data 1 langkah sebelumnya
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

            # apakah terjadi perubahan pada data sesi permainan
            if self.Last_Grid != self.Grid_Node:

                self.Update_Grid()
                # pemilihan posisi node yang kosong berdasarkan list list node  yang kosong
                list_pilih = random.choice(self.__list_empty_node)

                self.Custom_Spawn(
                    2,
                    list_pilih[0],
                    list_pilih[1]
                )
                # Mereset semau status tombol WASD
                self.check_key = {
                    "w": True,
                    "a": True,
                    "s": True,
                    "d": True
                }
                # jika menang maka menang
                if(self.Win == True):
                    self.Game_Win()

            else:
                #tombol yang dipencet akan dilabeli false karna tidak terjadi perubahan dalam pergerakan
                self.check_key[key] = False

                # jika semua status dari tombol WASD semuanya false maka game over
                if not any(self.check_key.values()):
                    print(self.check_key)
                    self.Game_Over()
            print(self.check_key)

        finally:
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
        # inisialisai node hanya akan mengambil yang ada isi nilai nya saja
        #  semisal list:[2,2,0,2] ke arah kiri
        # maka new = [2,2,2]
        # Proses penggaabungan: new = [4,2]
        # Penambahan nilai 0: new = [4,2,0,0]
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
            filetypes=[("CSV files", "*.csv")],
            title="Load game"
        )
        # mengecek apakah filepath kosong
        if not filepath:
            return

        with open(filepath, mode='r', newline='') as file:
            reader = csv.reader(file)
            grid = list(reader)

            # Menghitung jumlah baris dan kolom
            rows = len(grid)
            cols = len(grid[0]) if rows > 0 else 0

            print(f"Rows: {rows}, Columns: {cols}")

            # Validasi ukuran grid
            if rows != self.GridSize or cols != self.GridSize:
                messagebox.showwarning(
                    title="Ukuran Grid Tidak Sesuai",
                    message=(
                        f"Ukuran grid CSV tidak sesuai.\n"
                        f"Baris: {rows}\n"
                        f"Kolom: {cols}\n"
                        f"Ukuran yang dibutuhkan: "
                        f"{self.GridSize} x {self.GridSize}"
                    )
                )
                return

            try:
                grid = [[int(cell) for cell in row] for row in grid]
            except ValueError:
                messagebox.showwarning(
                    title="Data Tidak Valid",
                    message="CSV mengandung data yang bukan angka."
                )
                return

            self.Grid_Node = grid
            self.Update_Grid()
   # fngsi yang yang menjadi antarmuka tombol reset
    def ask_Reset(self):
        ans = messagebox.askyesno(title="Reset Game",message="Apakah Kamu mau mengulang game?\n tindakan ini tidak bisa diulang")
        if(ans == False):
            return
        self.Reset()

    # Mereset permainan
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
        answer = messagebox.askyesno(title="Kamu Menang",message=f"Kamu Telah mencapai/melebihi angka {self.TargetValue}, Apakah kamu mau melanjutkan?")
        if(answer):
            self.Win = False
            self.TargetValue *= 2
            return
        else:
            messagebox.showinfo(title="Terima Kasih", message="Terima Kasih Sudah Bermain :D")
            self.Window.destroy()

    def Game_Over(self):
        ans = messagebox.askretrycancel(title="Kalah",message=f"Kamu Kalah\nApakah kamu mau coba lagi?\n Skor Tertinggi dalam satu sesi: {self.__Highest_Score}")
        if(ans != True):
            messagebox.showinfo(title="Terima Kasih", message="Terima Kasih Sudah Bermain :D")
            self.Window.destroy()
        else:
            self.Reset()
            self.Last_Grid = []
# Update grid pada dasarnya fungsi ini melakukan update tampilan dari informasi nilai yang sebenarnya.
# data permainan disimpan secara terrpisah dari sebagai array multi dimensi dan objek gui yaitu label sebagai tampilan yang menyamai dari data game internal
# fungsi akan looping tiap node pada array 2 dimensi
    def Update_Grid(self):
        self.__list_empty_node = []
        for row in range(self.GridSize):
            for columns in range(self.GridSize):
                #looping tiap node untuk memperbarui nilai skor sesuai pada data internal yaitu Grid_Node
                self.Update(self.Grid_Node[row][columns],self.Label_Grid[row][columns])

                # Memperbarui capaian skor permainan
                if (self.__Highest_Score < self.Grid_Node[row][column]):
                    self.__Highest_Score = self.Grid_Node[row][column];
                # jika pada suatu perulangan terdapat node yang kosong pada posisi tertentu maka ditambahkan
                # sebagai list calon penempatan node random setelah pergerakan user
                if (self.Grid_Node[row][columns] == 0):
                    self.__list_empty_node.append([row,columns])
                    if(self.__debug == True):
                        self.Label_Grid[row][columns].config(text=f"{row},{columns}")
        # print(self.__list_empty_node)
    # Fungsi ini merupakan untuk mengupdate node pada posisi tertentu
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

# Eksekusi kode dimulai dari sini
if __name__ == "__main__":
    Game_2048(4,2048)
