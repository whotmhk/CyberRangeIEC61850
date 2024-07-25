#############################################################################
# This is for MSSD Project Student ID 1007386
# Titled : Cyber Range of Critical Infrastructure for Cybersecurity Experiment
############################################################################

import tkinter as tk
from tkinter import ttk
import subprocess
import os
import platform
from PIL import Image, ImageTk
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def run_script_in_terminal(script_name):
    script_path = os.path.join(os.getcwd(), 'Scripts', script_name)
    
    if not os.path.isfile(script_path):
        print(f"Script not found: {script_path}")
        return

    wrapper_path = os.path.join(os.getcwd(), 'run_with_sudo.sh')
    terminal_command = f"gnome-terminal -- bash -c '{wrapper_path} {script_path}; exec bash'"
    
    subprocess.Popen(terminal_command, shell=True)

def setup_tab(tab, scripts_info):
    btn_frame = ttk.Frame(tab)
    btn_frame.pack(side='left', fill='y', padx=50, pady=10)
    for script, description in scripts_info:
        script_frame = ttk.Frame(btn_frame)
        script_frame.pack(pady=40, fill='x', expand=True)
        btn = ttk.Button(script_frame, text=script, command=lambda s=script: run_script_in_terminal(s))
        btn.pack(side='left', padx=10, ipadx=5, ipady=5)
        desc_label = ttk.Label(script_frame, text=description, wraplength=400, font=('Arial', 12))
        desc_label.pack(side='left', padx=40)

def load_image(image_path, size=None):
    full_path = os.path.join('image', image_path)
    print(f"Trying to load image from path: {full_path}")  # Debug print
    try:
        img = Image.open(full_path)
        if size:
            img = img.resize(size, Image.Resampling.LANCZOS)
        return ImageTk.PhotoImage(img)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        print(f"File not found. Ensure the image path is correct: {full_path}")
        return None

def display_network(network_frame, img):
    print("Displaying network image")
    for widget in network_frame.winfo_children():
        if not isinstance(widget, ttk.Frame):
            widget.destroy()
    if img is not None:
        label = ttk.Label(network_frame, image=img)
        label.image = img
        label.pack(side='top', fill='both', expand=True)
    else:
        label = ttk.Label(network_frame, text="Image not found.")
        label.pack(side='top', fill='both', expand=True)

def setup_network_tab(network_tab):
    img1 = load_image('network1.jpg')
    img2 = load_image('network2.jpg')
    btn_frame = ttk.Frame(network_tab)
    btn_frame.pack(side='left', fill='y')
    btn1 = ttk.Button(btn_frame, text="Display Network 1", command=lambda: display_network(network_tab, img1))
    btn1.pack(pady=10, padx=10, ipadx=5, ipady=5)
    btn2 = ttk.Button(btn_frame, text="Display Network 2", command=lambda: display_network(network_tab, img2))
    btn2.pack(pady=10, padx=10, ipadx=5, ipady=5)

def setup_compliance_subtab(tab, file_path):
    data = pd.read_csv(file_path)
    compliance_choices = ['Compliant', 'Partial', 'Not Compliant']
    compliance_vars = []
    
    for i, row in data.iterrows():
        ttk.Label(tab, text=row['Descriptions'], wraplength=1000).grid(row=i, column=0, sticky='w')
        var = tk.StringVar(value=row['Compliance (Yes, Partial or Not)'])
        option_menu = ttk.OptionMenu(tab, var, var.get(), *compliance_choices)
        option_menu.grid(row=i, column=1, sticky='w', padx=20)
        compliance_vars.append(var)

    return compliance_vars

def calculate_compliance(vars_list):
    counts = {'Compliant': 0, 'Partial': 0, 'Not Compliant': 0}
    for var in vars_list:
        counts[var.get()] += 1
    return counts

