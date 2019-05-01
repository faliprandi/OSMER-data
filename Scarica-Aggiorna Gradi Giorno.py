# -*- coding: utf-8 -*-
"""
Created on Sat Apr 13 11:08:52 209

@author: Francesco

This script downloads data from the OSMER site for a given set of stations
and in a given range of months/years.
It is also possible to update an already existing file.
"""

import os
import logging
import datetime as dt
import requests
from bs4 import BeautifulSoup
import pandas as pd
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as tmb
# from numpy import nan as Nan

# CLASSES

# This is the main GUI
class OSMERGUI():
    def __init__(self,win):
        self.win = win
        win.title("Selezione dati input")

# We pass to the object the stored values        
        self.showed = showed
        self.lbox = tk.Listbox(win,
                               listvariable=showed,
                               height=8,
                               width=30,
                               selectmode=tk.EXTENDED)
        self.lbox.configure(exportselection=False)
        for i in showed:
            self.lbox.insert(tk.END, i)
            self.lbox.grid(column=0,
                           rowspan=6,
                           padx=8,
                           pady=16)

# Labels
        ttk.Label(win, text="Mese iniziale").grid(column = 1,
                                                  row = 0,
                                                  padx = 4,
                                                  pady = 4,
                                                  sticky = "W")
        ttk.Label(win, text="Anno iniziale").grid(column = 3,
                                                  row = 0,
                                                  padx = 4,
                                                  pady = 4,
                                                  sticky = "E")
        ttk.Label(win, text="Mese finale").grid(column = 1,
                                                row = 3,
                                                padx = 4,
                                                pady = 4,
                                                sticky = "W")
        ttk.Label(win, text="Anno finale").grid(column = 3,
                                                row = 3,
                                                padx = 4,
                                                pady = 4,
                                                sticky = "E")

# Variables for comboboxes
        self.text1 = tk.StringVar()
        self.text2 = tk.StringVar()
        self.text3 = tk.StringVar()
        self.text4 = tk.StringVar()

#Comboboxes descriptions
        self.start_month_chosen = ttk.Combobox(win,
                                               width = 8,
                                               textvariable = self.text1,
                                               state = 'readonly')
        self.start_month_chosen["values"] = months
        self.start_month_chosen.grid(column = 1,
                                     row = 1,
                                     padx = 4,
                                     pady = 4,
                                     sticky = "W")
        self.start_month_chosen.current(0)

        self.start_year_chosen = ttk.Combobox(win,
                                              width = 8,
                                              textvariable = self.text2,
                                              state = 'readonly')
        self.start_year_chosen["values"] = years
        self.start_year_chosen.grid(column = 3,
                                    row = 1,
                                    padx = 4,
                                    pady = 4,
                                    sticky = "E")
        self.start_year_chosen.current(0)
    
        self.end_month_chosen = ttk.Combobox(win,
                                             width = 8,
                                             textvariable = self.text3,
                                             state = 'readonly')
        self.end_month_chosen["values"] = months
        self.end_month_chosen.grid(column = 1,
                                   row = 4,
                                   padx = 4,
                                   pady = 4,
                                   sticky = "W")
        self.end_month_chosen.current(0)

        self.end_year_chosen = ttk.Combobox(win,
                                            width = 8,
                                            textvariable = self.text4,
                                            state = 'readonly')
        self.end_year_chosen["values"] = years
        self.end_year_chosen.grid(column = 3,
                                  row = 4,
                                  padx = 4,
                                  pady = 4,
                                  sticky = "E")
        self.end_year_chosen.current(0)

# Variable for checkbox
        self.GGvar = tk.BooleanVar()
        #self.GGvar.set('false')
        self.GGcheckbox = ttk.Checkbutton(win,
                                          text = "Calcolo Gradi Giorno",
                                          variable = self.GGvar,
                                          onvalue = 'true',
                                          offvalue = 'false')
        self.GGcheckbox.grid(column = 2,
                             row = 5,
                             sticky = "E")

