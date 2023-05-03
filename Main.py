import random
global Codes, Movies, Times, IMDbs, Date, Status, Rounds, TicketList
global S_Codes, S_Movies, S_Times, S_IMDbs, S_Date, S_Status
global Drinks, Foods, Sets, Items, Tickets, Checks
global FoodList, Seats, TotalSeat
Codes, Movies, Times, IMDbs, Date, Status, Rounds = [], [], [], [], [], [], {}
S_Codes, S_Movies, S_Times, S_IMDbs, S_Date, S_Status = [], [], [], [], [], []
Drinks, Foods, Sets, Items = {}, {}, {}, {}
SelectRound, Seats, Tickets, Checks = [], [], {}, []
FoodList, SeatList, TicketList = [], [], {}
Menu, Movie, Food, TotalSeat = "", "", "", 0

def LoadMovies():
  File = open("Final Project I/Movies.txt", "r")
  Lines = File.readlines()
  Index = 0
  for Line in Lines:
    Movie = Line.split("#")
    if Movie[4] == "R" or Movie[4] == "R\n":
      Codes.append("R%02d" % (Index))
      Movies.append(Movie[0])
      Times.append(float(Movie[1]))
      IMDbs.append(float(Movie[2]))
      Date.append(Movie[3])
      Status.append(Movie[4])
    else:
      S_Codes.append("S%02d" % (Index))
      S_Movies.append(Movie[0])
      S_Times.append(float(Movie[1]))
      S_IMDbs.append(float(Movie[2]))
      S_Date.append(Movie[3])
      S_Status.append(Movie[4])
    Index += 1
  LoadRounds()
  File.close()

def LoadRounds():
  File = open("Final Project I/Rounds.txt", "r")
  Lines = File.readlines()
  for Line in Lines:
    Movie = Line.replace("\n", "").split("#")
    if Movie[0][0] == "R":
      Rounds[Movie[0]] = Movie[1::]
  File.close()

def LoadDrinkAndFood():
  File = open("Final Project I/DrinkFood.txt", "r")
  Lines = File.readlines()
  for Line in Lines:
    Item = Line.replace("\n", "").split("#")
    if Item[0][0] == "P":
      Foods[Item[0]] = Item[2]
    elif Item[0][0] == "D":
      Drinks[Item[0]] = Item[2]
    elif Item[0][0] == "S":
      Sets[Item[0]] = Item[2]
    Items[Item[0]] = Item[1]
  File.close()

def LoadTickets():
  File = open("Final Project I/Tickets.txt", "r")
  Lines = File.readlines()
  for Line in Lines:
    Item = Line.replace("\n", "").split("#")
    TicketList[Item[0]] = Item[1], Item[2], Item[3::]
  File.close()

def LoadChecks():
  File = open("Final Project I/Checks.txt", "r")
  Lines = File.readlines()
  for Line in Lines:
    Item = Line.replace("\n", "")
    Checks.append(Item)
  File.close()

def WriteTicket(NMovie):
  File = open("Final Project I/Tickets.txt", "a")
  Id = str(random.randint(1, 100))
  Index = 0
  while Index != 1:
    if Id not in TicketList:
      Movie = ""
      Round = ""
      Seat = []
      Text = Id + "#"
      Tickets[Id] = NMovie, SelectRound, SeatList
      for Ticket in Tickets.items():
        Movie = Ticket[1][0]
        Round = Ticket[1][1]
        Text += Movie + "#"
        Text += Round[0] + "#"
        i = 0
        Count = len(Ticket[1][2])
        for Item in Ticket[1][2]:
          Seat.append(Item)
          Text += Item + "\n" if Count > 1 and i + 1 == Count else Item + "#"
          i += 1
      TicketList[Id] = Movie, Round, Seat
      Tickets.clear()
      SelectRound.clear()
      SeatList.clear()
      Index += 1
  File.write(Text)
  File.close()

def WriteChecks(Code):
  File = open("Final Project I/Checks.txt", "a")
  File.write(Code + "\n")
  File.close()

def ShowMovies():
  print("=" * 88)
  print("| {0} |".format("- Now Showing -".center(84)))
  print("=" * 88)
  for i in range(len(Movies)):
    print("| %-3s | %-35s Time: %4.2f hour IMDb: %3.1f Date: %10s |" % (Codes[i], Movies[i], Times[i], IMDbs[i], Date[i]))
  print("=" * 88)
  print("| {0} |".format("- Comming Soon -".center(84)))
  print("=" * 88)
  for i in range(len(S_Movies)):
    print("| %-3s | %-35s Time: %4.2f hour IMDb: %3.1f Date: %10s |" % (S_Codes[i], S_Movies[i], S_Times[i], S_IMDbs[i], S_Date[i]))
  print("=" * 88)
  print("| {0} |".format("Price 100 of every movie".ljust(84)))
  print("=" * 88)

