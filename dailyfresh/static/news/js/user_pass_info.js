// function getCookie(name) {
//     var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
//     return r ? r[1] : undefined;
// }


$(function () {
    $(".pass_info").submit(
        function (e){
        e.preventDefault()
        var old_pwd = $("#old_pwd").val()
        var new_pwd = $("#new_pwd").val()
        var check_new_pwd = $("#check_new_pwd").val()

        if (!old_pwd) {
            alert('当前密码不能为空')
            return
        }
        if (!new_pwd) {
            alert('新密码不能为空')
            return
        }
        if (!check_new_pwd) {
            alert('新密码不能为空')
            return
        }
        if (new_pwd != check_new_pwd) {
            alert('两次输入的密码不同')
            return
        }
        $.post(
            'user_pass_info',
            {
                'csrf_token':$('#csrf_token').val(),
                'old_pwd':old_pwd,
                'new_pwd':new_pwd,
            },
            function(data){
                if(data.result == '1'){
                    alert('success')
                    $("#old_pwd").val('')
                    $("#new_pwd").val('')
                    $("#check_new_pwd").val('')
                }else if(data.result=='3'){
                    alert('密码格式有误')
                    $("#new_pwd").val('')
                    $("#check_new_pwd").val('')
                }else if(data.result=='2'){
                    alert('旧密码错误')
                    $("#old_pwd").val('')
                }
            })
        })
})