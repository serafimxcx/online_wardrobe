$(function(){
           
    $("#btn_next1").click(function(){
        if($("#txt_name").val().trim() == ""){
            $("#message").text("Please enter a value.");
        }else{
            $("#setup_div1").css({"display":"none"});
            $("#setup_div2").css({"display":"block"});
        }
    });

    $("#btn_back2").click(function(){  
        $("#setup_div1").css({"display":"block"});
        $("#setup_div2").css({"display":"none"});
        
    });

    $("#btn_next2").click(function(){
        if($("#imageUpload").get(0).files.length === 0){
            $("#selectedimg").text("Please choose an image.");
        }else{
            $("#setup_div2").css({"display":"none"});
            $("#setup_div3").css({"display":"block"});
        }
    });


    $("#btn_back3").click(function(){  
        $("#setup_div2").css({"display":"block"});
        $("#setup_div3").css({"display":"none"});
        
    });

    $("#btn_next3").click(function(){
        if($("#txt_birthdate").val() == ""){
            $("#message2").text("Please specify your birthdate.");
        }else{
            var birthdate = $("#txt_birthdate").val();
            var today = new Date();
            var birthDate = new Date(birthdate);
            var age = today.getFullYear() - birthDate.getFullYear();
            var monthDifference = today.getMonth() - birthDate.getMonth();

            if (monthDifference < 0 || (monthDifference === 0 && today.getDate() < birthDate.getDate())) {
                age--;
            }

            if (age < 12) {
                $("#message2").text("You must be at least 12 years old.");
            } else {
                $("#setup_div3").css({"display":"none"});
                $("#setup_div4").css({"display":"block"});
            }
        }
    });

    $("#btn_back4").click(function(){  
        $("#setup_div3").css({"display":"block"});
        $("#setup_div4").css({"display":"none"});
        
    });
    
    $("#btn_next4").click(function(){
        if($("#txt_weight").val() == ""){
            $("#message3").text("Please specify your weight.");
            $("#txt_weight").focus();
        }else if($("#txt_height").val() == ""){
            $("#message3").text("Please specify your height.");
            $("#txt_height").focus();
        }else if($("#slct_bodyshape").val() == ""){
            $("#message3").text("Please specify your body shape.");
            $("#slct_bodyshape").focus();
        }else{
            $("#setup_div4").css({"display":"none"});
            $("#setup_div5").css({"display":"block"});
        }
    });

    $("#btn_back5").click(function(){  
        $("#setup_div4").css({"display":"block"});
        $("#setup_div5").css({"display":"none"});
        
    });

    $("#btn_next5").click(function(){
        var checkedCount = $("input[name='slct_color']:checked").length;
            if (checkedCount < 3) {
                $("#message4").text("Please select at least three colors.");
            }else{
            $("#setup_div5").css({"display":"none"});
            $("#setup_div6").css({"display":"block"});
        }
    });

    $("#btn_back6").click(function(){  
        $("#setup_div5").css({"display":"block"});
        $("#setup_div6").css({"display":"none"});
        
    });

    $("#btn_next6").click(function(){
        var checkedCount = $("input[name='slct_style']:checked").length;
            if (checkedCount < 3) {
                $("#message5").text("Please select at least three styles.");
            }else{
            $("#setup_div6").css({"display":"none"});
            $("#setup_div7").css({"display":"block"});
        }
    });

    $("#btn_back7").click(function(){  
        $("#setup_div6").css({"display":"block"});
        $("#setup_div7").css({"display":"none"});
        
    });

    $("#btn_save").click(function(){  
        if(confirm("Are you sure you want to save? ")){
            $("#setupForm").submit();
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