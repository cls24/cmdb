from django.test import TestCase

# Create your tests here.
def culPager(pg_num, current_page, total_pg):
    mid = (pg_num + 1) // 2
    if current_page < mid:
        start_pg = 1
        end_pg = pg_num
    elif current_page + mid-1 > total_pg:
        start_pg = total_pg - pg_num + 1
        end_pg = total_pg
    else:
        start_pg = current_page - 2
        end_pg = current_page + 2
    return (start_pg, end_pg)

[1,2,3,4,5,6,7,8,9,10]
for i in range(1,11):
    print(i,culPager(5,i,10))
