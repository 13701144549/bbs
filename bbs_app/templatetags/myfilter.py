from django import template
import datetime
from django.utils.safestring import mark_safe

register = template.Library()  # register的名字是固定的,不可改变


@register.filter  # 过滤器
def round_age(create_time):
    # 计算时间差：当前的时间减去创建的时间
    now_time = datetime.datetime.now()  # 当前的时间
    user_create_time = datetime.datetime(year=create_time.year, month=create_time.month, day=create_time.day,
                                         hour=create_time.hour, minute=create_time.minute, second=create_time.second)
    ret = now_time - user_create_time
    return mark_safe(str(ret)[:-17])  # mark_safe只是做一个安全机制，和safe过滤器一样，安全之后返回
