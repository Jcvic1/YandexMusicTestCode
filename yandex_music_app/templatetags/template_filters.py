from django import template
from datetime import datetime, timedelta, timezone
from django.template.defaultfilters import stringfilter
import json

register = template.Library()


@register.filter
@stringfilter
def update_last_seen(value):
    stored_datetime = datetime.strptime( value, "%Y-%m-%d %H:%M:%S.%f%z")
    stored_datetime = stored_datetime.replace(tzinfo=timezone.utc)
    current_datetime = datetime.now(timezone.utc)
    time_difference = current_datetime - stored_datetime
    inactive_minutes = timedelta(minutes=5)
    if time_difference < inactive_minutes:
        return True
        

@register.filter
@stringfilter
def replace(value):
    return value.replace("%%", "400x400")


@register.filter
@stringfilter
def extend(value):
    return "https://" + value


@register.filter
def to_mins_secs(value):
    time_in_milliseconds = value
    total_seconds = time_in_milliseconds / 1000
    td = timedelta(seconds=total_seconds)
    minutes, seconds = divmod(td.seconds, 60)
    return (f'{minutes}:{seconds}')


@register.filter
def get_play_link(value):
    download_info = value.get_download_info()
    max_bitrate = max([info.bitrate_in_kbps for info in download_info])
    url = list(filter(lambda t: t.codec == 'mp3' and t.bitrate_in_kbps == max_bitrate, download_info))[0].get_direct_link()
    return url


@register.filter
def multiply(value, arg):
    return value * arg

@register.filter
def split_date(value):
    date = value.split('T', 1)
    return date[0]


@register.filter
def tag_check(value):
    mix_select = value.split('/')[0]
    if 'tag' in mix_select:
        return True


@register.filter
def toggle_like_tag(value):
    my_string = value
    result = my_string.split('_')[0]
    return result


@register.filter
def tag_extract(value):
    if value.split(':')[0] == 'https':
        split_string = 'invalid'
    elif value.split('/')[0] == 'post':
        split_string = 'invalid'
    else:    
        split_string = value.split('/')[2].split('?')[0]
    return split_string            


@register.filter
def join_var(arg1, arg2):
    return str(arg1) + str(arg2)

@register.filter
def convert_to_json(value):
    json_value = json.dumps(value)
    return json_value
