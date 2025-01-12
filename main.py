import os
import platform
import psutil
import socket
import datetime
import time
import webbrowser
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text
from rich.prompt import Prompt

# Initialize Console
console = Console()

# Loading Animation
def loading_animation(message="Processing..."):
    with Progress(console=console) as progress:
        task = progress.add_task("[bold cyan]" + message, total=100)
        for i in range(100):
            time.sleep(0.02)
            progress.update(task, advance=1)

def ask_username():
    console.print("\n[bold cyan]Welcome! Please enter your username:[/bold cyan]", style="bold magenta")
    username = input("[Input] >> ").strip()
    return username

def ask_wake_up_phrase(username):
    console.print(f"[bold cyan]\nHello {username}, please enter your wake-up phrase:[/bold cyan]", style="bold magenta")
    phrase = input("[Input] >> ").strip()
    if phrase.lower() == "wake up daddy's home":
        loading_animation("Connecting to Satellite...")
        console.print(f"\n[green]Welcome Back, Boss {username}![/green]", style="bold green")
    else:
        console.print("[red]Access Denied![/red]", style="bold red")
        exit()

# System Info Module
def get_system_info():
    console.print("\n[bold cyan]System Information:[/bold cyan]")
    table = Table(title="System Overview", show_header=True, header_style="bold magenta")
    table.add_column("Attribute", justify="left")
    table.add_column("Details", justify="right")

    table.add_row("OS", platform.system())
    table.add_row("Kernel Version", platform.release())
    table.add_row("Machine", platform.machine())
    table.add_row("Processor", platform.processor())
    table.add_row("IP Address", socket.gethostbyname(socket.gethostname()))
    table.add_row("Network Name", get_network_name())

    console.print(Panel(table, style="bold yellow"))

# Battery Info Module
def get_battery_info():
    battery = psutil.sensors_battery()
    console.print("\n[bold cyan]Battery Information:[/bold cyan]")

    if battery:
        status = "Charging" if battery.power_plugged else "Discharging"
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Attribute", justify="left")
        table.add_column("Details", justify="right")
        table.add_row("Battery Percentage", f"{battery.percent}%")
        table.add_row("Power Status", status)
        table.add_row("Time Left", f"{battery.secsleft // 60} min" if battery.secsleft != psutil.POWER_TIME_UNLIMITED else "Unlimited")
        console.print(Panel(table, style="bold green"))
    else:
        console.print("[red]No Battery Detected![/red]")

# CPU and Memory Usage
def get_cpu_memory_usage():
    cpu_percent = psutil.cpu_percent(interval=1)
    memory_info = psutil.virtual_memory()

    console.print("\n[bold cyan]CPU and Memory Usage:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Attribute", justify="left")
    table.add_column("Details", justify="right")
    table.add_row("CPU Usage", f"{cpu_percent}%")
    table.add_row("Memory Usage", f"{memory_info.percent}%")
    console.print(Panel(table, style="bold blue"))

# Disk Space Usage
def get_disk_usage():
    console.print("\n[bold cyan]Disk Space Usage:[/bold cyan]")
    partitions = psutil.disk_partitions()
    for partition in partitions:
        usage = psutil.disk_usage(partition.mountpoint)
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Drive", justify="left")
        table.add_column("Used", justify="right")
        table.add_column("Free", justify="right")
        table.add_column("Total", justify="right")
        table.add_row(partition.device, f"{usage.used / (1024**3):.2f} GB", f"{usage.free / (1024**3):.2f} GB", f"{usage.total / (1024**3):.2f} GB")
        console.print(Panel(table, style="bold purple"))

# System Uptime
def get_system_uptime():
    uptime = time.time() - psutil.boot_time()
    uptime_str = str(datetime.timedelta(seconds=uptime))
    console.print(f"\n[bold cyan]System Uptime:[/bold cyan] {uptime_str}")

# Network Usage (Bandwidth)
def get_network_usage():
    net_io = psutil.net_io_counters()
    console.print("\n[bold cyan]Network Usage:[/bold cyan]")
    table = Table(show_header=True, header_style="bold magenta")
    table.add_column("Attribute", justify="left")
    table.add_column("Details", justify="right")
    table.add_row("Bytes Sent", f"{net_io.bytes_sent / (1024**2):.2f} MB")
    table.add_row("Bytes Received", f"{net_io.bytes_recv / (1024**2):.2f} MB")
    console.print(Panel(table, style="bold red"))

# Get Network Name
def get_network_name():
    try:
        network_name = os.popen("iwgetid -r").read().strip()  # For Linux
        if not network_name:
            network_name = os.popen("netsh wlan show interfaces | findstr SSID").read().strip()  # For Windows
        return network_name if network_name else "Not connected to Wi-Fi"
    except Exception as e:
        return "Error retrieving network name"

