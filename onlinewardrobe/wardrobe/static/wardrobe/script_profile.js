$(function(){
    

    $("#btn_editprof").click(function (event) {
        $("#editprof_modal").css("display", "flex");
    });
    
    $("#editprof_modal").click(function (event) {
        if (event.target == $("#editprof_modal")[0]) {
            location.reload();
        }
    });

    $("#profileImage").click(function(e) {
        $("#imageUpload").click();
    });

    $("#imageUpload").change(function(){
        var fileInput = $("#imageUpload");
        var file = fileInput[0].files[0];
        $("#selectedimg").text(file.name);

        const fileimg = this.files[0];
        if (fileimg){
          let reader = new FileReader();
          reader.onload = function(event){
            $('#profileImage').attr('src', event.target.result);
          }
          reader.readAsDataURL(fileimg);
        }
    });
});