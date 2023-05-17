import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from functions import generate_message_logic, parse_eml

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
    result_text = f"""Hello @MCCBackOffice,
    
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

upload_button = tk.Button(root, text="Upload exported email file", command=upload_eml)
upload_button.pack()

input_frame = tk.Frame(root)
input_frame.pack()

next_step_label = tk.Label(input_frame, text="Next Step:")
next_step_label.pack(side="left")

job_type_var = tk.StringVar()
job_type_dropdown = ttk.Combobox(input_frame, textvariable=job_type_var, values=['Replacement', 'Repair', 'Physical Damage', 'Area not Serviceable', 'Incorrect Diagnosis', 'Environment Issue'])
job_type_dropdown.pack(side="left")

send_to_frame = tk.Frame(root)
send_to_frame.pack()

send_to_label = tk.Label(send_to_frame, text="Send the defective unit to:")
send_to_label.pack(side="left")

iti_var = tk.BooleanVar()
iti_check = tk.Checkbutton(send_to_frame, text="ITI", variable=iti_var, command=lambda: update_output(data=parse_eml(filepath)))
iti_check.pack(side="left")

irvine_var = tk.BooleanVar()
irvine_check = tk.Checkbutton(send_to_frame, text="Irvine", variable=irvine_var, command=toggle_irvine)
irvine_check.pack(side="left")

atten_label = tk.Label(send_to_frame, text="ATTN:")
atten_entry = tk.Entry(send_to_frame)

generate_button = tk.Button(root, text="Generate", command=lambda: update_output(data=parse_eml(filepath)))
generate_button.pack()

result_box = tk.Text(root, width=75, height=30)
result_box.pack()

# Get the screen width and height
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()

# Calculate the x and y coordinates for the window
x = int((screen_width - root.winfo_reqwidth()) / 2)
y = int((screen_height - root.winfo_reqheight()) / 2)

root.geometry(f"+{x}+{y}")

root.mainloop()