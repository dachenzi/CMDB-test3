#!/usr/bin/env python
# _*_coding:utf-8_*_
# __author__:daxin

class Page(object):
    def __init__(self,current_page,all_count,base_url,per_page=10,pager_page_count=11):
        """
        分页初始化
        :param current_page: 当前页码
        :param per_page: 每页显示数据条数
        :param all_count: 数据库中总条数
        :param pager_page_count: 页面上最多显示的页码数量
        """
        self.base_url = base_url
        self.current_page = current_page
        self.per_page = per_page
        self.all_count = all_count
        self.pager_page_count = pager_page_count
        pager_count, b = divmod(all_count, per_page)
        if b != 0:
            pager_count += 1
        self.pager_count = pager_count

        half_pager_page_count = int(pager_page_count / 2)
        self.half_pager_page_count = half_pager_page_count

    @property
    def start(self):
        """
        数据获取值起始索引
        :return:
        """
        return (self.current_page - 1) * self.per_page

    @property
    def end(self):
        """
        数据获取值结束索引
        :return:
        """
        return self.current_page * self.per_page

    def page_html(self):
        """
        生成HTML页码
        :return:
        """
        # 如果数据总页码pager_count<11 pager_page_count
        if self.pager_count < self.pager_page_count:
            pager_start = 1
            pager_end = self.pager_count
        else:
            # 数据页码已经超过11
            # 判断： 如果当前页 <= 5 half_pager_page_count
            if self.current_page <= self.half_pager_page_count:
                pager_start = 1
                pager_end = self.pager_page_count
            else:
                # 如果： 当前页+5 > 总页码
                if (self.current_page + self.half_pager_page_count) > self.pager_count:
                    pager_end = self.pager_count
                    pager_start = self.pager_count - self.pager_page_count + 1
                else:
                    pager_start = self.current_page - self.half_pager_page_count
                    pager_end = self.current_page + self.half_pager_page_count

        page_list = []
        if self.current_page <= 1:
            prev = '<a href="#">上一页</a>'
        else:
            prev = '<a href="%s?page=%s">上一页</a>' % (self.base_url,self.current_page - 1,)
        page_list.append(prev)
        for i in range(pager_start, pager_end + 1):
            if self.current_page == i:
                tpl = '<a class="active" href="%s?page=%s">%s</a>' % (self.base_url,i, i,)
            else:
                tpl = '<a href="%s?page=%s">%s</a>' % (self.base_url,i, i,)
            page_list.append(tpl)

        if self.current_page >= self.pager_count:
            nex = '<a href="#">下一页</a>'
        else:
            nex = '<a href="%s?page=%s">下一页</a>' % (self.base_url,self.current_page + 1,)
        page_list.append(nex)
        page_str = "".join(page_list)
        return page_str