// 解析url中的查询字符串
function decodeQuery(){
    var search = decodeURI(document.location.search);
    return search.replace(/(^\?)/, '').split('&').reduce(function(result, item){
        values = item.split('=');
        result[values[0]] = values[1];
        return result;
    }, {});
}

// news_collect
$(function(){
    $(".focus").click(function () {
        $.post(
            'follow',
            {
                'csrf_token':$('#csrf_token').val(),
                'action':1,
                'author':$('.author_card').attr('author')
            },
            function(data){
                if(data.result==1){
                    $('.login_btn').click()
                }else if(data.result==2){
                    $('.focus').hide()
                    $('.focused').show()
                }
            })})

    // 取消关注当前新闻作者
    $(".focused").click(function () {
        $.post(
            'follow',
            {
                'csrf_token':$('#csrf_token').val(),
                'action':2,
                'author':$('.author_card').attr('author')
            },
            function(data){
                if(data.result==1){
                    $('.login_btn').click()
                }else if(data.result==2){
                    $('.focused').hide()
                    $('.focus').show()
                }
            })
    })
    $(".login_form_con").submit(function (e) {
        e.preventDefault()
        var mobile = $("#mobile").val()
        var password = $("#password").val()
        var csrf_token = $('#csrf_token').val()
        if (!mobile) {
            $("#login-mobile-err").show();
            e.preventDefault()
            return;
        }

        if (!password) {
            $("#login-password-err").show();
            e.preventDefault()
            return;
        }

        // 发起登录请求
        $.post('/news/login',
        {
            'csrf_token': csrf_token,
            'mobile':mobile,
            'password':password

        },data=>{
            if(data.state=='failure'){
                alert('error')
            }
            else if (data.state=='success'){
            $(this).hide()
            $('#user_btnsfr').hide()
            $('#nick_name').text(data.nick_name)
            $('.user_pic').attr('src',data.avatar_get)
            $('#user_loginfr').show()
            $('.comment_form_logout').hide()
            $('.comment_form').show()
            $('.comment_form img').attr('src',data.avatar_get)
            window.location.reload()
        }
        })
    })
})
