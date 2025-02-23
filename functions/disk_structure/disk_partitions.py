import psutil

def print_partition_structure():
    # Print the partition structure of the disk.
    partitions = psutil.disk_partitions()
    print("Partition structure of hard disks:")
    for partition in partitions:
        print(f"- Mountpoint: {partition.mountpoint}")
        print(f" Device: {partition.device}")
        print(f"Filesystem: {partition.fstype}")
        print(f"Options: {partition.opts}")