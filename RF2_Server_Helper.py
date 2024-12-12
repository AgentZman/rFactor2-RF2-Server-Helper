# Import the necessary module
import tkinter as tk
import subprocess
import os
import requests
import zipfile
import shutil
from idlelib.tooltip import Hovertip
import platform

myOS=platform.system()
print(myOS," System")

# Status / Working Notes:
# need to work on outputs to gui and user insteraction instead of terminal window
# also need sudo apt-get install winbind feature.


#Get home/user directory and create working directories for referencing
os.chdir(os.path.expanduser("~")) 
Home=os.getcwd()
#print(Home)

def create_directory_if_not_exists(path):
    """Creates a directory at the specified path if it doesn't already exist."""

    if not os.path.exists(path):
        os.makedirs(path)
        print(f"Directory '{path}' created successfully.")
    else:
        print(f"Directory '{path}'...OK")
    #directory_path = "Racing/SteamCMD"

# Creating Folder for rFactor2 and steamcmd.exe.
directory_path = "Racing/SteamCMD"
create_directory_if_not_exists(directory_path)

# Create other working directories to reference
os.chdir("Racing")
Racing=os.getcwd()
#print(Racing)
os.chdir("SteamCMD")
SteamCMD=os.getcwd()
#print(SteamCMD)
#Checking for steamcmd.zip file
#os.chdir(SteamCMD) #set directory
steamcmd_zipfile = "steamcmd.zip"
steamcmd_exefile = "steamcmd.exe"

if not os.path.isfile(steamcmd_zipfile):
    print("steamcmd.zip does not exist")
    url = "http://media.steampowered.com/installer/steamcmd.zip"
    response = requests.get(url)
    # Check if the request was successful
    if response.status_code == 200:
        with open("steamcmd.zip", "wb") as f:
            f.write(response.content)
            print("steamcmd.zip downloaded successfully!")
            #Extract all the content of the zip file
            with zipfile.ZipFile("steamcmd.zip", 'r') as zip_ref:
                zip_ref.extractall((SteamCMD))
                if os.path.isfile(steamcmd_exefile):
                    print("steamcmd.exe extracted successfully!")
    else:
        print(f"Error downloading file: {response.status_code}")          
else:
    pass
    #print("steamcmd.zip file exists")
if os.path.isfile(steamcmd_exefile):
    print("steamcmd.exe...Ready")

#reminder to len(stdout) and trim strings with \n for comparisons
def run_com1():
    command = "dpkg --print-architecture"  # Check for amd64 Architecture on Linux *typical for current Linux distros
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        button_num[0].config(text=" OK ", fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280)
        
def run_com2():
    command = "dpkg --print-foreign-architectures"  #Check for required i386 architecture on Linux 64bit
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        button_num[1].config(text=" OK ", fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280)
    if (button_num[1]["text"])!= " OK ": #If Not i386
        run_com3()

def run_com3():
    command = ("gnome-terminal -x sudo dpkg --add-architecture i386") # Replace with your desired command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output_label.config(text="i386 architecture added Process Completed\n" + result.stdout, wraplength=280, fg="green")
        run_com2()
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280)

def run_com4():
    command = "wine --version"  # Check Wine Version
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Version:\n" + result.stdout, wraplength=280, fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280, fg="red")

def run_com5():
    command = "winecfg"  # Run and select-Windows 10, Apply, and Save
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        button_num[4].config(text=" OK ", fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280, fg="red")

def run_com6(): # install win and winbind
    command = ("gnome-terminal -x sudo apt install wine winbind") # Replace with your desired command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output_label.config(text="WINE and WINBIND Installed -Process Completed" + result.stdout, wraplength=280, fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error: " + result.stderr, wraplength=280, fg="red")

def run_com7(): #Fix regedit sShortDate 
    command = ("wine reg add \"HKEY_CURRENT_USER\\Control Panel\\International\" /v sShortDate /t REG_SZ /d \"dd/MM/yyyy\" /f") # Replace with your desired command
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output_label.config(text="Registry sShortDate Updated\n" + result.stdout, wraplength=280, fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280, fg="red")

def run_com8(): #Install RF2 Server
    os.chdir(SteamCMD)
    if myOS=="Windows":
        command = ("steamcmd +force_install_dir ../rFactor2-Dedicated +login anonymous +app_update 400300 +quit") # Replace with your desired command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    else:        
        command = ("wine steamcmd +force_install_dir ../rFactor2-Dedicated +login anonymous +app_update 400300 +quit") # Replace with your desired command
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output_label.config(text="SteamCMD and rFactor2 Server\nInstall and/or Update\nProcess Completed" + result.stdout, wraplength=280, fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280, fg="red")

