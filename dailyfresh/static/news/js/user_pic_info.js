function getCookie(name) {
    var r = document.cookie.match("\\b" + name + "=([^;]*)\\b");
    return r ? r[1] : undefined;
}


$(function () {
    $('.pic_info').submit(
        function(e){
            e.preventDefault()
            $(this).ajaxSubmit({
                url: "user_pic_info",
                type: "post",
                dataType: "json",
                success: function(data){
                    $('img').attr('src',data.result)
                    $('.user_pic',window.parent.document).attr('src',data.result)
                }
            })
        }
    )
})