def update_compliance_results(ot_vars, sc_vars, fc_vars, results_frame):
    for widget in results_frame.winfo_children():
        widget.destroy()

    categories = ['OT Architecture and Security', 'Secure Coding', 'Field Controllers']
    all_vars = [ot_vars, sc_vars, fc_vars]
    
    overall_counts = {'Compliant': 0, 'Partial': 0, 'Not Compliant': 0}

    left_frame = ttk.Frame(results_frame)
    left_frame.pack(side='left', fill='y', padx=(0, 10))

    right_frame = ttk.Frame(results_frame)
    right_frame.pack(side='right', fill='both', expand=True)

    for category, vars_list in zip(categories, all_vars):
        counts = calculate_compliance(vars_list)
        overall_counts['Compliant'] += counts['Compliant']
        overall_counts['Partial'] += counts['Partial']
        overall_counts['Not Compliant'] += counts['Not Compliant']

        ttk.Label(left_frame, text=f"{category}:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(10, 5))
        for status, count in counts.items():
            ttk.Label(left_frame, text=f"{status}: {count}").pack(anchor='w')

    ttk.Label(left_frame, text="Overall Compliance:", font=('Arial', 12, 'bold')).pack(anchor='w', pady=(20, 5))
    for status, count in overall_counts.items():
        ttk.Label(left_frame, text=f"{status}: {count}").pack(anchor='w')

    fig, ax = plt.subplots(figsize=(6, 6))
    ax.pie(overall_counts.values(), labels=overall_counts.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')
    plt.title('Overall Compliance Chart')
    
    canvas = FigureCanvasTkAgg(fig, master=right_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True)
    plt.close(fig)

root = tk.Tk()
root.title("IEC 61850 CyberSecurity Experimentation")
root.geometry("1200x700")

top_frame = tk.Frame(root, bg='#0057b7')
top_frame.pack(side=tk.TOP, fill=tk.X)
logo_image = load_image("logo.jpg")
logo_label = tk.Label(top_frame, image=logo_image, bg='#0057b7')
logo_label.image = logo_image
logo_label.pack(side='left', padx=0)
title_label = tk.Label(top_frame, text="       Cyber Range of Critical Infrastructure \n for \n Cybersecurity Experiment", fg='white', bg='#0057b7', font=('Arial', 30, 'bold'))
title_label.pack(side='left')

style = ttk.Style()
style.configure('TNotebook.Tab', font=('Arial', 12, 'bold'))
style.configure('TNotebook', tabposition='n')
style.configure('Custom.TNotebook.Tab', padding=[5, 5], font=('Arial', 12, 'bold'))
style.map('Custom.TNotebook.Tab', background=[('selected', '#ffcccc'), ('!selected', '#ffebcc')])

tab_control = ttk.Notebook(root, style='Custom.TNotebook')
network_tab, mms_tab, goose_tab, ccop_tab = [ttk.Frame(tab_control) for _ in range(4)]
tab_control.add(network_tab, text='Network Diagram')
tab_control.add(mms_tab, text='MMS')
tab_control.add(goose_tab, text='GOOSE')
tab_control.add(ccop_tab, text='CCOP-OT')
tab_control.pack(expand=1, fill='both')

ccop_subtab_control = ttk.Notebook(ccop_tab, style='Custom.TNotebook')
ot_tab, sc_tab, fc_tab, results_tab = [ttk.Frame(ccop_subtab_control) for _ in range(4)]
ccop_subtab_control.add(ot_tab, text="OT Architecture and Security")
ccop_subtab_control.add(sc_tab, text="Secure Coding")
ccop_subtab_control.add(fc_tab, text="Field Controllers")
ccop_subtab_control.add(results_tab, text="Compliance Results")
ccop_subtab_control.pack(expand=1, fill='both')

setup_network_tab(network_tab)
setup_tab(mms_tab, [
    ("Data_Object.py", "ObjectInfo collection from targeted device"),
    ("Attributes.py", "Getting Attributes from targeted device"),
    ("Attributes-Value.py", "Identifying Values from targeted device"),
    ("Manipulation-Control.py", "Control selected device"),
])

setup_tab(goose_tab, [
    ("GooseSniff.py", "This is to sniff the network for goose traffic \n it will be captured as pcap file as 'capture_YYYYMMDD_time'. This pcap file can be use for GooseAttack simulation later"),
    ("goose_dataset_checker.py", "Check DataSets for later simulation \n you need the sniff pcap from previous stage"),
    ("goose_device_vlans.py", "Check the VLANs and Muticast address \n you need the sniff pcap from the previous stage"),
    ("GooseAttack.py", "This Goose Attack Simulation consists of \n 1.Replay GOOSE Traffic \n 2. Masquerade as a Publisher \n 3. Craft malicious content into the Goose PDU"),
    ("Publisher", "Induce High stNum and sqNum sequence"),
])
ot_vars = setup_compliance_subtab(ot_tab, 'T1.csv')
sc_vars = setup_compliance_subtab(sc_tab, 'T2.csv')
fc_vars = setup_compliance_subtab(fc_tab, 'T3.csv')

results_frame = ttk.Frame(results_tab)
results_frame.pack(expand=True, fill='both', padx=20, pady=20)

update_button = ttk.Button(results_tab, text="Update Compliance Results", 
                           command=lambda: update_compliance_results(ot_vars, sc_vars, fc_vars, results_frame))
update_button.pack(pady=10)

root.mainloop()