def ShowDrinksAndFood():
  print("=" * 88)
  print("| {0} |".format("Drinks And Food".center(84)))
  print("=" * 88)
  print("| {0} | {1} | {2} |".format("Code".center(4), "Price".center(5), "Item".center(69)))
  print("=" * 88)
  for Item in Items:
    print("| {0} | {1} | {2} |".format(Item.center(4), Foods[Item].center(5) 
    if Item[0] == "P" else Drinks[Item].center(5) if Item[0] == "D" else Sets[Item].center(5), Items[Item].ljust(69)))
  print("=" * 88)

def ShowRounds(Movie):
  print("=" * 88)
  Text_Round = ""
  Index = 1
  for Round in Rounds[Movie]:
    Text_Round += "   " + Round + " | "
    Index += 1
  print("| Rounds |   {0}".format(Text_Round))
  print("=" * 88)

def ShowSeat(Movie, Round):
  Seat = ""
  for i in range(5, -1, -1):
    for j in range(0, 10):
      Id = str(i) + str(j)
      SeatCode = "xx" if GetSeat(Movie, Round, Id) else Id
      Seats.append(SeatCode)
      Seat += "| " + SeatCode
      if i != 0:
        Seat += " | "
        if j == 9:
          Seat += "\n"
        else:
          Seat += "- "
      else:
        if j != 9:
          Seat += " | - "
        else:
          Seat += " |"
  print("=" * 88)
  print("{0}".format(Seat))
  print("=" * 88)
  print("| {0} |".format("Price 150 per seat".ljust(84)))
  print("=" * 88)

def GetSeat(Movie, Round, Seat):
  for Ticket in TicketList.items():
    if Movie == Ticket[1][0]:
      if Round == Ticket[1][1]:
        if Seat in Ticket[1][2]:
          return True

def SelectMenu(Menu):
  if Menu == "S":
    ShowMovies()
    Continue = "Y"
    while Continue != "N":
      if Continue in ["Y", "N"]:
        Movie = input("-> Select movie code : ")
        if Movie in Codes:
          ShowRounds(Movie)
          Round = input("-> Select Show time : ")
          if Round in Rounds[Movie]:
            SelectRound.append(Round)
            ShowSeat(Movie, Round)
            Amount = int(input("-> Amount of seat : "))
            i = 0
            while i != Amount:
              SeatCode = input("-> Selected seat [{0}] : ".format(i + 1))
              if SeatCode in Seats:
                SeatList.append(SeatCode)
                i += 1
              elif SeatCode == "xx":
                print("This seat cannot be selected because someone has been selected!!\nTry again.")
              else:
                print("Invalid seat code!!")
            TotalSeat = len(SeatList)
            WriteTicket(Movie)
            LoadTickets()
          else:
            print("Invalid round show time!!")
        elif Movie in S_Codes:
          print("Can't select because the movie hasn't been released yet.")
        else:
          print("Invalid Item!!")
      else:
        print("Invalid Key!!\nTry again.")
      Continue = input("Want to continue? [Y/N] : ")
      if Continue == "N":
        if TotalSeat != 0:
          Amount = 100 + (150 * TotalSeat)
          print("-> Pay amount %.2f Baht" % (Amount))
  elif Menu == "B":
    ShowDrinksAndFood()
    Continue = "Y"
    while Continue != "N":
      if Continue in ["Y", "N"]:
        Food = input("-> Select drink or food or set : ")
        if Food in Items:
          if Food[0] == "P":
            FoodList.append(Foods[Food])
          elif Food[0] == "D":
            FoodList.append(Drinks[Food])
          elif Food[0] == "S":
            FoodList.append(Sets[Food])
        else:
          print("Invalid Item!!")
      else:
        print("Invalid Key!!\nTry again.")
      Continue = input("Want to continue? [Y/N] : ")
      if Continue == "N":
        Amount = 0
        for i in FoodList:
          Amount += float(i)
        print("-> Pay amount %.2f Baht" % (Amount))
  elif Menu == "W":
    Code = input("-> Please enter your ticket code : ")
    if Code in TicketList:
      if Code not in Checks:
        Checks.append(Code)
        WriteChecks(Code)
        print("Success!! I hope you enjoy the movie.")
      else:
        print("-> Ticket {0} are already in use.".format(Code))
    else:
      print("-> Not found ticket code : {0}".format(Code))
  elif Menu == "E":
    print("-> Exit Program.")

LoadMovies()
LoadDrinkAndFood()
LoadTickets()
LoadChecks()
print("=" * 88)
print("| {0} |".format("Welcome to Unreal Cinema".center(84)))
print("=" * 88)
print("| {0} | {1} |".format("Menu".center(4), "Description".center(77)))
print("=" * 88)
print("| {0} | {1} |".format("S".center(4), "- Select the movie".ljust(77)))
print("| {0} | {1} |".format("B".center(4), "- Buy drinks and food".ljust(77)))
print("| {0} | {1} |".format("W".center(4), "- Enter to the theater".ljust(77)))
print("| {0} | {1} |".format("E".center(4), "- Exit".ljust(77)))
print("=" * 88)
while Menu != "E":
  Menu = input("-> Select menu [S, B, W, E] : ").upper()
  if Menu in ["S", "B", "W", "E"]:
    SelectMenu(Menu)
  else:
    print("Invalid menu!! Try again.")