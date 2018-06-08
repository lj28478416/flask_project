$(function(){

	// 打开登录框
	$('.login_btn').click(function(){
        $('.login_form_con').show();
	})
	
	// 点击关闭按钮关闭登录框或者注册框
	$('.shutoff').click(function(){
		$(this).closest('form').hide();
	})

    // 隐藏错误
    $(".login_form #mobile").focus(function(){
        $("#login-mobile-err").hide();
    });
    $(".login_form #password").focus(function(){
        $("#login-password-err").hide();
    });

    $(".register_form #mobile").focus(function(){
        $("#register-mobile-err").hide();
    });
    $(".register_form #imagecode").focus(function(){
        $("#register-image-code-err").hide();
    });
    $(".register_form #smscode").focus(function(){
        $("#register-sms-code-err").hide();
    });
    $(".register_form #password").focus(function(){
        $("#register-password-err").hide();
    });


	// 点击输入框，提示文字上移
	$('.form_group').on('click focusin',function(){
        (()=>{
            $(this).siblings().removeClass('hotline');
            for(var i = 0 ; i < $(this).siblings().length;i++){
            var val = $(this).siblings('.form_group').eq(i).children('input').val();
            if(val=='')
            {
                $(this).siblings('.form_group').eq(i).children('.input_tip').animate({'top':22,'font-size':14},'fast');
            }}
        })()
        $(this).children('.input_tip').animate({'top':-5,'font-size':12},'fast').siblings('input').focus()
    })
    $('.form_group input').focus(
        function(){
            $(this).parent().addClass('hotline')
            return false
        })

	// 打开注册框
	$('.register_btn').click(function(){
		$('.register_form_con').show();
	})


	// 登录框和注册框切换
	$('.to_register').click(function(){
		$('.login_form_con').hide();
		$('.register_form_con').show();
	})

	// 登录框和注册框切换
	$('.to_login').click(function(){
		$('.login_form_con').show();
		$('.register_form_con').hide();
	})

	// 根据地址栏的hash值来显示用户中心对应的菜单
	var sHash = window.location.hash;
	if(sHash!=''){
		var sId = sHash.substring(1);
		var oNow = $('.'+sId);		
		var iNowIndex = oNow.index();
		$('.option_list li').eq(iNowIndex).addClass('active').siblings().removeClass('active');
		oNow.show().siblings().hide();
	}

	// 用户中心菜单切换
	var $li = $('.option_list li');
	var $frame = $('#main_frame');

	$li.click(function(){
		if($(this).index()==5){
			$('#main_frame').css({'height':900});
		}
		else{
			$('#main_frame').css({'height':660});
		}
		$(this).addClass('active').siblings().removeClass('active');

	})

    // TODO 登录表单提交
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
        }
        })
    })

    // TODO 注册按钮点击
    $(".register_form_con").submit(function (e) {
        // 阻止默认提交操作
        e.preventDefault()

		// 取到用户输入的内容
        var mobile = $("#register_mobile").val()
        var smscode = $("#smscode").val()
        var password = $("#register_password").val()
        var imageCode = $("#imagecode").val();

		if (!mobile) {
            $("#register-mobile-err").show();
            return;
        }
        if (!smscode) {
            $("#register-sms-code-err").show();
            return;
        }
        if (!password) {
            $("#register-password-err").html("请填写密码!");
            $("#register-password-err").show();
            return;
        }

		if (password.length < 6) {
            $("#register-password-err").html("密码长度不能少于6位");
            $("#register-password-err").show();
            return;
        }

        // 发起注册请求
        // 因为页面是用了框架,框架是一种跨域请求方式,所以jquery自动将post请求变成了get
        $.post(
            '/news/register',
            {
                'sms_code':smscode,
                'mobile':mobile,
                'pwd':password,
                'pic_code':imageCode,
                'csrf_token': $('#csrf_token').val()
            },
            function(data){
                if(data.result == 1){
                    console.log('有空数据')
                }else if(data.result == 2){
                    console.log('手机号已存在')
                }else if(data.result == 3){
                    console.log('验证码错误')
                }else if(data.result == 4){
                    console.log('手机验证码错误')
                }else if(data.result == 5){
                    console.log('密码不符合规则')
                }else if(data.result == 6){
                    $(window).attr('location','/news/user');
                }
            }
        )

    })
})

var imageCodeId = ""

// TODO 生成一个图片验证码的编号，并设置页面中图片验证码img标签的src属性
function generateImageCode() {
    $('.get_pic_code').attr('src',$('.get_pic_code').attr('src') + 1)
}

// 发送短信验证码
function sendSMSCode() {
    // 校验参数，保证输入框有数据填写
    $(".get_code").removeAttr("onclick");
    var mobile = $("#register_mobile").val();
    if (!mobile) {
        $("#register-mobile-err").html("请填写正确的手机号！");
        $("#register-mobile-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }
    var imageCode = $("#imagecode").val();
    if (!imageCode) {
        $("#image-code-err").html("请填写验证码！");
        $("#image-code-err").show();
        $(".get_code").attr("onclick", "sendSMSCode();");
        return;
    }
    // TODO 发送短信验证码
    $.post(
        '/news/sms_verify',
        {   
            "csrf_token":$('#csrf_token').val(),
            "mobile":mobile,
            "pic_code":imageCode
        },
        function(data){
            console.log(data.result)
            if(data.result==3){
                console.log('手机号有误')
            }else if(data.result==1){
                console.log('图片验证码错误')
            }else if(data.result==2){
                console.log(data.code)
            }
            $(".get_code").attr("onclick", "sendSMSCode();");
        }
    )
}

// 调用该函数模拟点击左侧按钮
function fnChangeMenu(n) {
    var $li = $('.option_list li');
    if (n >= 0) {
        $li.eq(n).addClass('active').siblings().removeClass('active');
        // 执行 a 标签的点击事件
        $li.eq(n).find('a')[0].click()
    }
}

// 一般页面的iframe的高度是660
// 新闻发布页面iframe的高度是900
function fnSetIframeHeight(num){
	var $frame = $('#main_frame');
	$frame.css({'height':num});
}

function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}

function generateUUID() {
    var d = new Date().getTime();
    if(window.performance && typeof window.performance.now === "function"){
        d += performance.now(); //use high-precision timer if available
    }
    var uuid = 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
        var r = (d + Math.random()*16)%16 | 0;
        d = Math.floor(d/16);
        return (c=='x' ? r : (r&0x3|0x8)).toString(16);
    });
    return uuid;
}
