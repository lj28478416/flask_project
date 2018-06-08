var currentCid = 0; // 当前分类 id
var firstin = true
var cur_page = 1; // 当前页
var total_page = 1;  // 总页数
var data_querying = true;   // 是否正在向后台获取数据


$(function () {
    vue_list_con = new Vue({
        el: '.list_con',
        delimiters: ['[[', ']]'],//将语法中的{{换成[[，将}}换成]]
        data: {
            news_list: []
        }
    });
    // 首页分类切换
    $('.menu li').click(function () {
        var clickCid = $(this).attr('data-cid')
        $('.menu li').each(function () {
            $(this).removeClass('active')
        })
        $(this).addClass('active')
        if (clickCid != currentCid) {
            // TODO 去加载新闻数据
            cur_page=1
            vue_list_con.news_list=[]
            updateNewsData(clickCid ,1);
            currentCid=clickCid
        }
    })
    if(firstin = true){
        firstin = false
        $('.menu li').eq(0).addClass('active')
        updateNewsData(0,1)
    }

    //页面滚动加载相关
    $(window).scroll(function () {

        // 浏览器窗口高度
        var showHeight = $(window).height();

        // 整个网页的高度
        var pageHeight = $(document).height();

        // 页面可以滚动的距离
        var canScrollHeight = pageHeight - showHeight;

        // 页面滚动了多少,这个是随着页面滚动实时变化的
        var nowScroll = $(document).scrollTop();

        if ((canScrollHeight - nowScroll) < 100) {
            // TODO 判断页数，去更新新闻数据
            if(data_querying == true){
                if(cur_page<=total_page){
                updateNewsData(currentCid,cur_page)
        }}}
    })
})

function updateNewsData(clickCid,page) {
    // TODO 更新新闻数据
    data_querying = false
    $.get(
        'newslist',
        {
            'class_id':clickCid,
            'page':page
        },
        function(data){
            vue_list_con.news_list=vue_list_con.news_list.concat(data.news)
            total_page = data.totle_page
            cur_page++
            data_querying = true
        }
    )
}