def run_com9(): #Install WorkShop Content
    os.chdir(SteamCMD)
    if myOS=="Windows":
        command = (f"steamcmd.exe +login anonymous +workshop_download_item 365960 {pasted} +quit") # Replace with your desired command ref: 1515644900
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    else:
        command = (f"wine steamcmd.exe +login anonymous +workshop_download_item 365960 {pasted} +quit") # Replace with your desired command ref: 1515644900
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output_label.config(text="Worshop {pasted} Download Completed" + result.stdout, wraplength=280, fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280, fg="red")

def run_com10(): #MOVE workshop content to RF2 packages folder -  *if you want copy instead of move change shutil.move to shutil.copy in move_files() function
    command = move_files(src_dir, dest_dir) # Replace with your desired command
    #result = (command, shell=True)

def run_com11():#Run ModMgr
    os.chdir(os.path.expanduser("~"))
    os.chdir("Racing/rfactor2-dedicated/Bin64")
    #print(os.getcwd())
    if myOS=="Windows":
        command = "ModMgr"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    else:
        command = "wine ModMgr"  # Mod Manager
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output_label.config(text="Mod Manager Closed", wraplength=280, fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280, fg="red")

def run_com12():# Run MAS2 Utility
    os.chdir(os.path.expanduser("~"))
    os.chdir("Racing/rfactor2-dedicated/Support/Tools")
    #button_num[11].config(text="Run", fg="Green")
    if myOS=="Windows":
        command = "MAS2"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    else:
        command = "wine MAS2"
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output_label.config(text="MAS2 Utility Closee", wraplength=280, fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280, fg="red")

def run_com13():# Run RF2 Server
    os.chdir(os.path.expanduser("~"))
    os.chdir("Racing/rfactor2-dedicated/Bin64")
    #button_num[12].config(text=" ON ", fg="Green")
    #print(os.getcwd())
    # WINE or Windows CMD command is: "rFactor2 Dedicated" +path=".."
    # Linux sees extra space as delimiting aka \ Dedicated
    if myOS=="Windows":
        command = '"rFactor2 Dedicated" +path=\"..\"'  # RF2 Server
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    else:
        command = "wine rFactor2\ Dedicated +path=\"..\""  # RF2 Server
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
    if result.returncode == 0:
        output_label.config(text="rFactor2 Server Closed", wraplength=280, fg="green")
    else:
        output_label.grid(row=13, sticky="w")
        output_label.config(text="Error:\n" + result.stderr, wraplength=280, fg="red")

# Create a Tkinter window
window = tk.Tk()
window.geometry("720x720")
window.title("RF2 Server Helper")

# Define labels and buttons and used \ for readability
labels = ["Check AMD64 Architecture", "Check i368 Foreign Architecture", "Add i386 Architecture",\
          "Check WINE Status", "** Configure WINE **", "Install WINE & WinBind(distro version)",\
          "Fix Windows sShortDate", "Install/Update RF2 Server",\
          "Download RF2 Content", "Transfer Content To RF2 Server", "Mod Manager", "MAS2 Utility", "START RF2 SERVER"]
buttons = ["Run", "Run", "Run", "Run", "Run", "Run", "Run", "Run", "Run","Run", "Run", "Run", "Run"]
label_num=[]
button_num=[]
coms=[run_com1,run_com2,run_com3,run_com4,run_com5,run_com6,run_com7,run_com8,run_com9,run_com10, run_com11,run_com12,run_com13]

# Iterate over the labels and buttons - *I may change button to create button numbers for easy button text.config
for i in range(len(labels)):
    # Create a Label and Button widgets for each and put them in a list index for future referencing with .config
    label_num.append(i)
    button_num.append(i)
    label_num[i] = tk.Label(window, text=labels[i])
    button_num[i] = tk.Button(window, text=buttons[i], activebackground="Indianred2", command=coms[i])
    # Create OutPut Label
    output_label = tk.Label(window, text="\n")
    # Use grid layout manager to align widgets in rows and columns
    label_num[i].grid(row=i, column=0, padx=4, pady=4, sticky="w")
    button_num[i].grid(row=i, column=1, padx=4, pady=4)
    output_label.grid()

