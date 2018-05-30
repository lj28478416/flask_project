// function getCookie(name) {
//     var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
//     return r ? r[1] : undefined;
// }

$(function () {
    $(".base_info").submit(
        function (e){
        e.preventDefault()
        var signature = $("#signature").val()
        var nick_name = $("#nick_name").val()
        var gender = $('input[name="gender"]:checked').val()
        if (!nick_name) {
            alert('请输入昵称')
            return
        }
        if (!gender) {
            alert('请选择性别')
            return
        }
        $.post(
            'user_base_info',
            {
                'csrf_token':$('#csrf_token').val(),
                'signature':signature,
                'nick_name':nick_name,
                'gender':gender
            },
            function(data){
                $('#nick_name', window.parent.document).text(data.result)
                $('.user_center_name', window.parent.document).text(data.result)    
            })
        })
})