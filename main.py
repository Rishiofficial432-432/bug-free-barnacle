import os
import platform
import psutil
import socket
import datetime
import time
from rich.console import Console
from rich.table import Table
from rich.progress import Progress
from rich.panel import Panel
from rich.text import Text

# Initialize Console
console = Console()

# Loading Animation
def loading_animation():
    with Progress(console=console) as progress:
        task = progress.add_task("[bold cyan]Connecting to Satellite...", total=100)
        for i in range(100):
            time.sleep(0.03)
            progress.update(task, advance=1)

def ask_username():
    console.print("\n[bold cyan]Welcome! Please enter your username:[/bold cyan]", style="bold magenta")
    username = input("[Input] >> ").strip()
    return username

def ask_wake_up_phrase(username):
    console.print(f"[bold cyan]\nHello {username}, please enter your wake-up phrase:[/bold cyan]", style="bold magenta")
    phrase = input("[Input] >> ").strip()
    if phrase.lower() == "wake up daddy's home":
        loading_animation()
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

# Ask for Project Type: Old or New
def ask_project_type():
    console.print("\n[bold cyan]What type of project would you like to work on?[/bold cyan]", style="bold magenta")
    project_type = input("[Input] (1 for Old Projects, 2 for New Project) >> ").strip()
    return project_type

# Function to Handle Echo AI-related Projects
def create_echo_ai_project():
    project_directory = input("[Input] Enter the directory where you want to save this project >> ").strip()
    project_name = input("[Input] What should we name the project? >> ").strip()

    # Create the project directory and project file
    loading_animation()
    try:
        project_path = os.path.join(project_directory, project_name)
        os.makedirs(project_path, exist_ok=True)
        console.print(f"\n[green]Created new Echo AI project: {project_name}[/green]")
    except Exception as e:
        console.print(f"[red]Error creating project: {e}[/red]")

# Function to Handle Private Project Creation
def create_private_project():
    project_directory = input("[Input] Enter the directory where you want to save the project (private files) >> ").strip()
    project_name = input("[Input] What should we name the project? >> ").strip()

    # Create a private directory and project file
    loading_animation()
    try:
        private_dir = os.path.join(project_directory, "private")
        os.makedirs(private_dir, exist_ok=True)

        project_path = os.path.join(private_dir, project_name)
        os.makedirs(project_path, exist_ok=True)

        console.print(f"\n[green]Created new private project: {project_name}[/green]")
    except Exception as e:
        console.print(f"[red]Error creating project: {e}[/red]")

# Function to Handle New Project Logic
def create_new_project():
    console.print("\n[bold cyan]Is this project related to Echo AI?[/bold cyan]", style="bold magenta")
    related_to_echo_ai = input("[Input] (yes/no) >> ").strip().lower()

    if related_to_echo_ai == "yes":
        create_echo_ai_project()
    else:
        create_private_project()

# Main Function
def main():
    os.system('cls' if os.name == 'nt' else 'clear')
    username = ask_username()
    ask_wake_up_phrase(username)

    # Add a beautiful heading
    console.print(Panel("[bold cyan]Welcome to Your System Monitor[/bold cyan]", style="bold yellow", expand=False))

    # Display System Information
    get_system_info()
    get_battery_info()
    get_cpu_memory_usage()
    get_disk_usage()
    get_system_uptime()
    get_network_usage()

    # Ask about projects after system details
    project_type = ask_project_type()

    if project_type == "2":  # New Project
        create_new_project()
    elif project_type == "1":  # Old Projects
        console.print("[yellow]Old Projects option selected, exiting...[/yellow]")
        exit()
    else:
        console.print("[red]Invalid option, exiting...[/red]")

if __name__ == "__main__":
    main()
