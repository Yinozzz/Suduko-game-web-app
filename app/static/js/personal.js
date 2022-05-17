function show_upload_form(){
    is_display = document.getElementById("upload_head_pic_form").style.display
    if (is_display == 'block')
        document.getElementById("upload_head_pic_form").style.display="none"
    else{
        document.getElementById("upload_head_pic_form").style.display="block"
    }
}

$(document).ready(function(){
    $('#upload_head_pic_form').submit(function(e){
        e.preventDefault();
        if ($("#headpic_input").get(0).files[0]) {
            var image_data = new FormData($("#upload_head_pic_form")[0]);
            $.ajax({
                type: 'post',
                url: '/avatar',
                data: image_data,
                processData: false,
                contentType: false,
                success: function(resp){
                    document.getElementById("upload_head_pic_form").style.display="none"
                    $('#current_avatar').attr('src', resp)
                    $('#change_pic').attr('src', resp)
                }
            });
        }else{
            alert("please upload your head picture")
        }
    });
});