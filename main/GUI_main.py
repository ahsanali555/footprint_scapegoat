from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk
import OCR as imagereader
#import tree as scapegoat
import scapegoat as bst
import csv
import os
import time

Menu = Tk()
Menu.title("Footprint Calculator")
Menu.configure(bg="#ffffff")

# Tree making from Excel Dataset


def treeMaker(foodTree):
    foodList = []
    with open('footprint.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        var = 0
        for row in csv_reader:
            if line_count > 1000:
                break
            if line_count == 0:
                # print(Error: No Food Items Found)
                pass
            else:
                foodName = row[1].lower()
                waterFootprint = float(row[2])+float(row[3])+float(row[4])
                carbonFootprint = float(row[7])+float(row[8])+float(row[9])
                foodInfo = [foodName, round(
                    waterFootprint, 5), round(carbonFootprint, 5)]
                foodList.append(foodInfo)
                # print(foodInfo)
            line_count += 1
    data = foodList

    for i in range(0, len(data)):
        foodTree.insert(data[i])
    '''
    root = None
    scapegoatTree = scapegoat.BST(root)
    root = scapegoatTree.insert(root, data[0])
    for i in range(1, len(data) - 1):
        scapegoatTree.insert(root, data[i])
        # print(data[i])
    scapegoatTree.Inorder(root)
    return scapegoatTree
    '''
    return foodTree


global foodTree
foodTree = bst.ScapeGoatTree(0.5)
foodScapeGoat = treeMaker(foodTree)
# foodScapeGoat.printTree()
# print(foodScapeGoat.search('salt'))
#####


def center_window(root, w=300, h=200):
    # get screen width and height
    ws = root.winfo_screenwidth()
    hs = root.winfo_screenheight()
    # calculate position x, y
    x = (ws/2) - (w/2)
    y = (hs/2) - (h/2)
    root.geometry('%dx%d+%d+%d' % (w, h, x, y))


def is_number(string):
    try:
        float(string)
        return True
    except ValueError:
        return False


def foodListMaker(detectedFood):
    # compare scapegoat-tree and detectedfood to make fooditems list containing lists with name wf and cp
    for item in detectedFood:
        treeItem = foodScapeGoat.search(item)
        if treeItem != None:
            foodItems.append(treeItem.key)
    for ingredients in foodItems:
        # print(ingredients.key[0])
        foodItemsString.append(ingredients[0])
        IngredientsBox.insert(END, ingredients[0]+' ')


def open_img_file():
    filename = filedialog.askopenfilename(initialdir=os.getcwd(
    ), title="Select file", filetypes=(("png images", ".png", ".jpg"), ("all files", "*.*")))
    if not filename:
        return
    # setup new window
    new_window = Toplevel(Menu)
    # get image
    image1 = Image.open(filename)
    image1 = image1.resize((600, 800), Image.ANTIALIAS)
    selectedImage = ImageTk.PhotoImage(image1)
    # load image
    panel = Label(new_window, image=selectedImage)
    panel.image = selectedImage
    panel.pack()

    foodDetected = imagereader.Get_Ingredients(filename, 'ingredients.csv')

    resetBox()
    foodListMaker(foodDetected)


#  Prominent Arduino map function :)
def mapPB(x, in_min, in_max, out_min, out_max):
    return int((x - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)


def computeFootprint():
    # use the tree to traverse with foodItems list
    # add condition for empty foodItems list
    waterBox.delete("1.0", END)
    carbonBox.delete("1.0", END)
    totalWaterFootprint = 0
    totalCarbonFootprint = 0
    for item in foodItems:
        totalWaterFootprint += item[1]
        totalCarbonFootprint += item[2]
    waterBox.insert(END, totalWaterFootprint)
    carbonBox.insert(END, totalCarbonFootprint)

    rescaleWater = mapPB(totalWaterFootprint, 0, 20000, 0, 50)
    rescaleCarbon = mapPB(totalCarbonFootprint, 0, 500, 0, 50)

    # print(foodItems)
    pb['value'] = rescaleCarbon+rescaleWater


def resetBox():
    IngredientsBox.delete('1.0', END)
    addItemBox.delete("1.0", END)
    addItemResultBox.delete("1.0", END)
    IrrigationWaterBox.delete("1.0", END)
    FreshWaterBox.delete("1.0", END)
    RainWaterBox.delete("1.0", END)
    CO2Box.delete("1.0", END)
    SO2Box.delete("1.0", END)
    PO4Box.delete("1.0", END)
    waterBox.delete("1.0", END)
    carbonBox.delete("1.0", END)
    foodItems.clear()
    foodItemsString.clear()
    pb['value'] = 0


def addItem():
    foodName = addItemBox.get("1.0", END)
    irrigationWater = IrrigationWaterBox.get("1.0", END)
    freshWater = FreshWaterBox.get("1.0", END)
    rainWater = RainWaterBox.get("1.0", END)
    C02 = CO2Box.get("1.0", END)
    S02 = SO2Box.get("1.0", END)
    P04 = PO4Box.get("1.0", END)
    if foodName == '\n':
        addItemResultBox.delete("1.0", END)
        addItemResultBox.insert(END, 'Please enter the Ingredient Name')
    elif not (is_number(irrigationWater) and is_number(freshWater) and is_number(rainWater)
              and is_number(C02) and is_number(S02) and is_number(P04)):
        addItemResultBox.delete("1.0", END)
        addItemResultBox.insert(
            END, 'Please enter numeric values for Ingredient paramaters')
    elif foodName.rstrip("\n") in foodItemsString:
        addItemResultBox.delete("1.0", END)
        addItemResultBox.insert(
            END, 'Ingredient already present')
    else:
        addItemResultBox.delete("1.0", END)
        addItemResultBox.insert(END, 'Food Ingredient successfully added')
        waterFootprint = float(irrigationWater) + \
            float(freshWater)+float(rainWater)
        carbonFootprint = float(C02)+float(S02)+float(P04)
        foodInfo = [foodName.rstrip("\n"), round(
            waterFootprint, 5), round(carbonFootprint, 5)]

        foodItems.append(foodInfo)
        IngredientsBox.insert(END, foodName.rstrip("\n")+' ')
        foodItemsString.append(foodName.rstrip("\n"))
        # print(foodItems)


def inMenu(buttons):  # Interface
    global Menu
    # rendering image for menupage on the same window
    Menu.configure(bg="white")
    background = Image.open(
        "images/inmenu.png")
    img = PhotoImage(file="images/inmenu.png")
    render = Label(image=img)
    render.image = img
    render.place(x=0, y=0)

    # Food items and their information for selected food picture
    global foodItems
    foodItems = []
    global foodItemsString
    foodItemsString = []

    # Creating Scapegoat tree from excel dataset
    #scapegoatTree = treeMaker()
    # print(scapegoatTree.root)
    #print(scapegoatTree.search(root, 'salt'))

    # Upload Food Image
    upload = ImageTk.PhotoImage(
        (Image.open("images/upload.png")).resize((100, 30), Image.ANTIALIAS))  # Upload button
    uploadButton = Button(Menu, text="Upload Food", compound=TOP, image=upload,
                          bd=0, bg='#1b82ab', command=lambda: open_img_file(), activebackground='#1b82ab', fg="white")
    uploadButton.place(x=40, y=10)

    # Reset all entries
    reset = ImageTk.PhotoImage(
        (Image.open("images/reset.png")).resize((100, 30), Image.ANTIALIAS))  # Upload button
    resetButton = Button(Menu, text="Clear Food", compound=TOP, image=reset,
                         bd=0, bg='#1b82ab', command=lambda: resetBox(), activebackground='#1b82ab', fg="white")
    resetButton.place(x=40, y=70)

    # Ingredient box
    global IngredientsBox
    IngredientsBox = Text(Menu, height=5, width=70,
                          xscrollcommand=set(), font=("Arial", 10))
    IngredientsBox.place(x=180, y=40)
    Ingredients = Label(Menu, text='Food Ingredients Detected', bd=0,
                        bg='#39b549', activebackground='#39b549', fg="white")
    Ingredients.place(x=180, y=10)
    Ingredients.config(font=("Arial", 14))

    # Add an Ingredient
    add = ImageTk.PhotoImage(
        (Image.open("images/add.png")).resize((100, 30), Image.ANTIALIAS))  # Upload button
    addButton = Button(Menu, text="Add Item", compound=TOP, image=add,
                       bd=0, bg='#1b82ab', command=lambda: addItem(), activebackground='#1b82ab', fg="white")
    addButton.place(x=40, y=180)

    # Parameters to be added for a food

    global IrrigationWaterBox
    IrrigationWaterBox = Text(
        Menu, height=1, width=11, xscrollcommand=set(), font=("Arial", 10))
    IrrigationWaterBox.place(x=180, y=215)
    IrrigationWater = Label(Menu, text='Irrigation Water\nper million kcal', bd=0,
                            bg='#1b82ab', activebackground='#1b82ab', fg="white")
    IrrigationWater.place(x=180, y=180)
    IrrigationWater.config(font=("Arial", 10))

    global FreshWaterBox
    FreshWaterBox = Text(Menu, height=1, width=11,
                         xscrollcommand=set(), font=("Arial", 10))
    FreshWaterBox.place(x=280, y=215)
    FreshWater = Label(Menu, text='Fresh Water\nper million kcal', bd=0,
                       bg='#1b82ab', activebackground='#1b82ab', fg="white")
    FreshWater.place(x=280, y=180)
    FreshWater.config(font=("Arial", 10))

    global RainWaterBox
    RainWaterBox = Text(Menu, height=1, width=11,
                        xscrollcommand=set(), font=("Arial", 10))
    RainWaterBox.place(x=380, y=215)
    RainWater = Label(Menu, text='Rain Water\nper million kcal', bd=0,
                      bg='#1b82ab', activebackground='#1b82ab', fg="white")
    RainWater.place(x=380, y=180)
    RainWater.config(font=("Arial", 10))

    global CO2Box
    CO2Box = Text(Menu, height=1, width=11,
                  xscrollcommand=set(), font=("Arial", 10))
    CO2Box.place(x=480, y=215)
    CO2 = Label(Menu, text='CO2 Emission\nper million kcal', bd=0,
                bg='#39b549', activebackground='#39b549', fg="white")
    CO2.place(x=480, y=180)
    CO2.config(font=("Arial", 10))

    global SO2Box
    SO2Box = Text(Menu, height=1, width=11,
                  xscrollcommand=set(), font=("Arial", 10))
    SO2Box.place(x=580, y=215)
    SO2 = Label(Menu, text='SO2 Emission\nper million kcal', bd=0,
                bg='#39b549', activebackground='#39b549', fg="white")
    SO2.place(x=580, y=180)
    SO2.config(font=("Arial", 10))

    global PO4Box
    PO4Box = Text(Menu, height=1, width=11,
                  xscrollcommand=set(), font=("Arial", 10))
    PO4Box.place(x=680, y=215)
    PO4 = Label(Menu, text='PO4 Emission\nper million kcal', bd=0,
                bg='#39b549', activebackground='#39b549', fg="white")
    PO4.place(x=680, y=180)
    PO4.config(font=("Arial", 10))

    global addItemBox
    addItemBox = Text(
        Menu, height=1, width=11, xscrollcommand=set(), font=("Arial", 10))
    addItemBox.place(x=180, y=270)
    addIngredient = Label(Menu, text='Ingredient Name', bd=0,
                          bg='#39b549', activebackground='#39b549', fg="white")
    addIngredient.place(x=180, y=250)
    addIngredient.config(font=("Arial", 10))

    global addItemResultBox
    addItemResultBox = Text(
        Menu, height=1, width=60, xscrollcommand=set(), font=("Arial", 10))
    addItemResultBox.place(x=300, y=270)
    addItemResult = Label(Menu, text='Result', bd=0,
                          bg='#39b549', activebackground='#39b549', fg="white")
    addItemResult.place(x=300, y=250)
    addItemResult.config(font=("Arial", 10))

    # Compute Footprint
    compute = ImageTk.PhotoImage(
        (Image.open("images/compute.png")).resize((100, 30), Image.ANTIALIAS))  # Upload button
    computeButton = Button(Menu, text="Find Footprint", compound=TOP, image=compute,
                           bd=0, bg='#1b82ab', command=lambda: computeFootprint(), activebackground='#1b82ab', fg="white")
    computeButton.place(x=40, y=345)

    global waterBox
    waterBox = Text(Menu, height=1, width=9,
                    xscrollcommand=set(), font=("Arial", 10))
    waterBox.place(x=200, y=430)
    unitWater = Label(Menu, text='per million kcal', bd=0,
                      bg='#1b82ab', activebackground='#39b549', fg="white")
    unitWater.place(x=270, y=430)
    unitWater.config(font=("Arial", 10))

    waterFootprint = Label(Menu, text='Water Footprint:   ', bd=0,
                           bg='#1b82ab', activebackground='#39b549', fg="white")
    waterFootprint.place(x=40, y=430)
    waterFootprint.config(font=("Arial", 14))

    global carbonBox
    carbonBox = Text(Menu, height=1, width=9,
                     xscrollcommand=set(), font=("Arial", 10))
    carbonBox.place(x=200, y=460)
    unitCarbon = Label(Menu, text='per million kcal', bd=0,
                       bg='#39b549', activebackground='#39b549', fg="white")
    unitCarbon.place(x=270, y=460)
    unitCarbon.config(font=("Arial", 10))

    carbonFootprint = Label(Menu, text='Carbon Footprint: ', bd=0,
                            bg='#39b549', activebackground='#39b549', fg="white")
    carbonFootprint.place(x=40, y=460)
    carbonFootprint.config(font=("Arial", 14))

    '''
    global totalFootprintBox
    totalFootprintBox = Text(Menu, height=1, width=9,
                             xscrollcommand=set(), font=("Arial", 10))
    totalFootprintBox.place(x=200, y=530)
    unittotalFootprint = Label(Menu, text='per million kcal', bd=0,
                               bg='#39b549', activebackground='#39b549', fg="white")
    unittotalFootprint.place(x=270, y=530)
    unittotalFootprint.config(font=("Arial", 10))
    '''
    totalFootprint = Label(Menu, text='Total Footprint:     ', bd=0,
                           bg='#39b549', activebackground='#39b549', fg="white")
    totalFootprint.place(x=40, y=530)
    totalFootprint.config(font=("Arial", 14))

    # Footprint scale
    scaleImage = Image.open(  # rendering image on the first window
        "images/indicator.PNG")
    scaleImage = scaleImage.resize((300, 23), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(scaleImage)
    scaleimg = Label(image=render)
    scaleimg.image = render
    scaleimg.place(x=200, y=500)

    global pb
    pb = ttk.Progressbar(Menu, orient='horizontal',
                         mode='determinate', length=303)
    pb.place(x=200, y=530)

    global Backbutton
    Backy = ImageTk.PhotoImage(
        (Image.open("images/Back2.png")).resize((35, 28), Image.ANTIALIAS))
    Backbutton = Button(Menu, image=Backy, bd=2, bg="#1b82ab",
                        activebackground="#1b82ab", command=lambda: Mainpage()).place(x=40, y=565)

    Menu.mainloop()


def Aboutpage():  # About Page
    center_window(Menu, 800, 600)
    load = Image.open(  # rendering image on the first window
        "images/about_BG.PNG")
    load = load.resize((800, 600), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.place(x=0, y=0)
    global Backbutton
    Backy = ImageTk.PhotoImage(
        (Image.open("images/Back2.png")).resize((35, 28), Image.ANTIALIAS))
    Backbutton = Button(Menu, image=Backy, bd=2, bg="green",
                        activebackground="green", command=lambda: Mainpage()).place(x=40, y=565)

    Menu.mainloop()


def Mainpage():  # first page
    center_window(Menu, 800, 600)
    load = Image.open(  # rendering image on the first window
        "images/mainmenu.PNG")
    load = load.resize((800, 600), Image.ANTIALIAS)
    render = ImageTk.PhotoImage(load)
    img = Label(image=render)
    img.image = render
    img.place(x=0, y=0)
    Nextbutton = ImageTk.PhotoImage(
        (Image.open("images/calculate.png")).resize((200, 80), Image.ANTIALIAS))  # Next button
    Next = Button(Menu, image=Nextbutton, bd=5, background='green',
                  width=180, height=60, activebackground="#1b82ab", command=lambda: inMenu(Next)).place(x=180, y=280)

    Nextbutton2 = ImageTk.PhotoImage(
        (Image.open("images/about.png")).resize((140, 50), Image.ANTIALIAS))  # Next button
    Next = Button(Menu, image=Nextbutton2, bd=5, background='green',
                  width=180, height=60, activebackground="#1b82ab", command=lambda: Aboutpage()).place(x=430, y=280)
    Menu.mainloop()


Mainpage()
