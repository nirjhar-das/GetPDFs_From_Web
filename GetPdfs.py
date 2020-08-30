from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
import os
from tkinter import ttk
import tkinter
from tkinter import *
from tkinter import messagebox

def KeyWordsIn(compulsory_list, year_list, choice_list, text):
    ret_list = []
    for word in compulsory_list:
        if compulsory_list[0] == 'All' :
            ret_list.append(text[:-4])
            return True, True, True, ret_list
        elif word in text :
            ret_list.append(word)
        else :
            return False, False, False, ret_list
    flag_year = False
    for year in year_list :
        if year in text :
            flag_year = True
            break
    if not flag_year :
        return True, False, False, ret_list
    flag = False
    for word in choice_list :
        if word in text :
            ret_list.append(word)
            flag = True
    
    return True, flag_year, flag, ret_list

def NamePDFs(word_list, i) :
    name = ''
    for word in word_list :
        name = name + word + '-'
    name = name+ str(i) + '.pdf'
    return name

def MoveToFolder(list_of_folders, current_Folder) :
    for root, _, files in os.walk(current_Folder):
        for fileName in files:
            for folder in list_of_folders :
                if folder in fileName :
                    newFile = os.path.join(os.path.dirname(current_Folder), folder, fileName)
                    currFile = os.path.join(root, fileName)
                    os.rename(currFile, newFile)
                    break
    return

def getParams():
    params = {}
    print('Enter the website address from where to download.')
    print('Make sure that you input the exact website where you can see the download links.')
    print('Also make sure that the whole link is input including \"https\" etc.')
    print('A good way is to just copy the link directly from your browser.')
    params['url'] = input('Enter the address of the website from where to download')
    words = input('Enter compulsory keywords separated by space: ').split()
    params['comp_lis'] = words
    if input('Want to enter years? Y/N') == 'Y' :
        words = input('Enter optional keywords like Year separated by space: ').split()
        params['year_lis'] = words
    else :
        params['year_lis'] = []
    if input('Want to enter choice words? Y/N') == 'Y' :
        params['choice_lis'] = input('Enter choice words separated by space: ').split()
    else :
        params['choice_lis'] = []
    params['downPath'] = os.path.join(os.getcwd(), 'Downloads')
    if not os.path.isdir(params['downPath']):
        os.mkdir(params['downPath'])
    print('Please enter names of folders e.g. by years: 2018, 2019 etc. or by subject: History, Literature etc. or both')
    print('Note: If you are using both year and choice word, make sure the format is like:- \"2019-Literature\"')
    print('Please make sure that the names of folders are from the year list or choice list')
    print('In case you have not entered either, this step will not work in grouping files! Sorry!')
    params['folder_lis'] = input('Enter folder names: ').split()
    for folder in params['folder_lis'] :
        os.mkdir(os.path.join(os.getcwd(), folder))
    
    params['wait'] = int(input('Lastly, enter how many seconds you want to wait for every file to get downloaded. If your internet speed is low, set this to about 240 to 300'))

    return params

'''def downloadWait(params) :
    flag, sec = True, 0
    while flag and sec < params['wait'] :
        for name in os.listdir(params['downPath']):
            if name.endswith('.crdownload') :
                flag = True
                sleep(10)
                sec = sec + 10
            else :
                flag = False
    return'''

def getPdfs(params, progress, succ, flist, root) :

    options = webdriver.ChromeOptions()
    profile = {"download.default_directory": params['downPath'] ,
    "download.prompt_for_download": False,
    "download.directory_upgrade": True,
    "plugins.always_open_pdf_externally": True}
    options.add_experimental_option("prefs", profile)
    
    driver = webdriver.Chrome(os.path.join(os.getcwd(), 'chromedriver.exe'), options=options)
    driver.get(params['url'])
    elems = driver.find_elements_by_tag_name('a')
    files = []
    s, c = 0, 0
    final_elems = []
    for elem in elems:
        href = elem.get_attribute('href')
        if href is not None and href.endswith('.pdf') :
            s = s + 1
            final_elems.append(elem)
    i = 0
    with open('Serial_Number.txt', 'r') as f :
        i = int(f.readline())
    for elem in final_elems:
        href = elem.get_attribute('href')
        txt = elem.text
        comp_flag, year_flag, choice_flag, ret_lis = KeyWordsIn(params['comp_lis'], params['year_lis'], params['choice_lis'], txt)
        if comp_flag :
            if (year_flag or len(params['year_lis']) == 0) and (choice_flag or len(params['choice_lis']) == 0):
                fileName = NamePDFs(ret_lis, i)
                i = i + 1
                try :
                    driver.get(href)
                except Exception:
                    flist.insert('', 'end',values= (txt, href))
                    c = c + 1
                    progress['value'] = int((c/s)*100)
                    root.update_idletasks()
                    continue
                sleep(5)
                flag, sec, nm = True, 0, ''
                while flag and (sec < params['wait'] or params['wait'] < 0) :
                    fileList = sorted([os.path.join(params['downPath'], i) for i in os.listdir(params['downPath'])], key= os.path.getmtime)
                    name = fileList[-1]
                    if name.endswith('.crdownload') :
                        flag = True
                        sleep(10)
                        sec = sec + 10
                        nm = name
                    else :
                        flag = False
                if sec > params['wait'] :
                    os.remove(os.path.join(params['downPath'], nm))
                    flist.insert('', 'end', values= (txt, href))
                    continue
                fileList = sorted([os.path.join(params['downPath'], i) for i in os.listdir(params['downPath'])], key= os.path.getmtime)
                path_old = ''
                try:
                    path_old = os.path.join(params['downPath'], os.path.basename(fileList[-1]))
                except Exception:
                    path_old = ''
                path_new = os.path.join(params['downPath'], fileName)
                files.append((path_old, path_new))
                c = c + 1
                progress['value'] = int((c/s)*100)
                succ.insert("",'end', values=(txt, fileName, href))
                root.update_idletasks()
    progress['value'] = 100
    root.update_idletasks()
    driver.close()
    with open('Serial_Number.txt', 'w') as f:
        f.write(str(i))
    for tup in files :
        os.rename(tup[0], tup[1])
    MoveToFolder(params['folder_lis'], params['downPath'])
    messagebox.showinfo('Notification', 'Process Completed', parent=root)
    root.update_idletasks()
    return

'''
if __name__ == "__main__":
    
    params = getParams()
    getPdfs(params)
    print('Done!')'''