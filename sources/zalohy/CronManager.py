import tkinter as tk
from tkinter.font import Font
from tkinter import filedialog
import os
import re
from tkinter import messagebox  # Tkinter dialog boxes
from datetime import datetime, timedelta
import shutil
# Configuration text files utility
import configparser
# Keeps order of dictionary-keys
from collections import OrderedDict


class MainGui(tk.Frame):
    # Class inherited from tk.Frame
    def __init__(self, master=None):
        tk.Frame.__init__(self, master)

        # Working directory path setup (server is triggered from rc.local command line)
        #os.chdir('/home/pi/Documents/HTOB')

        # Create object to get configuration data from .ini file
        self.configp = configparser.ConfigParser()
        # To disable Configparser feature: capital keys are automatically changed to lower case
        self.configp.optionxform = str

        master.title("HTOB CRONTAB Manager")

        # Populate column/row structure
        for r in range(13):
            master.rowconfigure(r, weight=1, minsize=10)
        for c in range(7):
            master.columnconfigure(c, weight=1, minsize=100)

        # Fonts -central setup
        helv10 = Font(family='Helvetica', size=10, weight='normal')
        bold = Font(family='TkHeadingFont', size=9, weight='bold')
        giant = Font(family='TkHeadingFont', size=24, weight='bold')

        # Label variables inititation
        #total_cycles_var = tk.StringVar()
        #total_cycles_var.set(self.cycle_counter())
        # //////////////////////////////////////////////////////////////////////////////////
        # Show control buttons (Menu)
        tk.Button(master, text="Start HTOB", fg='#2f6725', font=helv10, command = self.cronStart).grid(row=14,column=0,sticky="ew")
        tk.Button(master, text="Stop HTOB", fg='#d90000', font=helv10, command = self.cronStop).grid(row=14,column=1,sticky="ew")
        tk.Button(master, text="Emergency Stop", bg='#d90000', fg='#ffffff', font=helv10, command = self.stopAC).grid(row=14,column=2,sticky="ew")
        tk.Button(master, text="Reset counters", font=helv10, command = self.resetCounter).grid(row=14,column=3,sticky="ew")
        tk.Button(master, text="Export Logs", font=helv10, command = self.exportLogs).grid(row=14,column=4,sticky="ew")
        # Quit HTOB Manager application
        tk.Button(master, text="Quit", font=helv10, command = self.closeWindows).grid(row=14,column=5,sticky="ew")
        # //////////////////////////////////////////////////////////////////////////////////
        # Left columns
        Frame1 = tk.Frame(master, bg="#dbe9c9",padx=10,pady=10)
        Frame1.grid(row=0,column=0, rowspan=13, columnspan=2, sticky="nsew")
        self.cycles_total_label = tk.Label(Frame1, height=1,bg="#dbe9c9",text="TOTAL CYCLES: ").grid(column=0, row=0, sticky="w")
        self.cycles_total = tk.Label(Frame1, height=1,bg="#dbe9c9",text="no counter")
        self.cycles_total.grid(column=1, row=0,sticky="e")
        self.cycles_elapsed_label = tk.Label(Frame1,height=1,bg="#dbe9c9",text="ELAPSED CYCLES: ").grid(column=0, row=1, sticky="w")
        self.cycles_elapsed = tk.Label(Frame1,height=1,bg="#dbe9c9",text="no counter")
        self.cycles_elapsed.grid(column=1, row=1,sticky = "e")
        self.cycles_remaining_label = tk.Label(Frame1,height=1,bg="#dbe9c9",text="REMAINING CYCLES: ").grid(column=0, row=2, sticky="w")
        self.cycles_remaining = tk.Label(Frame1,height=1,bg="#dbe9c9",text="no counter")
        self.cycles_remaining.grid(column=1, row=2,sticky = "e")
        self.start_test_label = tk.Label(Frame1, height=1, bg="#dbe9c9", text="START OF TEST: ").grid(column=0, row=3, sticky="w")
        self.start_test = tk.Entry(Frame1, justify="right")
        self.start_test.grid(column=1, row=3, sticky="w")
        self.reset_cycles_label = tk.Label(Frame1, height=1,bg="#dbe9c9", font=bold, text="RESET COUNTER VALUES").grid(column=0, row=4, sticky="ew")
        self.reset_cycles_total_label = tk.Label(Frame1,height=1,bg="#dbe9c9",text="NEW TOTAL CYCLES: ").grid(column=0, row=5, sticky="w")
        self.reset_cycles_total = tk.Entry(Frame1, justify="right")
        self.reset_cycles_total.grid(column=1, row=5,sticky = "e")
        self.reset_cycles_elapsed_label = tk.Label(Frame1,height=1,bg="#dbe9c9",text="NEW ELAPSED CYCLES: ").grid(column=0, row=6, sticky="w")
        self.reset_cycles_elapsed = tk.Entry(Frame1, justify="right")
        self.reset_cycles_elapsed.grid(column=1, row=6,sticky = "e")
        # Right columns
        self.cycles_total_days_label = tk.Label(Frame1, height=1, bg="#dbe9c9", text="DAYS/H M ").grid(column=2, row=0, sticky="w", padx=20)
        self.cycles_total_days = tk.Label(Frame1, height=1, bg="#dbe9c9", text="no counter")
        self.cycles_total_days.grid(column=3, row=0, sticky="e")
        self.cycles_elapsed_days_label = tk.Label(Frame1, height=1, bg="#dbe9c9", text="DAYS/H M ").grid(column=2, row=1, sticky="w", padx=20)
        self.cycles_elapsed_days = tk.Label(Frame1, height=1, bg="#dbe9c9", text="no counter")
        self.cycles_elapsed_days.grid(column=3, row=1, sticky="e")
        self.cycles_remaining_days_label = tk.Label(Frame1, height=1, bg="#dbe9c9", text="DAYS/H M ").grid(column=2, row=2, sticky="w", padx=20)
        self.cycles_remaining_days = tk.Label(Frame1, height=1, bg="#dbe9c9", text="no counter")
        self.cycles_remaining_days.grid(column=3, row=2, sticky="e")
        self.end_test_date_label = tk.Label(Frame1, height=1, bg="#dbe9c9", text="END OF TEST: ").grid(column=2, row=3, sticky="w", padx=20)
        self.end_test_date = tk.Label(Frame1, height=1, bg="#dbe9c9", text="no counter")
        self.end_test_date.grid(column=3, row=3, sticky="e")
        # //////////////////////////////////////////////////////////////////////////////////
        Frame2 = tk.Frame(master, bg="#727272", padx=10, pady=10)
        Frame2.grid(row=12, column=0, rowspan=2,columnspan=2, sticky="nsew")
        self.clock = tk.Label(Frame2,height=1,bg="#727272",fg="#ffffff",font=giant,padx=40, pady=30)
        self.clock.grid(column=0, row=0)
        self.cron_status_label = tk.Label(Frame2,bg="#727272",fg="#ffffff",text="TEST STATUS\n(updated each 5s): ").grid(column=0, row=1, sticky="w")
        self.cron_status = tk.Label(Frame2,bg="#727272",fg="#ffffff",text="no value available")
        self.cron_status.grid(column=1, row=1)
        # //////////////////////////////////////////////////////////////////////////////////
        Frame3 = tk.Frame(master, bg="#e6e6e6", padx=10, pady=10)
        Frame3.grid(row=0,column=2, rowspan=13, columnspan=5,sticky="nsew")
        self.logs_path_label = tk.Label(Frame3, height=1, bg="#e6e6e6", text="LOG FILES DIRECTORY: ")
        self.logs_path_label.grid(column=0, row=0, columnspan=3, sticky="w")
        self.logs_path = tk.Entry(Frame3, width=60, justify="left")
        self.logs_path.insert(0, os.path.join(os.path.abspath(os.path.dirname(__file__)), "log-data-backups"))
        self.logs_path.grid(column=0, row=1, columnspan=5, sticky="w")
        tk.Button(Frame3,text="Choose dir",command = self.chooseDirectory).grid(row=2,column=0,sticky="w")
        # Variacs block
        self.variacs_title = tk.Label(Frame3, height=1, font=bold, bg="#e6e6e6", text="AC VARIABLE TRANSFORMERS").grid(pady=10, column=0, row=3, columnspan=3, sticky="w")
        self.variac_ip_label = tk.Label(Frame3, height=1, bg="#e6e6e6", text="IP ADDRESS").grid(column=0, row=4, sticky="w")
        self.variac_required_volt_label = tk.Label(Frame3, height=1, bg="#e6e6e6", text="REQ.VOLTAGE(VAC)").grid(column=1, row=4, sticky="w")
        self.variac_L1_label = tk.Label(Frame3, height=1, bg="#e6e6e6", text="L1(VAC)").grid(column=2, row=4, sticky="w")
        self.variac_L2_label = tk.Label(Frame3, height=1, bg="#e6e6e6", text="L2(VAC)").grid(column=3, row=4, sticky="w")
        self.variac_L3_label = tk.Label(Frame3, height=1, bg="#e6e6e6", text="L3(VAC)").grid(column=4, row=4, sticky="w")
        # Variac 1
        self.variac1_ip = tk.Entry(Frame3, justify="right")
        self.variac1_ip.grid(column=0, row=5, sticky="w")
        self.variac1_request = tk.Entry(Frame3, justify="right")
        self.variac1_request.grid(column=1, row=5, sticky="w")
        self.variac1_L1_voltage = tk.Entry(Frame3, justify="right")
        self.variac1_L1_voltage.grid(column=2, row=5, sticky="w")
        self.variac1_L2_voltage = tk.Entry(Frame3, justify="right")
        self.variac1_L2_voltage.grid(column=3, row=5, sticky="w")
        self.variac1_L3_voltage = tk.Entry(Frame3, justify="right")
        self.variac1_L3_voltage.grid(column=4, row=5, sticky="w")
        # Variac 2
        self.variac2_ip = tk.Entry(Frame3, justify="right")
        self.variac2_ip.grid(column=0, row=6, sticky="w")
        self.variac2_request = tk.Entry(Frame3, justify="right")
        self.variac2_request.grid(column=1, row=6, sticky="w")
        self.variac2_L1_voltage = tk.Entry(Frame3, justify="right")
        self.variac2_L1_voltage.grid(column=2, row=6, sticky="w")
        self.variac2_L2_voltage = tk.Entry(Frame3, justify="right")
        self.variac2_L2_voltage.grid(column=3, row=6, sticky="w")
        self.variac2_L3_voltage = tk.Entry(Frame3, justify="right")
        self.variac2_L3_voltage.grid(column=4, row=6, sticky="w")
        # Variac 3
        self.variac3_ip = tk.Entry(Frame3, justify="right")
        self.variac3_ip.grid(column=0, row=7, sticky="w")
        self.variac3_request = tk.Entry(Frame3, justify="right")
        self.variac3_request.grid(column=1, row=7, sticky="w")
        self.variac3_L1_voltage = tk.Entry(Frame3, justify="right")
        self.variac3_L1_voltage.grid(column=2, row=7, sticky="w")
        self.variac3_L2_voltage = tk.Entry(Frame3, justify="right")
        self.variac3_L2_voltage.grid(column=3, row=7, sticky="w")
        self.variac3_L3_voltage = tk.Entry(Frame3, justify="right")
        self.variac3_L3_voltage.grid(column=4, row=7, sticky="w")
        # Variac 4
        self.variac4_ip = tk.Entry(Frame3, justify="right")
        self.variac4_ip.grid(column=0, row=8, sticky="w")
        self.variac4_request = tk.Entry(Frame3, justify="right")
        self.variac4_request.grid(column=1, row=8, sticky="w")
        self.variac4_L1_voltage = tk.Entry(Frame3, justify="right")
        self.variac4_L1_voltage.grid(column=2, row=8, sticky="w")
        self.variac4_L2_voltage = tk.Entry(Frame3, justify="right")
        self.variac4_L2_voltage.grid(column=3, row=8, sticky="w")
        self.variac4_L3_voltage = tk.Entry(Frame3, justify="right")
        self.variac4_L3_voltage.grid(column=4, row=8, sticky="w")
        # Save button
        tk.Button(Frame3, text="Save Variacs", command=self.saveVariacs()).grid(row=9, column=0, sticky="w")
        # Manual scripts
        self.variacs_title = tk.Label(Frame3, height=1, font=bold, bg="#e6e6e6", text="RUN SCRIPTS MANUALLY").grid(pady=10, column=0, row=10, sticky="w")
        self.manual_scripts = tk.Listbox(Frame3, width=60)
        self.manual_scripts.grid(row=11, column=0, columnspan=5, sticky="w")
        tk.Button(Frame3, text="Execute the script", command=self.executeScript()).grid(row=12, column=0, sticky="w")
        # //////////////////////////////////////////////////////////////////////////////////

        # Update fields in GUI in neverending loop
        self.loopFunction()
        # Show digital clock and calculate date/time counters
        self.actualTimers()
        # Run function on GUI startup
        self.startupFunction()
        # Fill empty Listbox - Manually triggered scripts
        self.manualScriptsFillListbox()
        # Show the GUI
        self.grid()

    def closeWindows(self):
        if messagebox.askokcancel("CRONTAB MANAGER", "You are going to quit Crontab Manager application.\nAre you sure?"):
            self.master.destroy()

    def cronStart(self):
        if messagebox.askokcancel("CRONTAB JOB", "You are going to start the CRONTAB job what will run the HTOB test.\nAre you sure?"):
            cmd = os.popen('sudo cp /etc/crontab-final /etc/crontab')
            StatArray = ["running"]  # update the status
            # --------------------------------------------
            # Update CRONTAB job status in txt-file
            # --------------------------------------------
            file_object = open("cron-status.txt", "w")  # opening the counter file for writing
            file_object.write(str(StatArray))  # write updated counter
            file_object.close()

    def cronStop(self):
        if messagebox.askokcancel("CRONTAB JOB", "You are going to stop the CRONTAB job what will cause the HTOB test will be interrupted.\nAre you sure?"):
            cmd = os.popen('sudo cp /etc/crontab-stop /etc/crontab')
            StatArray = ["stopped"]  # update the status
            # ----------------------------------------------
            # Update CRONTAB job status in txt-file
            # ----------------------------------------------
            file_object = open("cron-status.txt", "w")  # opening the counter file for writing
            file_object.write(str(StatArray))  # write updated counter
            file_object.close()
            self.exportLogs()
            messagebox.showinfo("CRONTAB JOB", "CRONTAB job stopped. Be aware that variacs might be still running with CRONTAB script!")

    def cyclesCounter(self):
        file_object = open("htob-cycles.txt","r")    # opening the counter file for reading
        value = re.findall("\d+", file_object.read())    # extract all numbers from file
        file_object.close()
        elapsed_cycles = int(value[0]) # convert the string to int number
        remaining_cycles = int(value[1]) # convert the string to int number
        total_cycles = elapsed_cycles + remaining_cycles
        # Update the label values in GUI
        self.cycles_total.config(text=str(total_cycles))
        self.cycles_elapsed.config(text=str(elapsed_cycles))
        self.cycles_remaining.config(text=str(remaining_cycles))

    def resetCounter(self):
        try:
            total_cycles = int(self.reset_cycles_total.get()) # convert the string to int number
            elapsed_cycles = int(self.reset_cycles_elapsed.get()) # convert the string to int number
            CyclArray = [elapsed_cycles, total_cycles - elapsed_cycles] # update the counter
            # Update the counter file content
            file_object = open("htob-cycles.txt","w")    # opening the counter file for writing
            file_object.write(str(CyclArray))  # write updated counter
            file_object.close()
            # Clear Entry widgets
            self.reset_cycles_total.delete(0, 'end')
            self.reset_cycles_elapsed.delete(0, 'end')
            # Save Start of date into .ini file
            self.putConfigData("TEST PARAMETERS", "start_of_test", self.start_test.get())
        except Exception:
            messagebox.showerror("Input error", "Wrong or missing values in \nNEW TOTAL CYCLES/NEW ELAPSED CYCLES field.")


    # Function runs automatically on GUI startup
    def startupFunction(self):
        # Read input parameters from .ini file - cycle duration in minutes
        self.start_test.insert(0, self.getConfigData('TEST PARAMETERS', 'start_of_test'))


    def cyclesToMinutes(self):
        # Initiate list for minutes data
        timers_minutes = []
        # Read input parameters from .ini file - cycle duration in minutes
        cycle_interval = self.getConfigData('APPLICATION', 'test_cycle_duration')
        # Do calculations cycle->time (minutes)
        timers_minutes.append(int(self.cycles_total["text"]) * int(cycle_interval))
        timers_minutes.append(int(self.cycles_elapsed["text"]) * int(cycle_interval))
        timers_minutes.append(int(timers_minutes[0]) - int(timers_minutes[1]))
        # return list with minutes data
        return timers_minutes


    def actualTimers(self):
        # Get actual timestamp to update all time/date fields in GUI
        date_time_now = datetime.now()
        # Show current time in dig.clock field
        self.clock["text"] = date_time_now.strftime('%H:%M:%S')

        # Update all timers in GUI
        timers = self.cyclesToMinutes()
        delta_total = timedelta(minutes=+int(timers[0]))
        delta_elapsed = timedelta(minutes=+int(timers[1]))
        delta_remaining = timedelta(minutes=+int(timers[2]))
        self.cycles_total_days["text"] = "{}d / {}h {}m ".format(delta_total.days, delta_total.seconds//3600, (delta_total.seconds//60)%60)
        self.cycles_elapsed_days["text"] = "{}d / {}h {}m ".format(delta_elapsed.days, delta_elapsed.seconds//3600, (delta_elapsed.seconds//60)%60)
        self.cycles_remaining_days["text"] = "{}d / {}h {}m ".format(delta_remaining.days, delta_remaining.seconds//3600, (delta_remaining.seconds//60)%60)
        # End of test
        cycles_total_minutes = date_time_now + delta_total
        self.end_test_date["text"] = cycles_total_minutes.strftime('%d.%m.%Y, %H:%M')
        # Loop code execution in function in 200 ms interval
        self.clock.after(200, self.actualTimers)


    def exportLogs(self):
        # Get timestamp to add it to the log-file name
        LogTime = datetime.now()
        # Format:  YYYY-MM-DD hh:mm:ss.msm like 2016-10-04 10:09:35.699
        logg_timestamp = LogTime.strftime("%d") + "-" + LogTime.strftime("%m") + "-" + LogTime.strftime("%Y") + "_" + LogTime.strftime("%H") + "-" + LogTime.strftime("%M") + "-" + LogTime.strftime("%S")

        try:
            # Copy log files into directory-path from Entry widget
            # File name format:  htob-test_15-10-2016_19-25-08.txt
            shutil.copyfile("htob-test.txt", os.path.join(self.logs_path.get(), "htob-test_" + logg_timestamp + ".txt"))
            shutil.copyfile("htob-test-scripts.txt", os.path.join(self.logs_path.get(), "htob-test-scripts_" + logg_timestamp + ".txt"))
        except IOError:
            print ("Unable to copy file.")
        else:
            # Clear source log files
            self.deleteContent("htob-test.txt")
            self.deleteContent("htob-test-scripts.txt")
            messagebox.showinfo("FILES EXPORT", "Log files have been successfuly exported to the destination folder.\nSource log files have been cleared for further usage.")


    def chooseDirectory(self):
        # Select directory and return its path to variable
        self.directory = filedialog.askdirectory()
        # Clear existing path
        self.logs_path.delete(0, 'end')
        # Insert new path
        self.logs_path.insert(0, self.directory)


    def deleteContent(self, fname):
        with open(fname, "w"):
            pass
        
        
    def stopAC(self):
        if messagebox.askokcancel("VARIAC AC POWER SUPPLY", "You are going to stop AC input power supply from variacs what will cause all modules switch off!\nAre you sure?"):
            cmd = os.popen("sudo python HTOB-AC-IN-Contactor-control-STOP.py")


    def cronStatus(self):
        file_object = open("cron-status.txt","r")    # opening the status file for reading
        value = re.findall("\w+", file_object.read())    # extract status from file
        file_object.close()        
        # status string to GUI field
        self.cron_status.config(text=value[0])


    # Execute a functions inside neverending loop (after() method with interval in miliseconds)
    def loopFunction(self):
        # Run functions
        self.cronStatus()
        self.cyclesCounter()
        # Re-run this function after a miliseconds
        self.master.after(5000, self.loopFunction)


    # Auxiliary function - read configuration data from .ini file
    def getConfigData(self, section, ini_parameter):
        # Read .ini file
        self.configp.read("CronManager-config.ini")
        # Read config data for this load
        ini_value = self.configp.get(str(section), str(ini_parameter))
        # Return value from .ini file
        return ini_value


    # Auxiliary function - save record into configuration data .ini file
    def putConfigData(self, ini_section, ini_parameter, ini_value):
        # Read .ini file
        self.configp.read("CronManager-config.ini")
        # Prepeare the .ini file content
        self.configp.set(ini_section, ini_parameter, ini_value)
        # Writing our configuration to .ini file
        with open("CronManager-config.ini", 'w') as configfile:
            self.configp.write(configfile)


    # Auxiliary function - return a dictionary of all items under specific section from .ini file
    # {'Label': 'Python command'}
    def listConfigData(self, ini_parameter):
        # Read .ini file
        self.configp.read("CronManager-config.ini")
        # OrderedDict() ensures the key order is the same as when data was inserted to dictionary
        # OrderedDict(any_dictionary)
        data_dict = OrderedDict(self.configp.items(ini_parameter))
        # Return dictionary
        return data_dict
            

    # Save Variacs configuration to start control process
    def saveVariacs(self):
        pass


    # Save Variacs configuration to start control process
    def executeScript(self):
        pass


    # Initiate Listbox with list of scripts which can be triggered manually
    def manualScriptsFillListbox(self):
        commands_dict = self.listConfigData("MANUAL SCRIPTS")
        # Fill Listbox with .ini records
        for key in commands_dict:
            self.manual_scripts.insert(tk.END, key)




def main():
    # Tk root window is created. The root window is a main application window in our programs.
    root = tk.Tk()
    root.geometry("750x400+70+70")
    root.minsize(width=600, height=240)
    # root = root window
    app = MainGui(master=root)
    app.mainloop()

if __name__ == '__main__':
    main()
