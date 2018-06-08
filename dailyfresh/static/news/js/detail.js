// function getCookie(name) {
//     var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
//     return r ? r[1] : undefined;
// }


$(function(){
    comment_list()
    vue_comment_list = new Vue({
        el: '.comment_list_con',
        delimiters: ['[[', ']]'],
        data: {
            comments: []
        }
    });
    function comment_list(){
        $.get(
            'comment_list',
            {
            'news_id':$('#news_id').val()
            },
            function(data){
                vue_comment_list.comments = data.comment_list
            }

        )
    }
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
    // 收藏
    $("#collection2").click(function () {
        $.get(
            'collect',
            {
                'news_id':$('#news_id').val() 
            },
            function(data){
                if(data.result==1){
                    $('#collection2').hide()
                    $('#collection1').hide()
                    $('.collected').show()
                }
            }
        )
       
    })
    // 取消收藏
    $(".collected").click(function () {
        console.log(123)
        $.get(
            'collected',
            {
                'news_id':$('#news_id').val() 
            },
            function(data){
                if(data.result==1){
                    $('.collected').hide()
                    $('#collection2').show()
                    $('#collection1').hide()
                }
            }
        )
       
    })
     

        // 评论提交
    $("#comment_form").submit(function (e) {
        e.preventDefault();
        if($('#comment_input').val()==''){
            console.log('评论不能为空')
            return
        }
        $.post(
            'comment',
            {
                'csrf_token':$('#csrf_token').val(),
                'comment':$('#comment_input').val(),
                'news_id':$('#news_id').val()
            },
            function(data){
                if(data.result==1){
                comment_list()
                $('#comment_input').val('')
                $('#comment_count').html( Number($('#comment_count').html()) + 1)
            }
            }
        )
    })

    $('.comment_list_con').delegate('a,input','click',function(){

        var sHandler = $(this).prop('class');

        if(sHandler.indexOf('comment_reply')>=0)
        {
            $(this).next().toggle();
        }

        if(sHandler.indexOf('reply_cancel')>=0)
        {
            $(this).parent().toggle();
        }

        if(sHandler.indexOf('comment_up')>=0)
        {
            var $this = $(this);
            if(sHandler.indexOf('has_comment_up')>=0)
            {
                // 如果当前该评论已经是点赞状态，再次点击会进行到此代码块内，代表要取消点赞
                $.post(
                    'click_like',
                    {   
                        'csrf_token':$('#csrf_token').val(),
                        'commentid':$this.attr('comment'),
                        'action':0
                    },function(data){
                        $this.text(data.like_cout)
                        $this.removeClass('has_comment_up')
                        $this.addClass('comment_up')
                    }
                )
            }else {
                $.post(
                    'click_like',
                    {   
                        'csrf_token':$('#csrf_token').val(),
                        'commentid':$this.attr('comment'),
                        'action':1
                    },function(data){
                        $this.text(data.like_cout)
                        $this.removeClass('comment_up')
                        $this.addClass('has_comment_up')
                    }
                )
            }
        }

        if(sHandler.indexOf('reply_sub')>=0)
        {   
            $this = $(this)
            $.post(
                'comment_comment',
                {
                    'csrf_token':$('#csrf_token').val(),
                    'msg':$this.prev().val(),
                    'comment_id':$this.attr('comment'),
                    'news_id':$('#news_id').val()
                },
                function(data){
                    if(data.result==1){
                    comment_list()
                    $('#comment_count').html( Number($('#comment_count').html()) + 1)
                    $this.parent().hide()
                    $this.prev().val('')
                }
                }
            )
        }
    })

        // 关注当前新闻作者
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
                    $('.follows>b').text(Number($('.follows>b').text())+1)
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
                    $('.follows>b').text(Number($('.follows>b').text())-1)
                    $('.focused').hide()
                    $('.focus').show()
                }
            })
    })
})