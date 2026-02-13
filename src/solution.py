## Student Name:MHD-Oubai Al-khimi
## Student ID: 219533637
import datetime

def suggest_slots(events, meeting_duration, day):
    """
    Suggests meeting slots for a given day, incorporating the Friday 15:00 cutoff.
    """
    WORK_START = "09:00"
    WORK_END = "17:00"
    LUNCH_START = "12:00"
    LUNCH_END = "13:00"
    FRIDAY_CUTOFF = "15:00"
    
    def time_to_minutes(t_str):
        h, m = map(int, t_str.split(':'))
        return h * 60 + m

    def minutes_to_time(minutes):
        h = minutes // 60
        m = minutes % 60
        return f"{h:02d}:{m:02d}"

    # Determine if the day is a Friday
    date_obj = datetime.datetime.strptime(day, "%Y-%m-%d")
    is_friday = date_obj.weekday() == 4  # 4 represents Friday
    
    work_start_min = time_to_minutes(WORK_START)
    work_end_min = time_to_minutes(WORK_END)
    friday_cutoff_min = time_to_minutes(FRIDAY_CUTOFF)
    
    blocked_intervals = []
    blocked_intervals.append((time_to_minutes(LUNCH_START), time_to_minutes(LUNCH_END)))
    
    for event in events:
        start = time_to_minutes(event['start'])
        end = time_to_minutes(event['end'])
        blocked_intervals.append((start, end))
    
    blocked_intervals.sort(key=lambda x: x[0])
    
    valid_slots = []
    current_time = work_start_min
    
    while current_time + meeting_duration <= work_end_min:
        # NEW CONSTRAINT: Check if it's Friday and the start time is after 15:00
        if is_friday and current_time > friday_cutoff_min:
            break  # Stop looking for slots after 15:00 on Fridays
            
        meeting_start = current_time
        meeting_end = current_time + meeting_duration
        
        is_valid = True
        for b_start, b_end in blocked_intervals:
            if meeting_start < b_end and meeting_end > b_start:
                is_valid = False
                break
        
        if is_valid:
            valid_slots.append(minutes_to_time(meeting_start))
        
        current_time += 15
        
    return valid_slots
