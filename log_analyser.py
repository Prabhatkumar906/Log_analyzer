try:
    import tkinter as tk
    from tkinter import filedialog, messagebox
except ImportError as e:
    print("Error: tkinter is not installed on your system.")
    print("Please install tkinter by running the following command:")
    print("brew install python-tk (for macOS with Homebrew)")
    print("or")
    print("sudo apt-get install python3-tk (for Debian-based Linux systems)")
    sys.exit(1)

import re
import matplotlib.pyplot as plt
from collections import defaultdict

root = tk.Tk()
root.title("Log Analyzer")
root.geometry("400x200")

patterns = {
    'malware': re.compile(r'malware|virus|trojan|ransomware', re.IGNORECASE),
    'file_tampering': re.compile(r'file tampering|unauthorized file modification', re.IGNORECASE),
    'unauthorized_access': re.compile(r'unauthorized access|login failure|invalid login|access denied', re.IGNORECASE),
    'security_breach': re.compile(r'security breach|data breach|intrusion detected|unauthorized entry', re.IGNORECASE),
    'advanced_malware': re.compile(r'zero-day|advanced persistent threat|rootkit', re.IGNORECASE),
    'phishing': re.compile(r'phishing|spear phishing|fraudulent email', re.IGNORECASE),
    'data_leakage': re.compile(r'data leakage|data exfiltration|information leak', re.IGNORECASE)
}

remedies = {
    'malware': "Remedy: Run a full system antivirus scan, isolate the affected systems, and update your antivirus software.",
    'file_tampering': "Remedy: Restore the affected files from backup, change file permissions, and monitor file integrity.",
    'unauthorized_access': "Remedy: Reset passwords, implement multi-factor authentication, and review access logs.",
    'security_breach': "Remedy: Disconnect affected systems from the network, conduct a thorough investigation, and notify affected parties.",
    'advanced_malware': "Remedy: Employ advanced threat detection tools, perform a deep system scan, and update security protocols.",
    'phishing': "Remedy: Educate users about phishing, implement email filtering solutions, and report the phishing attempt.",
    'data_leakage': "Remedy: Identify the source of the leak, implement data loss prevention solutions, and review data access policies."
}

def analyze_log_file(log_file):
    suspicious_activity = defaultdict(int)
    with open(log_file, 'r') as f:
        for line in f:
            try:
                for activity, pattern in patterns.items():
                    if pattern.search(line):
                        suspicious_activity[activity] += 1
            except Exception as e:
                pass 

    return suspicious_activity

def save_report(log_file, suspicious_activity):
    report_file = log_file.replace('.log', '_output.txt')
    with open(report_file, 'w') as f:
        if suspicious_activity:
            for activity, count in suspicious_activity.items():
                f.write(f'{activity}: {count}\n')
                f.write(f'{remedies[activity]}\n\n')
        else:
            f.write('No suspicious activity detected.\n')
    return report_file

def plot_suspicious_activity(log_file, suspicious_activity):
    if not suspicious_activity:
        return None

    activities = list(suspicious_activity.keys())
    counts = list(suspicious_activity.values())

    plt.figure(figsize=(10, 5))
    plt.bar(activities, counts, color='red')
    plt.xlabel('Activity Type')
    plt.ylabel('Count')
    plt.title('Suspicious Activity Detected in Logs')
    graph_file = log_file.replace('.log', '_suspicious_activity.png')
    plt.savefig(graph_file)
    return graph_file

def run_analysis():
    log_file = filedialog.askopenfilename(title="Select Log File", filetypes=[("Log Files", "*.log")])
    if not log_file:
        return
    
    suspicious_activity = analyze_log_file(log_file)
    report_file = save_report(log_file, suspicious_activity)
    graph_file = plot_suspicious_activity(log_file, suspicious_activity)

    result_message = f"Analysis complete!\nReport saved to: {report_file}"
    if graph_file:
        result_message += f"\nGraph saved to: {graph_file}"

    messagebox.showinfo("Analysis Complete", result_message)

def quit_application():
    root.quit()

def create_gui():
    global root
    tk.Label(root, text="Log Analyzer Tool", font=("Helvetica", 16)).pack(pady=20)
    tk.Button(root, text="Select Log File and Scan", command=run_analysis, font=("Helvetica", 12)).pack(pady=20)
    tk.Button(root, text="Quit", command=quit_application, font=("Helvetica", 12)).pack(pady=20)

    root.mainloop()

if __name__ == '__main__':
    create_gui()
