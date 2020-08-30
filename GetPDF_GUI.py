import tkinter
from tkinter import *
from tkinter import filedialog, ttk, messagebox
from time import sleep
import GetPdfs as gp
import os
import threading


root = Tk()
root.title('Get PDFs')
photo = PhotoImage(file= os.path.join(os.getcwd(), 'TFIL-final.png'))
root.iconphoto(True, photo)

mainframe = ttk.Frame(root, padding= "5 5 5 5")
mainframe.grid(column= 0, row= 0, sticky= (N, W, E, S))
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

URL = StringVar()
Compulsory = StringVar(value='All')
Years = StringVar()
Choice = StringVar()
folderPath = StringVar()
folderNames = StringVar()
Wait = StringVar(value='120')

def go():
    params = {}
    params['url'] = URL.get()
    params['comp_lis'] = Compulsory.get().split()
    params['year_lis'] = Years.get().split()
    params['choice_lis'] = Choice.get().split()
    params['mainPath'] = folderPath.get().replace("/", "\\")
    params['downPath'] = os.path.join(params['mainPath'], 'Downloads')
    params['folder_lis'] = folderNames.get().split()
    params['wait'] = int(Wait.get())

    if params['url'] == '' :
        messagebox.showerror('Enter URL', message='Please Enter Website address')
        return
    if len(params['comp_lis']) == 0 :
        messagebox.showerror("Compulsory Words", message='Please Enter Compulsory List of Words')
        return
    if params['mainPath'] == '' :
        messagebox.showerror("Download Folder Path", message='Please Select Download Folder')
        return
    if not os.path.isdir(params['downPath']):
        os.mkdir(params['downPath'])
    if len(params['folder_lis']) == 0 :
        m = messagebox.askyesno("Names of Folders", message='Names of folders not given. Files won\'t be grouped after download.\nDo you want to continue?')
        if m == 'no' :
            return
    else :
        for fold in params['folder_lis'] :
            path = os.path.join(params['mainPath'], fold)
            if not os.path.isdir(path) :
                os.mkdir(path)
    run_flag = True
    new_root = Toplevel(root)
    new_root.title("Download Process")
    sideFrame = ttk.Frame(new_root, padding= "5 5 5 5")
    sideFrame.grid(column= 0, row= 0, sticky= (N, W, E, S))
    new_root.columnconfigure(0, weight=1)
    new_root.rowconfigure(0, weight=1)
    ttk.Label(sideFrame, text='Progress').grid(column=1, row=1, sticky=E)
    progress = ttk.Progressbar(sideFrame, orient= HORIZONTAL, length= 600, mode='determinate')
    progress.grid(column=2, columnspan=2, row=1, sticky=(W,E))
    succ = ttk.Treeview(sideFrame, selectmode='browse', height=10)
    succ['columns'] = ("1", "2", "3")
    succ['show'] = "headings"
    succ.column("1", width = 20, anchor ='c') 
    succ.column("2", width = 20, anchor ='c')
    succ.column("3", width= 100, anchor='w') 
    succ.heading("1", text ="Description") 
    succ.heading("2", text ="Name After Download")
    succ.heading("3", text ="Link for Download") 
    fail = ttk.Treeview(sideFrame, height= 10, selectmode='browse')
    fail['show'] = 'headings'
    fail['columns'] = ('1', '2')
    fail.column('1', width= 40, anchor= 'c')
    fail.column('2', width= 100, anchor='w')
    fail.heading('1', text= 'Description')
    fail.heading('2', text= 'Link for Download')
    scroll1y = Scrollbar(sideFrame)
    scroll1y.configure(command= succ.yview)
    succ.configure(yscrollcommand=scroll1y.set)
    scroll2y = Scrollbar(sideFrame)
    scroll2y.configure(command= fail.yview)
    fail.configure(yscrollcommand=scroll2y.set)
    ttk.Label(sideFrame, text='Successful Files').grid(column=1, row=2, sticky=E)
    ttk.Label(sideFrame, text='Failed Links and Files').grid(column=1, row=3, sticky=E)
    succ.grid(column=2, columnspan=2, row=2, sticky=(E, W))
    fail.grid(column=2, columnspan=2, row=3, sticky=(E,W))
    scroll1y.grid(column=4, row=2, sticky=(N, S, W))
    scroll2y.grid(column=4, row=3, sticky=(N, S, W))
    ttk.Button(sideFrame, text='Close', command= new_root.destroy).grid(column=3, columnspan=2, row=6, sticky=(S,E))
    for child in sideFrame.winfo_children():
        child.grid_configure(padx=5, pady=5)
    if run_flag:
        threading.Thread(target=gp.getPdfs, args=(params, progress, succ, fail, new_root)).start()
        run_flag = False
    new_root.mainloop()



def get_folder():
    folderPath.set(filedialog.askdirectory())
    
    

url_entry = ttk.Entry(mainframe, width= 100, textvariable= URL)
url_entry.grid(column=2, row=1, sticky=E)

compul_entry = ttk.Entry(mainframe, width= 100, textvariable=Compulsory)
compul_entry.grid(column=2, row=2, sticky=E)

years_entry = ttk.Entry(mainframe, width= 100, textvariable= Years)
years_entry.grid(column=2, row=3, sticky=E)

choice_entry = ttk.Entry(mainframe, width= 100, textvariable= Choice)
choice_entry.grid(column=2, row=4, sticky=E)

folder_entry = ttk.Entry(mainframe, width= 100, textvariable= folderNames)
folder_entry.grid(column=2, row=5, sticky=E)

wait_entry = ttk.Entry(mainframe, width=20, textvariable=Wait)
wait_entry.grid(column=3, row=2, sticky=(N, E))

ttk.Label(mainframe, text= 'Web Adrress :').grid(column=1, row=1, sticky=W)
ttk.Label(mainframe, text= 'Compulsory Words :').grid(column=1, row=2, sticky=W)
ttk.Label(mainframe, text= 'Years/Numeric :').grid(column=1, row=3, sticky=W)
ttk.Label(mainframe, text= 'Choice Words (e.g. Subject) :').grid(column=1, row=4, sticky=W)
ttk.Label(mainframe, text= 'Folder Names for grouping :').grid(column=1, row=5, sticky=W)
ttk.Label(mainframe, textvariable= folderPath).grid(column=2, row=6, sticky=W)
ttk.Label(mainframe, text='Wait for each download \n        (in seconds)').grid(column=3, row=1, sticky=(S, E))

ttk.Button(mainframe, text= "Get PDFs", command= go).grid(column=3, row=5, sticky=E)
ttk.Button(mainframe, text='Close', command=root.destroy).grid(column=3, row=6, sticky=E)
ttk.Button(mainframe, text= "Select Folder", command= get_folder).grid(column=1, row=6, sticky=W)


for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

url_entry.focus()

root.mainloop()

