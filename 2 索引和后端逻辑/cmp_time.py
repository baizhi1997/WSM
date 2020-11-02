from functools import cmp_to_key
times_str=["2019-01-27 21:11","2019-01-27 21:12","2018-01-27 21:11"]

def cmp_time(t1,t2):
    if t1 == None or t2 == None:
        return 0
    year1 = t1[0:4]
    year2 = t2[0:4]
    month1 = t1[5:7]
    print(month1)
    month2 = t2[5:7]
    day1 = t1[8:10]
    day2 = t2[8:10]
    print(day1)
    hour1 = t1[11:13]
    hour2 = t2[11:13]
    min1 = t1[14:-1]
    min2 = t2[14:-1]

    if year1 != year2 :
        return int(year2) - int(year1)
    if month1 != month2 :
        return int(month2) - int(month1)
    if day1 != day2 :
        return int(day2) - int(day1)
    if hour1 != hour2 :
        return int(hour2) - int(hour1)
    if min1 != min2 :
        return int(min2) - int(min1)
    return 0

times_str.sort(key=cmp_to_key(cmp_time))

print(times_str)
