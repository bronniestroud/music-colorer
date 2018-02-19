from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import musicColorer
from music21 import converter
from music21.analysis import AnalysisException
import os
from tkinter import filedialog
from tkinter import colorchooser
from music21 import musicxml


root = Tk()
root.title("MusicColorer 1.0")
root.resizable(width=False, height=False)

img = PhotoImage(file='trill-opaque.gif')
root.tk.call('wm', 'iconphoto', root._w, img)


def run():
    try:

        runButton.configure(state=DISABLED)
        runVar.set("Working...")

        if not os.path.isfile(inPath.get()):
            raise FileNotFoundError
        if not os.path.isdir(outPath.get()):
            raise NotADirectoryError


        colorString = packageColors()
        print("ColorString: ", colorString, "          InPath: ",  inPath.get(), "          outPath: ", outPath.get())

        inputScore = converter.parse(inPath.get())
        colorerArgs = [inputScore, colorString]
        colorer = musicColorer.MusicColorer(colorerArgs)

        messagebox.showinfo(title="Ready", message="Initialization complete, Press OK to start.")
        finalScore = colorer.run()

        fileName = os.path.basename(inPath.get())
        fileNameNoExt = os.path.splitext(fileName)[0]
        outFileName = outPath.get() + "/" + fileNameNoExt + " (Recolored)"

        print("About to print score!")
        print(outFileName + '.xml')
        finalScore.write('musicxml', outFileName + '.xml')

        messagebox.showinfo(title="Operation Complete!", message="File was saved at: " + outFileName + '.xml')
        runButton.configure(state=NORMAL)
        runVar.set("Run!")

    except (IndexError):
        messagebox.showerror(title="Error!", message="Something went wrong...")
    except (NotADirectoryError):
        messagebox.showerror(title="Error!", message="Directory not valid!")
    except (FileNotFoundError):
        messagebox.showerror(title="Error!", message="File not found!")
    except (converter.ConverterException, converter.ConverterFileException):
        messagebox.showerror(title="Error!", message="Invalid file or format!")
    except (musicxml.xmlToM21.MusicXMLImportException):
        messagebox.showerror(title="Error!", message="File was not a valid musicXML file!")
    except (AnalysisException):
        messagebox.showerror(title="Error!", message="An error occurred analyzing the score...")

    runButton.configure(state=NORMAL)
    runVar.set("Run!")


def packageColors():
    colorString = str(color1Set[1]) + "," + str(color2Set[1]) + "," + str(color3Set[1]) + "," + str(color4Set[1]) + ","\
        + str(color5Set[1]) + "," + str(color6Set[1]) + "," + str(color7Set[1])
    colorString = str(colorString)
    return colorString


def load_inPath():
    filename = filedialog.askopenfilename(defaultextension=".xml", filetypes=[("musicXML", ".xml"), ("musicXML (compressed)", ".mxl"), ("HumDrum", ".kern"), ("ABC", ".abc"), ("MIDI", ".midi"), ("LilyPond", ".ly"), ("MuseData", ".md")])
    inPath.set(filename)


def load_outPath():
    filename = filedialog.askdirectory()
    outPath.set(filename)


def set_color1():
    global color1Set
    color1Set = colorchooser.askcolor()
    color1Label.configure(background=color1Set[1])
    return


def set_color2():
    global color2Set
    color2Set = colorchooser.askcolor()
    color2Label.configure(background=color2Set[1])
    return


def set_color3():
    global color3Set
    color3Set = colorchooser.askcolor()
    color3Label.configure(background=color3Set[1])
    return


def set_color4():
    global color4Set
    color4Set = colorchooser.askcolor()
    color4Label.configure(background=color4Set[1])
    return


def set_color5():
    global color5Set
    color5Set = colorchooser.askcolor()
    color5Label.configure(background=color5Set[1])
    return


def set_color6():
    global color6Set
    color6Set = colorchooser.askcolor()
    color6Label.configure(background=color6Set[1])
    return


def set_color7():
    global color7Set
    color7Set = colorchooser.askcolor()
    color7Label.configure(background=color7Set[1])
    return


# -------------------- Top Frame -- Paths Input

framePaths = ttk.Frame(root, padding="3 3 12 12")
framePaths.grid(column=0, row=0, sticky=(N, W, E),padx=5, pady=5)
framePaths.columnconfigure(0, weight=1)
framePaths.rowconfigure(0, weight=1)

inPath = StringVar()
outPath = StringVar()

inPath_entry = ttk.Entry(framePaths, width=80, textvariable=inPath)
inPath_entry.grid(column=2, row=1, sticky=(W, E))