# Definition of action commands
        self.action = ttk.Button(win,
                                 text="Scarica",
                                 command = self.click_me1)
        self.action.grid(column = 1,
                         row = 7,
                         padx = 4,
                         pady = 8,
                         sticky = "W")
    
        self.action = ttk.Button(win,
                                 text="Aggiorna",
                                 command = self.click_me2)
        self.action.grid(column = 2,
                         row = 7)
    
        self.action = ttk.Button(win,
                                 text="Annulla",
                                 command = self.delete_me)
        self.action.grid(column = 3,
                         row = 7,
                         padx = 4,
                         pady = 8,
                         sticky = "E")
        
    def get_values(self):
        self.items = list(self.lbox.curselection())
        self.str_month = self.start_month_chosen.get()
        self.str_year = self.start_year_chosen.get()
        self.end_month = self.end_month_chosen.get()
        self.end_year = self.end_year_chosen.get()
        self.GGbool = self.GGvar.get()
    
    def click_me1(self):
        self.get_values()
        self.downloadflag = True
        self.win.destroy()
    
    def click_me2(self):
        self.get_values()
        self.downloadflag = False
        self.win.destroy()
        
    def delete_me(self):
        self.win.destroy()
        raise SystemExit()


# FUNCTIONS

# Function that returns calculated degree days
def degreedays(x):
    try:
        if x < 20:
            return round((20 - x),1)
        else:
            return 0
    except TypeError:
        print(x)
        return 0

# Function that returns both the list of stations as coded on the site and
# the list to be showed in the main window
def getlists(url1):
    stations = []
    showed = []
    r = requests.get(url1)
# Cookie must be saved for following sessions
    cookie = r.cookies
    list_page = BeautifulSoup(r.content, 'html5lib')
    names = list_page.find('select',{'id':'stazione'})
    options = names.find_all('option')
    stations = [o.get('value') for o in options]
# We delete the first element as it is empty
    del stations[0]
# Stripping of extra characters    
    for i in range(0, len(stations)):
        full_string = stations[i]
        showed.append(full_string[full_string.find("@") +
                                  1:full_string.find("@", 5)])
    return(stations, showed, cookie)

# Function that exits if there are no stations selected
def checkstation(items):
    if not items:
        root = tk.Tk()
        root.withdraw()
        tmb.showwarning(title="Attenzione!",
                        message="Nessuna stazione selezionata, precedura annullata")
        raise SystemExit()

# Function that checks for congruent dates
def checkdates():
    if start > end:
        root = tk.Tk()
        root.withdraw()
        tmb.showwarning(title="Attenzione!",
                        message="La data iniziale deve precedere quella finale. \n Procedura terminata")
        raise SystemExit()

# Function that creates a list of dates
def datelist(start, end):
    temp_list = []
    panda_list = pd.date_range(start, end, freq='MS')
    for dates in panda_list:
        temp_list.append([dates.month, dates.year])
    return temp_list

# Function that checks for file existence and eventually renames files
def checkfiles(i):
    new_name = showed[i] + ".csv"
    old_name = "_old_" + showed[i] + ".csv"
    new_file = os.path.normpath(os.path.join(rel_path, new_name))
    old_file = os.path.normpath(os.path.join(rel_path, old_name))
    if os.path.isfile(new_file):
        if os.path.isfile(old_file):
            os.remove(old_file)
        os.rename(new_file, old_file)
    return(new_file, old_file)

# Function that checks for folder existence
def checkfolder():
    if not os.path.isdir(rel_path):
        root = tk.Tk()
        root.withdraw()
        tmb.showwarning(title="Attenzione!",
                        message="Non è presente la cartella Dati allo stesso livello dello script. \n Procedura terminata")
        raise SystemExit()

