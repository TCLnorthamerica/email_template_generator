import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functions import generate_message_logic, parse_eml
import os

filepath = ""

def upload_eml():
    global filepath
    filepath = filedialog.askopenfilename(filetypes=[("EML files", "*.eml")])
    if filepath:
        data = parse_eml(filepath)
        update_output(data)

def update_output(data=None):
    if not data:
        return

    job_type = job_type_var.get()
    model_number = data['model_number']
    task, job_label = generate_message_logic(job_type, model_number)
    send_to = ""
    if iti_var.get():
        send_to = "ITI"
    if irvine_var.get():
        send_to += f" Irvine ATTN: {atten_entry.get()}"
    result_text = f"""
Hello @MCCBackOffice,

Task: {task}

Job Label: {job_label}

Case: {data.get('case_number')}

Model: {model_number}

Failed Job Reason: {data.get('failed_job')}

ITI Notes: {data.get('iti_notes')}

Send the defective unit to: {send_to}
"""
    result_box.delete("1.0", tk.END)
    result_box.insert(tk.END, result_text)

def toggle_irvine():
    if irvine_var.get():
        atten_label.pack()
        atten_entry.pack()
        update_output(data=parse_eml(filepath))  # Update output when Irvine checkbox is checked
    else:
        atten_label.pack_forget()
        atten_entry.pack_forget()
        update_output(data=parse_eml(filepath))  # Update output when Irvine checkbox is unchecked

root = tk.Tk()
root.title("Email Template Generator")

upload_button = tk.Button(root, text="Upload exported email file", command=upload_eml)
upload_button.pack(pady=10)

input_frame = tk.Frame(root)
input_frame.pack(pady=10)

next_step_label = tk.Label(input_frame, text="Next Step:")
next_step_label.pack(side="left")

job_type_var = tk.StringVar()
job_type_dropdown = ttk.Combobox(input_frame, textvariable=job_type_var, values=['Replacement', 'Repair', 'Physical Damage', 'Area not Serviceable', 'Incorrect Diagnosis', 'Environment Issue'])
job_type_dropdown.pack(side="left")

send_to_frame = tk.Frame(root)
send_to_frame.pack(pady=10)

send_to_label = tk.Label(send_to_frame, text="Send the defective unit to:")
send_to_label.pack(side="left")

iti_var = tk.BooleanVar()
iti_check = tk.Checkbutton(send_to_frame, text="ITI", variable=iti_var, command=lambda: update_output(data=parse_eml(filepath)))
iti_check.pack(side="left")

irvine_var = tk.BooleanVar()
irvine_check = tk.Checkbutton(send_to_frame, text="Irvine", variable=irvine_var, command=toggle_irvine)
irvine_check.pack(side="left")

atten_label = tk.Label(root, text="ATTN:")
atten_label.pack_forget()

atten_entry = tk.Entry(root)
atten_entry.pack_forget()

generate_button = tk.Button(root, text="Generate", command=lambda: update_output(data=parse_eml(filepath)))
generate_button.pack(pady=10)

result_box = tk.Text(root, width=50, height=60)
result_box.pack()

root.mainloop()