outPath_entry = ttk.Entry(framePaths, width=80, textvariable=outPath)
outPath_entry.grid(column=2, row=2, sticky=(W, E))

ttk.Button(framePaths, text="...", command=load_inPath).grid(column=3, row=1, sticky=W)
ttk.Button(framePaths, text="...", command=load_outPath).grid(column=3, row=2, sticky=W)

ttk.Label(framePaths, text="Select File: ").grid(column=1, row=1, sticky=W)
ttk.Label(framePaths, text="Save To: ").grid(column=1, row=2, sticky=E)

for child in framePaths.winfo_children():
    child.grid_configure(padx=5, pady=5)

# ------------------------------ Lower Frame -- Colors

color1Set = [(000, 000, 000), '#000000']  # Default color is all black-- so no change.
color2Set = [(000, 000, 000), '#000000']
color3Set = [(000, 000, 000), '#000000']
color4Set = [(000, 000, 000), '#000000']
color5Set = [(000, 000, 000), '#000000']
color6Set = [(000, 000, 000), '#000000']
color7Set = [(000, 000, 000), '#000000']

frameColors = ttk.Frame(root, padding="3 3 12 12")
frameColors.grid(column=0, row=1, sticky=(N, S, W, E), padx=5, pady=5)
frameColors.columnconfigure(0, weight=1)
frameColors.rowconfigure(1, weight=1)

# Scale-degree labels
ttk.Label(frameColors, text='Scale Degree: ', anchor=CENTER, width=14).grid(row=1, column=0, sticky=N)
ttk.Label(frameColors, text='1: Tonic', anchor=CENTER, width=12).grid(row=1, column=1, sticky=N)
ttk.Label(frameColors, text='2: Supertonic', anchor=CENTER, width=12).grid(row=1, column=2, sticky=N)
ttk.Label(frameColors, text='3: Mediant', anchor=CENTER, width=10).grid(row=1, column=3, sticky=N)
ttk.Label(frameColors, text='4: Subdominant', anchor=CENTER, width=14).grid(row=1, column=4, sticky=N)
ttk.Label(frameColors, text='5: Dominant', anchor=CENTER, width=11).grid(row=1, column=5, sticky=N)
ttk.Label(frameColors, text='6: Submediant', anchor=CENTER, width=13).grid(row=1, column=6, sticky=N)
ttk.Label(frameColors, text='7: Subtonic/LT', anchor=CENTER, width=13).grid(row=1, column=7, sticky=N)

# Colored rectangel labels. Must save reference to each so the color can be changed once something different is chosen
color1Label = ttk.Label(frameColors, background=color1Set[1], width=12)
color1Label.grid(row=2, column=1, sticky=N)
color2Label = ttk.Label(frameColors, background=color2Set[1], width=12)
color2Label.grid(row=2, column=2, sticky=N)
color3Label = ttk.Label(frameColors, background=color3Set[1], width=12)
color3Label.grid(row=2, column=3, sticky=N)
color4Label = ttk.Label(frameColors, background=color4Set[1], width=12)
color4Label.grid(row=2, column=4, sticky=N)
color5Label = ttk.Label(frameColors, background=color5Set[1], width=12)
color5Label.grid(row=2, column=5, sticky=N)
color6Label = ttk.Label(frameColors, background=color6Set[1], width=12)
color6Label.grid(row=2, column=6, sticky=N)
color7Label = ttk.Label(frameColors, background=color7Set[1], width=12)
color7Label.grid(row=2, column=7, sticky=N)

# Buttons to select colors
ttk.Button(frameColors, text='Select color...', command=set_color1).grid(column=1, row=3, sticky=S)
ttk.Button(frameColors, text='Select color...', command=set_color2).grid(column=2, row=3, sticky=S)
ttk.Button(frameColors, text='Select color...', command=set_color3).grid(column=3, row=3, sticky=S)
ttk.Button(frameColors, text='Select color...', command=set_color4).grid(column=4, row=3, sticky=S)
ttk.Button(frameColors, text='Select color...', command=set_color5).grid(column=5, row=3, sticky=S)
ttk.Button(frameColors, text='Select color...', command=set_color6).grid(column=6, row=3, sticky=S)
ttk.Button(frameColors, text='Select color...', command=set_color7).grid(column=7, row=3, sticky=S)

# -------------------------------------- Finalize root and add root-level button

runVar = StringVar()
runVar.set("Run!")

runButton = ttk.Button(root, textvar=runVar, command=run, state=NORMAL)
runButton.grid(sticky=(S, N, W, E),column=1, row=0, rowspan=2, padx=15, pady=15)

#-------------------------------------------Menu

inPath_entry.focus()

root.bind('<Return>', run)

root.mainloop()