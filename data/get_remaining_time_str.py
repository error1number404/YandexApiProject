import datetime

def get_remaining_time_str(delta):
    if delta.total_seconds() < 0 and delta.total_seconds() > -3600:
        return'Already started'
    elif delta.total_seconds() < 0:
        return 'Ended'
    elif delta.total_seconds() // 31536000 > 0:
        return f'{round(delta.total_seconds() // 31536000)} {"year" if delta.total_seconds() // 31536000 < 2 else "years"}'
    elif delta.total_seconds() // 2592000 > 0:
        return f'{round(delta.total_seconds() // 2592000)} {"month" if delta.total_seconds() // 2592000 < 2 else "months"}'
    elif delta.total_seconds() // 86400 > 0:
        return f'{round(delta.total_seconds() // 86400)} {"day" if delta.total_seconds() // 86400 < 2 else "days"}'
    elif delta.total_seconds() // 3600 > 0:
        return f'{round(delta.total_seconds() // 3600)} {"hour" if delta.total_seconds() // 60 < 2 else "hours"} {round((delta.total_seconds() - 3600 * (delta.total_seconds() // 3600)) // 60)} {"minute" if (delta.total_seconds() - 3600 * (delta.total_seconds() // 3600)) // 60 < 2 else "minutes"}'
    else:
        return f'{round(delta.total_seconds() // 60)} {"minute" if delta.total_seconds() // 60 < 2 else "minutes"} {round(delta.total_seconds() - 60 * (delta.total_seconds() // 60))} {"second" if round(delta.total_seconds() - 60 * (delta.total_seconds() // 60)) < 2 else "seconds"}'
