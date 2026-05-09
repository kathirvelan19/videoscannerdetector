def format_time(seconds):
    
    minutes = int(seconds // 60)
    secs = int(seconds % 60)

    return f"{minutes:02}:{secs:02}"