# File Management Functions
def list_files(directory="."):
    console.print(f"\n[bold cyan]Listing files in directory: {directory}[/bold cyan]", style="bold magenta")
    for item in os.listdir(directory):
        console.print(item)

def create_file(file_path):
    open(file_path, 'a').close()
    console.print(f"[green]File '{file_path}' created.[/green]")

def delete_file(file_path):
    if os.path.exists(file_path):
        os.remove(file_path)
        console.print(f"[red]File '{file_path}' deleted.[/red]")
    else:
        console.print(f"[red]File '{file_path}' does not exist.[/red]")

def move_file(src, dst):
    if os.path.exists(src):
        os.rename(src, dst)
        console.print(f"[green]File moved from '{src}' to '{dst}'[/green]")
    else:
        console.print(f"[red]File '{src}' does not exist.[/red]")

def read_file(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            console.print(file.read())
    else:
        console.print(f"[red]File '{file_path}' does not exist.[/red]")

def write_file(file_path, content):
    with open(file_path, 'w') as file:
        file.write(content)
        console.print(f"[green]Content written to '{file_path}'.[/green]")

# Task Management Functions
def list_processes():
    console.print("\n[bold cyan]Running Processes:[/bold cyan]", style="bold magenta")
    for proc in psutil.process_iter(['pid', 'name', 'username']):
        console.print(f"PID: {proc.info['pid']}, Name: {proc.info['name']}, User: {proc.info['username']}")

def start_process(command):
    os.system(command)
    console.print(f"[green]Process '{command}' started.[/green]")

def stop_process(pid):
    try:
        proc = psutil.Process(pid)
        proc.terminate()
        console.print(f"[red]Process with PID {pid} terminated.[/red]")
    except psutil.NoSuchProcess:
        console.print(f"[red]No process with PID {pid} found.[/red]")

# User Management Functions
def add_user(username):
    try:
        os.system(f"useradd {username}")
        console.print(f"[green]User '{username}' added.[/green]")
    except Exception as e:
        console.print(f"[red]Error adding user: {e}[/red]")

def remove_user(username):
    try:
        os.system(f"userdel {username}")
        console.print(f"[red]User '{username}' removed.[/red]")
    except Exception as e:
        console.print(f"[red]Error removing user: {e}[/red]")

def change_password(username):
    try:
        os.system(f"passwd {username}")
        console.print(f"[green]Password for user '{username}' changed.[/green]")
    except Exception as e:
        console.print(f"[red]Error changing password: {e}[/red]")

# System Settings Functions
def display_system_settings():
    console.print("\n[bold cyan]System Settings:[/bold cyan]", style="bold magenta")
    console.print(f"Hostname: {socket.gethostname()}")
    console.print(f"IP Address: {socket.gethostbyname(socket.gethostname())}")

def change_hostname(new_hostname):
    try:
        os.system(f"hostnamectl set-hostname {new_hostname}")
        console.print(f"[green]Hostname changed to '{new_hostname}'[/green]")
    except Exception as e:
        console.print(f"[red]Error changing hostname: {e}[/red]")

# Scheduled Tasks Functions
def create_scheduled_task(task, time):
    # Simulate creating a scheduled task
    console.print(f"[green]Scheduled task '{task}' at {time}[/green]")

def list_scheduled_tasks():
    # Simulate listing scheduled tasks
    console.print("[bold cyan]Listing scheduled tasks (simulated):[/bold cyan]")
    console.print("Task 1: Backup at 02:00 AM")
    console.print("Task 2: System Update at 03:00 AM")

def remove_scheduled_task(task_id):
    # Simulate removing a scheduled task
    console.print(f"[red]Scheduled task '{task_id}' removed (simulated)[/red]")

# Utilities Functions
def calculator():
    expression = Prompt.ask("[bold cyan]Enter expression to calculate (e.g., 3 + 4 * 2):[/bold cyan]")
    try:
        result = eval(expression)
        console.print(f"[green]Result: {result}[/green]")
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")

def clipboard_management():
    # Simulate clipboard management
    console.print("[bold cyan]Clipboard management (simulated):[/bold cyan]")
    clipboard = ""
    while True:
        action = Prompt.ask("[bold cyan]Choose action (copy/paste/exit):[/bold cyan]").lower()
        if action == "copy":
            clipboard = Prompt.ask("[bold cyan]Enter text to copy to clipboard:[/bold cyan]")
            console.print(f"[green]Copied to clipboard: {clipboard}[/green]")
        elif action == "paste":
            console.print(f"[green]Clipboard content: {clipboard}[/green]")
        elif action == "exit":
            break
        else:
            console.print("[red]Invalid action[/red]")

def file_compression():
    # Simulate file compression
    file_path = Prompt.ask("[bold cyan]Enter file path to compress:[/bold cyan]")
    console.print(f"[green]File '{file_path}' compressed (simulated)[/green]")

def local_password_manager():
    # Simulate local password manager
    console.print("[bold cyan]Local password manager (simulated):[/bold cyan]")
    passwords = {}
    while True:
        action = Prompt.ask("[bold cyan]Choose action (add/view/delete/exit):[/bold cyan]").lower()
        if action == "add":
            service = Prompt.ask("[bold cyan]Enter service name:[/bold cyan]")
            password = Prompt.ask("[bold cyan]Enter password:[/bold cyan]")
            passwords[service] = password
            console.print(f"[green]Password for {service} added.[/green]")
        elif action == "view":
            service = Prompt.ask("[bold cyan]Enter service name to view password:[/bold cyan]")
            if service in passwords:
                console.print(f"[green]Password for {service}: {passwords[service]}[/green]")
            else:
                console.print(f"[red]No password found for {service}[/red]")
        elif action == "delete":
            service = Prompt.ask("[bold cyan]Enter service name to delete password:[/bold cyan]")
            if service in passwords:
                del passwords[service]
                console.print(f"[red]Password for {service} deleted.[/red]")
            else:
                console.print(f"[red]No password found for {service}[/red]")
        elif action == "exit":
            break
        else:
            console.print("[red]Invalid action[/red]")

def searchable_offline_docs():
    # Simulate searchable offline documentation
    console.print("[bold cyan]Searchable offline documentation (simulated):[/bold cyan]")
    docs = {
        "sysinfo": "Displays system information.",
        "list": "Lists files and directories.",
        "calc": "Opens the calculator.",
    }
    query = Prompt.ask("[bold cyan]Enter command to search for:[/bold cyan]").lower()
    if query in docs:
        console.print(f"[green]{query}: {docs[query]}[/green]")
    else:
        console.print(f"[red]No documentation found for '{query}'[/red]")

# Customization Functions
def set_alias(alias, command):
    aliases[alias] = command
    console.print(f"[green]Alias '{alias}' set for command '{command}'[/green]")

def theme_customization():
    # Simulate theme customization
    console.print("[bold cyan]Theme customization (simulated):[/bold cyan]")
    theme = Prompt.ask("[bold cyan]Enter theme name (e.g., dark, light):[/bold cyan]").lower()
    console.print(f"[green]Theme set to '{theme}' (simulated)[/green]")

# Developer Tools Functions
def code_runner(file_path):
    os.system(f"python {file_path}")
    console.print(f"[green]Executed script '{file_path}'[/green]")

def version_control_simulation():
    # Simulate version control
    console.print("[bold cyan]Version control simulation (simulated):[/bold cyan]")
    console.print("Commit: Initial commit")
    console.print("Branch: main")

def custom_scripting():
    # Simulate custom scripting
    console.print("[bold cyan]Custom scripting (simulated):[/bold cyan]")
    script = Prompt.ask("[bold cyan]Enter script to execute (e.g., print('Hello, World!')):[/bold cyan]")
    try:
        exec(script)
        console.print("[green]Script executed successfully.[/green]")
    except Exception as e:
        console.print(f"[red]Error executing script: {e}[/red]")

# Placeholder for menus that are not yet implemented
def file_management_menu():
    console.print("[bold cyan]File management menu is under development.[/bold cyan]")

def system_settings_menu():
    console.print("[bold cyan]System settings menu is under development.[/bold cyan]")

def main_menu():
    aliases = {}
    while True:
        console.print("\n[bold cyan]Main Menu[/bold cyan]", style="bold magenta")
        console.print("1. System Information")
        console.print("2. File Management")
        console.print("3. Process Management")
        console.print("4. User Management")
        console.print("5. System Settings")
        console.print("6. Scheduled Tasks")
        console.print("7. Utilities")
        console.print("8. Customization")
        console.print("9. Developer Tools")
        console.print("10. Shutdown System")
        console.print("11. Restart System")
        console.print("12. Exit")

        choice = input("[Input] >> ").strip()

        if choice == "1":
            get_system_info()
            get_battery_info()
            get_cpu_memory_usage()
            get_disk_usage()
            get_system_uptime()
            get_network_usage()
        elif choice == "2":
            file_management_menu()
        elif choice == "3":
            process_management_menu()
        elif choice == "4":
            user_management_menu()
        elif choice == "5":
            system_settings_menu()
        elif choice == "6":
            scheduled_tasks_menu()
        elif choice == "7":
            utilities_menu()
        elif choice == "8":
            customization_menu()
        elif choice == "9":
            developer_tools_menu()
        elif choice == "10":
            shutdown_system()
        elif choice == "11":
            restart_system()
        elif choice == "12":
            console.print("\n[bold cyan]Thank you for using the System Management Tool![/bold cyan]")
            break
        else:
            console.print("[red]Invalid option, please try again.[/red]")

# Process Management Menu
def process_management_menu():
    while True:
        console.print("\n[bold cyan]Process Management[/bold cyan]", style="bold magenta")
        console.print("1. List Running Processes")
        console.print("2. Start Process")
        console.print("3. Stop Process")
        console.print("4. Back to Main Menu")

        choice = input("[Input] >> ").strip()

        if choice == "1":
            list_processes()
        elif choice == "2":
            command = input("[Input] Enter process command to start: ").strip()
            start_process(command)
        elif choice == "3":
            pid = int(input("[Input] Enter PID to stop: ").strip())
            stop_process(pid)
        elif choice == "4":
            break
        else:
            console.print("[red]Invalid option, please try again.[red]")

# User Management Menu
def user_management_menu():
    while True:
        console.print("\n[bold cyan]User Management[/bold cyan]", style="bold magenta")
        console.print("1. Add User")
        console.print("2. Remove User")
        console.print("3. Change Password")
        console.print("4. Back to Main Menu")

        choice = input("[Input] >> ").strip()

        if choice == "1":
            username = input("[Input] Enter username to add: ").strip()
            add_user(username)
        elif choice == "2":
            username = input("[Input] Enter username to remove: ").strip()
            remove_user(username)
        elif choice == "3":
            username = input("[Input] Enter username to change password: ").strip()
            change_password(username)
        elif choice == "4":
            break
        else:
            console.print("[red]Invalid option, please try again.[/red]")

# Scheduled Tasks Menu
def scheduled_tasks_menu():
    while True:
        console.print("\n[bold cyan]Scheduled Tasks[/bold cyan]", style="bold magenta")
        console.print("1. Create Scheduled Task")
        console.print("2. List Scheduled Tasks")
        console.print("3. Remove Scheduled Task")
        console.print("4. Back to Main Menu")

        choice = input("[Input] >> ").strip()

        if choice == "1":
            task = input("[Input] Enter task description: ").strip()
            time = input("[Input] Enter time (HH:MM): ").strip()
            create_scheduled_task(task, time)
        elif choice == "2":
            list_scheduled_tasks()
        elif choice == "3":
            task_id = input("[Input] Enter task ID to remove: ").strip()
            remove_scheduled_task(task_id)
        elif choice == "4":
            break
        else:
            console.print("[red]Invalid option, please try again.[/red]")

# Utilities Menu
def utilities_menu():
    while True:
        console.print("\n[bold cyan]Utilities[/bold cyan]", style="bold magenta")
        console.print("1. Calculator")
        console.print("2. Clipboard Management")
        console.print("3. File Compression")
        console.print("4. Local Password Manager")
        console.print("5. Searchable Offline Docs")
        console.print("6. Back to Main Menu")

        choice = input("[Input] >> ").strip()

        if choice == "1":
            calculator()
        elif choice == "2":
            clipboard_management()
        elif choice == "3":
            file_compression()
        elif choice == "4":
            local_password_manager()
        elif choice == "5":
            searchable_offline_docs()
        elif choice == "6":
            break
        else:
            console.print("[red]Invalid option, please try again.[/red]")

# Customization Menu
def customization_menu():
    while True:
        console.print("\n[bold cyan]Customization[/bold cyan]", style="bold magenta")
        console.print("1. Set Command Alias")
        console.print("2. Theme Customization")
        console.print("3. Back to Main Menu")

        choice = input("[Input] >> ").strip()

        if choice == "1":
            alias = input("[Input] Enter alias name: ").strip()
            command = input("[Input] Enter command: ").strip()
            set_alias(alias, command)
        elif choice == "2":
            theme_customization()
        elif choice == "3":
            break
        else:
            console.print("[red]Invalid option, please try again.[/red]")

# Developer Tools Menu
def developer_tools_menu():
    while True:
        console.print("\n[bold cyan]Developer Tools[/bold cyan]", style="bold magenta")
        console.print("1. Code Runner")
        console.print("2. Version Control")
        console.print("3. Custom Scripting")
        console.print("4. Back to Main Menu")

        choice = input("[Input] >> ").strip()

        if choice == "1":
            file_path = input("[Input] Enter Python file path to run: ").strip()
            code_runner(file_path)
        elif choice == "2":
            version_control_simulation()
        elif choice == "3":
            custom_scripting()
        elif choice == "4":
            break
        else:
            console.print("[red]Invalid option, please try again.[/red]")

# Main execution
if __name__ == "__main__":
    try:
        username = ask_username()
        ask_wake_up_phrase(username)
        main_menu()
    except KeyboardInterrupt:
        console.print("\n[bold red]Program terminated by user.[/bold red]")
    except Exception as e:
        console.print(f"\n[bold red]An error occurred: {e}[/bold red]")
    finally:
        console.print("\n[bold cyan]Thank you for using the System Management Tool![/bold cyan]")
