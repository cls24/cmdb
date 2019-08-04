class Pager():
    @staticmethod
    def makePager(pg_num,current_page,total_pg):
        mid = (pg_num + 1) // 2
        if current_page < mid:
            start_pg = 1
            end_pg = total_pg if total_pg < pg_num else pg_num
        elif current_page + mid - 1 > total_pg:
            start_pg = total_pg - pg_num + 1
            end_pg = total_pg
        else:
            start_pg = current_page - 2
            end_pg = current_page + 2
        prev = '<li class="page-item %s" pn="%d"><a class="page-link" href="#">上一页</a></li>'%('disabled' if current_page==1 else '',current_page-1)
        next = '<li class="page-item %s" pn="%d"><a class="page-link" href="#">下一页</a></li>'%('disabled' if current_page==total_pg else '',current_page+1)
        pg_list = [prev]
        for i in range(start_pg,end_pg+1):
            active = 'active' if i==current_page else ''
            pg_list.append('<li class="page-item %s" pn="%s"><a class="page-link" href="#">%s</a></li>'%(active,i,i))
        pg_list.append(next)
        pager = '<ul class="pagination">%s</ul>'%(''.join(pg_list))
        return pager