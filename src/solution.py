## Student Name:MHD-Oubai Al-khimi
## Student ID: 219533637
from typing import List, Dict

def suggest_slots(events: List[Dict[str, str]], meeting_duration: int, day: str) -> List[str]:
    def to_min(time_str: str) -> int:
        h, m = map(int, time_str.split(':'))
        return h * 60 + m

    def from_min(minutes: int) -> str:
        return f"{minutes // 60:02d}:{minutes % 60:02d}"

    # Constants in minutes
    WORK_START, WORK_END = 9 * 60, 17 * 60
    LUNCH_START, LUNCH_END = 12 * 60, 13 * 60
    
    # Process events into minute ranges
    blocked_periods = []
    for e in events:
        start, end = to_min(e['start']), to_min(e['end'])
        # Only care about events that overlap with working hours
        if end > WORK_START and start < WORK_END:
            blocked_periods.append((start, end))

    suggestions = []
    
    # Check every 15-minute slot
    for start_m in range(WORK_START, WORK_END, 15):
        end_m = start_m + meeting_duration
        
        # Constraint 1: Must end by end of day
        if end_m > WORK_END:
            continue
            
        # Constraint 2: Start time cannot be during lunch [12:00, 13:00)
        if LUNCH_START <= start_m < LUNCH_END:
            continue
            
        # Constraint 3: Overlap check
        is_blocked = False
        for b_start, b_end in blocked_periods:
            # Standard overlap logic: (StartA < EndB) and (EndA > StartB)
            if start_m < b_end and end_m > b_start:
                is_blocked = True
                break
        
        if not is_blocked:
            suggestions.append(from_min(start_m))
            
    return suggestions
