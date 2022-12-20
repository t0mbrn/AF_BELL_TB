import psutil
import platform
import wmi
import GPUtil
#https://www.thepythoncode.com/article/get-hardware-system-information-python

def get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor


c = wmi.WMI()
my_system = c.Win32_ComputerSystem()[0]


def get_cpu_type():
    from win32com.client import GetObject
    root_winmgmts = GetObject("winmgmts:root\cimv2")
    cpus = root_winmgmts.ExecQuery("Select * from Win32_Processor")
    return cpus[0].Name


print("="*20, "System Information", "="*20)
uname = platform.uname()
print(f"System: {uname.system}")
print(f"System Name: {uname.node}")
print(f"Manufacturer: {my_system.Manufacturer}")
print(f"SystemFamily: {my_system.SystemFamily}")
print(f"SystemType: {my_system.SystemType}")
print(f"Model: {my_system. Model}")
print(f"Release: {uname.release}")
print(f"Version: {uname.version}")
print(f"Machine: {uname.machine}")
print(f"Processor Name: {get_cpu_type()}")
print(f"Processor: {uname.processor}")
print(f"Disk Name: {c.Win32_DiskDrive()[1].Caption}")


# let's print CPU information
print("="*20, "CPU Info", "="*20)
# number of cores
print("Physical cores:", psutil.cpu_count(logical=False))
print("Total cores:", psutil.cpu_count(logical=True))
# CPU frequencies
cpufreq = psutil.cpu_freq()
print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
# CPU usage
print("CPU Usage Per Core:")
for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
    print(f"Core {i}: {percentage}%")
print(f"Total CPU Usage: {psutil.cpu_percent()}%")

# Memory Information
print("="*20, "Memory Information", "="*20)
# get the memory details
svmem = psutil.virtual_memory()
print(f"Total: {get_size(svmem.total)}")
print(f"Available: {get_size(svmem.available)}")
print(f"Used: {get_size(svmem.used)}")
print(f"Percentage: {svmem.percent}%")
print("="*20, "SWAP", "="*20)
# get the swap memory details (if exists)
swap = psutil.swap_memory()
print(f"Total: {get_size(swap.total)}")
print(f"Free: {get_size(swap.free)}")
print(f"Used: {get_size(swap.used)}")
print(f"Percentage: {swap.percent}%")

# Disk Information
print("="*20, "Disk Information", "="*20)
print("Partitions and Usage:")
# get all disk partitions
partitions = psutil.disk_partitions()
for partition in partitions:
    print(f"=== Device: {partition.device} ===")
    print(f"  Mountpoint: {partition.mountpoint}")
    print(f"  File system type: {partition.fstype}")
    try:
        partition_usage = psutil.disk_usage(partition.mountpoint)
    except PermissionError:
        # this can be catched due to the disk that
        # isn't ready
        continue
    print(f"  Total Size: {get_size(partition_usage.total)}")
    print(f"  Used: {get_size(partition_usage.used)}")
    print(f"  Free: {get_size(partition_usage.free)}")
    print(f"  Percentage: {partition_usage.percent}%")
# get IO statistics since boot
disk_io = psutil.disk_io_counters()
print(f"Total read: {get_size(disk_io.read_bytes)}")
print(f"Total write: {get_size(disk_io.write_bytes)}")

# GPU information
print("="*20, "GPU Details", "="*20)
gpu = GPUtil.getGPUs()[0]
print(f"GPU ID: {gpu.id}")
print(f"GPU UUID: {gpu.uuid}")
print(f"GPU Name: {gpu.name}")
print(f"GPU Load: {gpu.load*100}%")
print(f" GPU Free Mem: {gpu.memoryFree} MB")
print(f" GPU Used Mem: {gpu.memoryUsed} MB")
print(f" GPU Used Total: {gpu.memoryTotal} MB")
print(f"GPU Temperature: {gpu.temperature}°C")