# Function that checks for missing days in each month
def checkdays(dataframe, month, year):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
# Checking against leap years
    if year % 4 == 0:
        days[1] = 29
    if len(dataframe) == 0:
        for i in range(days[month- 1]):
            dataframe = dataframe.append({'giorno*': i + 1}, ignore_index = True)
            dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
            dataframe.sort_values(by='giorno*', inplace = True)
            dataframe['giorno*'] = dataframe['giorno*'].astype(int)
            complete_dataframe = dataframe
    elif len(dataframe) < days[month - 1]:
# We miss some days, must loop over rows and insert them
# First we convert to int the column 'giorno*'
        dataframe['giorno*'] = dataframe['giorno*'].astype(int)
#        print(days[month])
        for i in range(days[month- 1]):
            if i == len(dataframe):
                dataframe = dataframe.append({'giorno*': i + 1}, ignore_index = True)
                dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
                dataframe.sort_values(by='giorno*', inplace = True)
                dataframe = dataframe.reset_index(drop = True)
#            print(dataframe.iloc[i, 0])
            if dataframe.iloc[i, 0] != i + 1:
# Must append a row
#                newrow = pd.Series.to_frame(pd.Series([i+1], 'giorno*'))
#                dataframe = dataframe.append(newrow, ignore_index=True)
#                dataframe = pd.concat([dataframe, newrow], axis = 0)
                dataframe = dataframe.append({'giorno*': i + 1}, ignore_index = True)
                dataframe = dataframe.apply(pd.to_numeric, errors='coerce')
                dataframe.sort_values(by='giorno*', inplace = True)
                dataframe = dataframe.reset_index(drop = True)
        dataframe['giorno*'] = dataframe['giorno*'].astype(int)
        complete_dataframe = dataframe
# Too many days!
    elif len(dataframe) > days[month - 1]:
        k = 0
        while k < days[month- 1]:
            if dataframe.iloc[k, 0] != k + 1:
                dataframe = dataframe.drop(dataframe.index[k])
                dataframe.sort_values(by='giorno*', inplace = True)
                dataframe = dataframe.reset_index(drop = True)
                dataframe['giorno*'] = dataframe['giorno*'].astype(int)
                complete_dataframe = dataframe
#                k = k - 1
            else:
                k = k + 1
    else:
        complete_dataframe = dataframe
    return(complete_dataframe)

# Function that retrieves data for each station
def getdata(pairs_list, encoded_station, cookie):
    list_datafrm = []

    for pair in pairs_list:
        run_month, run_year = pair
        print('Downloading', run_month, run_year)
# General form of data to be passed    
        data = {'a':str(run_year),
                'm':str(run_month),
                'g':'3',
                's':str(encoded_station),
                't':'H_3',
                'ln':'',
                'o':'visualizza',
                }
        r = requests.post(url2, data, cookies=cookie)
        html_page = r.text
        new_page = html_page.replace('\\', '')
        soup = BeautifulSoup(new_page, 'html5lib')
        scrapedtable = soup.find_all("table")[0]
        df = pd.read_html(str(scrapedtable))
        my_datafrm = df[0]
        
        complete_datafrm = checkdays(my_datafrm, run_month, run_year)
        complete_datafrm['Data'] = str(run_year) + '-' + str(
                run_month) + '-' + complete_datafrm['giorno*'].apply(str)
        pd.to_datetime(complete_datafrm['Data'])
        del complete_datafrm['giorno*']
        list_datafrm.append(complete_datafrm)

    master_datafrm = pd.concat(list_datafrm, ignore_index=True)

# Conversion of spurious strings to numeric
    master_datafrm['Temp. med°C'] = master_datafrm['Temp. med°C'].apply(
                            pd.to_numeric, errors='coerce')
# GG column is added only if the relative flag is set to true
    if GGflag:
        master_datafrm['GG'] = master_datafrm['Temp. med°C'].apply(degreedays)
    
    return(master_datafrm)

