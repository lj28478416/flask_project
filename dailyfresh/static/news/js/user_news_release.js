// function getCookie(name) {
//     var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
//     return r ? r[1] : undefined;
// }


$(function () {

    $(".release_form").submit(function (e) {
        e.preventDefault()
        $(this).ajaxSubmit({
            url: "",
            type: "post",
            dataType: "json",
            success: function(data){
                if(data.result=='error'){
                    $('#error').text('每一项都不能为空')
                    $('#error').show()
                }else 
                if(data.result=='success'){
                    window.parent.fnChangeMenu(6)
                    window.parent.scrollTo(0, 0)
                    // location.href = 'user_news_list'
                }
            }
        })
        })
        // TODO 发布完毕之后需要选中我的发布新闻
        // 选中索引为6的左边单菜单

        // // 滚动到顶部

    })