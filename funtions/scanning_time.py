def format_elapsed_time(elapsed_time):
    """Format the elapsed time into a readable string."""
    days, remainder = divmod(elapsed_time, 86400)
    hours, remainder = divmod(remainder, 3600)
    minutes, seconds = divmod(remainder, 60)
    
    time_parts = []
    if days > 0:
        time_parts.append(f"{int(days)} days")
    if hours > 0:
        time_parts.append(f"{int(hours)} hours")
    if minutes > 0:
        time_parts.append(f"{int(minutes)} minutes")
    time_parts.append(f"{seconds:.2f} seconds")
    
    return ', '.join(time_parts)