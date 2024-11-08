$(function(){
    setTimeout(function() {
        $('.messages').fadeOut('slow');
    }, 2000);


    $(".btn_category").click(function(){
        category = $(this).attr("category_name");
        
        window.location.href="/wardrobe/"+category;
    })

    $("#btn_addnew_modal").click(function(){
        $("#btn_submit_item").css({"display":"block"})
        $("#btn_cancel_submit_item").css({"display":"block"})
        $("#btn_addnew_modal").css({"display":"none"})
        $(".outfit_container").css({"display":"none"})
        $("#additem_container").css({"display":"block"})
        $(".item_container").css({"display":"none"})

    })

    $("#btn_cancel_submit_item").click(function(){
        window.location.reload();
    })

    $('#file-upload').change(function() {
        var file = $(this)[0].files[0];
        
        if (file) {
            $('#file-name-output').html('<i class="bi bi-arrow-up-right-square"></i> Selected file: ' + file.name);
        } else {
            $('#file-name-output').html('');
        }

        var input = event.target;
        if (input.files && input.files[0]) {
            var reader = new FileReader();
            reader.onload = function(e) {
                $('#preview-image').attr('src', e.target.result);
            }
            reader.readAsDataURL(input.files[0]);
        }
    });

    $('#file-name-output').click(function(){
        $("#preview_image_modal").css({"display":"flex"});
    });

    $("#preview_image_modal").click(function(){
        $("#preview_image_modal").css({"display":"none"});
    });

    $(".img_outfit_col").click(function(){
        var id = $(this).attr('id');
        $("#item_container"+id).css({"display":"flex"});
        $("#btn_addnew_modal").css({"display":"none"});
        $(".item_container").not("#item_container"+id).css({"display":"none"});
        $(".outfit_container").css({"display":"none"})
    });

    $(".btn_back").click(function(){
        $(".item_container").css({"display":"none"});
        $("#btn_addnew_modal").css({"display":"block"});
        $(".outfit_container").css({"display":"flex"})
    });

    $(".btn_delete_item").click(function(){
        var id = $(this).attr("id");
        $("#txt_del_item_id").val(id);   
        $("#delete_item_modal").css({"display":"flex"});
    });

    $("#btn_delete_no").click(function(){
        $("#delete_item_modal").css({"display":"none"});
    });

    $(".btn_edit").click(function(){
        var itemID = $(this).attr("id");
        var category = $(this).attr("category").toLowerCase();
    
        $.ajax({
            url: '/get_item/' + itemID,
            type: "GET",
            success: function(response){
                $("#btn_submit_item").css({"display":"block"});
                $("#btn_cancel_submit_item").css({"display":"block"});
                $("#btn_addnew_modal").css({"display":"none"});
                $(".outfit_container").css({"display":"none"});
                $("#additem_container").css({"display":"block"});
                $(".item_container").css({"display":"none"});
                $("#add_item_form").attr("action", "/edit_item/"+category);

                $("#txt_outfitname").val(response.outfit_name);
                $("#slct_subcategory").empty();

                var subcategories = JSON.parse(response.subcategories_optn);
                
                subcategories.forEach(function(subcategory) {
                    $("#slct_subcategory").append("<option value='" + subcategory.fields.name + "'>" + subcategory.fields.name + "</option>");
                });

                $("#slct_subcategory").val(response.subcategory);
                $("#slct_color").val(response.color);

                $('#preview-image').attr('src', response.image);
                $('#file-name-output').html('<i class="bi bi-arrow-up-right-square"></i> Selected file: ' + response.image);

                $("#slct_genderedstyle").val(response.gendered_style);

                $.each(response.styles, function(index, styleId) {
                    $('#style' + styleId).prop('checked', true);
                });

                $("#txt_desc").val(response.desc);

                $("#btn_submit_item").html("<i class='bi bi-check2'></i> Save Edited Item");
                $("#txt_item_id").val(itemID);

                $('#file-upload').removeAttr('required');

                
            },
            error: function (XMLHttpRequest, textStatus, errorThrown) {
                console.log('XHR ERROR ' + XMLHttpRequest.status);
                return JSON.parse(XMLHttpRequest.responseText);
            }
            
        });
    });




})