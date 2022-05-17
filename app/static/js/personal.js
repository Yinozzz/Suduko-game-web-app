function show_upload_form(){
    document.getElementById("upload_head_pic_form").style.display="block"
}

$(document).ready(function(){
    $('#upload_head_pic_form').submit(function(e){
        e.preventDefault();

        var image_data = new FormData($("#upload_head_pic_form")[0]);
        console.log(image_data)
            $.ajax({
                type: 'post',
                url: '/avatar',
                data: image_data,
                processData: false,
                contentType: false,
                success: function(resp){
                    alert("success")
                }
            });
    });
});