#mytip2 =Hovertip(button_num[2], "Sudo required\nTerminal Expected")
mytip2 =Hovertip(button_num[2], "NOT Required if amd64 and i386 = OK\nSudo required for this command\nTerminal Expected")
mytip3 =Hovertip(button_num[3], "Manual Check -Version")
mytip4 =Hovertip(button_num[4], "\t**Configure\n-Windows 10\n-Graphics Tap\n-Screen Resolution=120dpi")
mytip7 =Hovertip(button_num[7], "--rFactor2 Server Helper\n--Instructions (In This Order)\nInstall/Update Server\nDownload Content\nTranser to Server\nMod Manager to Install Content\nMAS2(Package,Install,Done)\nStart Server\n")
mytip12 =Hovertip(button_num[12], "Force/Wait Message is expected\nBe Patient It Goes Away\nWhen Closing The Server\nWait for Server Closed Message")

#rFactor2 Button,Color and Font Settings.
rf2bg="light sky blue"
rf2font=("MATHJAX+MATH", "12", "italic")
rf2fg="red"
button_num[7].config(bg=rf2bg)
button_num[8].config(bg=rf2bg)
button_num[9].config(bg=rf2bg)
button_num[10].config(bg=rf2bg)
button_num[11].config(bg=rf2bg)
button_num[12].config(bg=rf2bg)
label_num[7].config(bg=rf2bg, fg=rf2fg, font=rf2font)
label_num[8].config(bg=rf2bg, fg=rf2fg, font=rf2font)
label_num[9].config(bg=rf2bg, fg=rf2fg, font=rf2font)
label_num[10].config(bg=rf2bg, fg=rf2fg, font=rf2font)
label_num[11].config(bg=rf2bg, fg=rf2fg, font=rf2font)
label_num[12].config(bg=rf2bg, fg=rf2fg, font=rf2font)


# GET steam workshop ID with Steam Workshop URL and extracting ID for content downloads.
def paste_highlighted_text(event):
    try:
        global pasted
        text = window.clipboard_get()
        text = text.split('=', 1)[1].strip()#strip everything but ID
        text = text.split('&', 1)[0].strip()
        print(text)
        pasted = text
        entry.insert(tk.END, text)
    except tk.TclError:
        pass  # Clipboard is empty
    
entry=tk.Entry(window, bg=rf2bg,fg=rf2fg, font=rf2font)
entry.insert(0, "WorkShop ID")
entry.grid(row=8, column=2, sticky="w")

mytip1 =Hovertip(entry, "EASY INSTRUCTIONS\nCopy-Paste-Run-Run\n1-(Copy)-(FULL) Workshop URL\n2-(Paste)-Right Click to Auto Paste\n3-(Run) \
(Download RF2 Content)\n4-(Run)-Transfer Content To RF2 Server\n\n Full Steam WorkShop URLs are OK\n\
 NOTE: Remove Entry Before Paste\n Hint: Triple click, then backspace\n or manually del etc.")
entry.bind("<Button-3>", paste_highlighted_text)  # Right-click to paste

# To Move Downloaded Workshop files from workshop /365960 to RF2 Packages 
src_dir = "Racing/SteamCMD/steamapps/workshop/content/365960"
dest_dir = "Racing/rfactor2-dedicated/Packages"
def move_files(src_dir, dest_dir):
    os.chdir(os.path.expanduser("~"))
    """Moves all regular files from src_dir and its subdirectories to dest_dir."""

    for root, dirs, files in os.walk(src_dir):
        for file in files:
            src_path = os.path.join(root, file)
            dest_path = os.path.join(dest_dir, file)
            print("---Moving Files---",file)
            # Check if it's a regular file
            if os.path.isfile(src_path):
                shutil.move(src_path, dest_path) # can use shutil.copy

    # print updated file lists from both directories. need to change to output_label for reference
    print("\n\tWorkShop/Content Folders\n     Should Show Empty Folders Only")
    
    for i in os.listdir(src_dir):
        print(i)

    print("\n\tPackage Files List-(Current)")
    list_label=""
    for i in os.listdir(dest_dir):
        print(i)
        list_label += '\n' + str(i)
    #create button numbers to reference button for hovertip addition   
    #? output_label.config(text=f"Package Files\n{list_label}").grid(stick="w")


#move_files(src_dir, dest_dir)
if myOS=="Linux":
    run_com1()
    run_com2()
# Start the Tkinter event loop
window.mainloop()
