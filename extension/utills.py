from django.utils import timezone 
from . import jalali

def convert_to_jalali_date(time):
    time = timezone.localtime(time)
    jmonth = ["فروردین", "اردیبهشت", "خرداد", "تیر", "مرداد", "شهریور", "مهر", "آبان", "آذر", " دی", " بهمن", " اسفند"]
    jalali_to_str = f'{time.year},{time.month},{time.day}'
    jalali_to_tuple = jalali.Gregorian(jalali_to_str).persian_tuple()
    jalali_to_list = list(jalali_to_tuple)
    for index, value in enumerate(jmonth):
        if jalali_to_list[1] == index + 1:
            jalali_to_list[1] = value 
            break 
    
    output = f'{jalali_to_list[2]} , {jalali_to_list[1]} , {jalali_to_list[0]},  ساعت: {time.hour}:{time.minute}' 
    return output
    

    