# GLOBAL VARIABLES

# Start year for combobox
start_year = 1991

# Current year
cur_year = dt.datetime.today().year

# Current month
cur_month = dt.datetime.today().month

# List of years for combobox (dynamic)
years = list(range(start_year, cur_year + 1))

# List of months (static)
months = list(range(1, 13))

# url of OSMER site
#url = "http://www.osmer.fvg.it/archivio.php?ln=&p=dati"
url1 = 'http://www.osmer.fvg.it/archivio.php?ln=&p=dati'
url2 = 'http://www.osmer.fvg.it/ajax/getStationData.php'

# Relative path for data files
# It is assumed to be one level below the script, in a directory named "Dati"
rel_path = os.path.normpath(os.path.join(os.path.dirname(__file__), 'Dati'))

if not os.path.exists(rel_path):
    root = tk.Tk()
    root.withdraw()
    tmb.showwarning(title="Attenzione!",
                    message="La cartella Dati non esiste.\n Procedura terminata")
    raise SystemExit()

# File for logging errors
err_file = 'error.txt'

# Logging settings
logging.basicConfig(filename=err_file,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.ERROR)


# Main script
# Let's retrieve the list of stations
stations, showed, cookie = getlists(url1)

# Creates the main window
root=tk.Tk()
my_gui=OSMERGUI(root)
root.mainloop()

# Main variables
items = my_gui.items
start_month = my_gui.str_month
start_year = my_gui.str_year
end_month = my_gui.end_month
end_year = my_gui.end_year
downloadflag = my_gui.downloadflag
GGflag = my_gui.GGbool

# Check if the list is empty and eventually exits
checkstation(items)

# We already know the starting date
start = dt.date(int(start_year), int(start_month), 1)

# If downloadflag = True we are dling historical data
# Set end data and check for congruent dates
if downloadflag:
# End date has already been retrieved
    end = dt.date(int(end_year), int(end_month), 1)
    checkdates()
# The end date for updating is previous month
# We don't want to download incomplete months
else:
    end = dt.date(int(cur_year), int(cur_month) - 1, 1)

# Now we know there is at least one station
for i in items:
    checkfiles(i)
    encoded_station = stations[i]
    new_file, old_file = checkfiles(i)
# Download of new stations
    if downloadflag:
# Create list of dates
        date_list = datelist(start, end)
        final_dataframe = getdata(date_list, encoded_station, cookie)
# Updating of existing stations
    else:
        if not os.path.isfile(old_file):
            root = tk.Tk()
            root.withdraw()
            tmb.showwarning(title="Attenzione!", message="Impossibile aggiornare. \n Procedura terminata")
            raise SystemExit()
        old_dataframe = pd.read_csv(old_file, encoding = "ISO-8859-1", 
                              decimal=',', sep = ';')
        bottom_line = old_dataframe.tail(1)
        last_update = pd.to_datetime(bottom_line.iloc[0]['Data'])
        last_update_month = last_update.month
        last_update_year = last_update.year
# We must increase the month by 1 (and check for december)
        if last_update_month == 12:
            start = dt.date(int(last_update_year) + 1, 1, 1)
        else:
            start = dt.date(int(last_update_year), int(last_update_month) + 1, 1)
        date_list = datelist(start, end)
        new_list = date_list[0:1 or None]
        
        if not new_list:
            root = tk.Tk()
            root.withdraw()
            tmb.showwarning(title="Attenzione!", message="Impossibile aggiornare. \n Procedura terminata")
            raise SystemExit()
        else:
            print('Success')
            pass
        new_dataframe = getdata(date_list, encoded_station, cookie)
        result_dataframe = [old_dataframe, new_dataframe]
        final_dataframe = pd.concat(result_dataframe)
        
    with open(new_file, 'wt') as f:
            final_dataframe.to_csv(f, sep = ';', index=False, decimal=',')