from django.shortcuts import render
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
user_list = []
for i in range(1,666):
    temp = {'name':'root'+str(i),'age':i}
    user_list.append(temp)

# Create your views here.
#分页原理
def index(request):
    pre_page_count = 10
    current_page = request.GET.get('p')
    current_page = int(current_page)

    pre_pager=current_page-1    #上一页
    next_pager=current_page+1   #下一页
    #p=1
    #0,10   0-9
    #p=2
    #10,20  10-19
    start=(current_page-1)*pre_page_count
    end=current_page*pre_page_count
    data=user_list[start:end]
    return render(request,'index.html',{'user_list':data,'pre_pager':pre_pager,'next_pager':next_pager})

# ****************************************Django分页**********************************************

#自定制类分页(显示页码)
class CustomPaginator(Paginator):
    def __init__(self,current_page,per_pager_num,*args,**kwargs):
        self.current_page=int(current_page)             # 当前页
        self.per_pager_num=int(per_pager_num)           # 显示最多的页码数量 11
        super(CustomPaginator,self).__init__(*args,**kwargs)    #运用继承Paginator的功能

    def pager_num_range(self):
        #当前页	
        #self.current_page
        #最多页码数量
        # self.per_pager_num
        #总页数
        # self.num_pages
        if self.num_pages < self.per_pager_num:     #条件1：当总页数小于要显示的页码时      *
            return range(1,self.num_pages+1)
														# 条件2：当总页数大于要显示的页码时     **
        part = int(self.per_pager_num/2)            #中间页码                               **
        if self.current_page <= part:               #当前所在的页码小于中间页码，显示1-11页 **
            return range(1,self.per_pager_num+1)
        if (self.current_page + part) > self.num_pages:     #条件3：当页码到总页数时，不能再增加页码   ***
            return range(self.num_pages-self.per_pager_num+1,self.num_pages+1)
        return range(self.current_page-part,self.current_page+part+1) #当前所在页码大于中间页码，需要改变页码 **

#Django内置分页
def index1(request):
    current_page=request.GET.get('p')
    paginator = CustomPaginator(current_page,11,user_list,10)   #每页10个数据
    #per_page:每页显示条目数量
    #count:   数据总个数
    #num_page:总页数
    #page_range:总页数的索引范围，如（1,10），（1,200）
    #page:page对象
    try:
        posts=paginator.page(current_page)
        #has_next               是否有下一页
        #next_page_number       下一页页码
        #has_previous           是否有上一页
        #previous_page_number   上一页页码
        #object_list            分页之后的数据列表
        #number                 当前页
        #paginator              paginator对象
    except PageNotAnInteger:
        posts=paginator.page(1)
    except EmptyPage:
        posts=paginator.page(paginator.num_pages)
    return render(request,'index1.html',{'posts':posts})


#*****************************************自定制分页***********************************************
from app01.pager import Pagination
def index2(request):
    current_page=request.GET.get('p')
    page_obj = Pagination(666,current_page)

    data_list=user_list[page_obj.start():page_obj.end()]
    return render(request,'index2.html',{'data':data_list,'page_obj':page_obj})