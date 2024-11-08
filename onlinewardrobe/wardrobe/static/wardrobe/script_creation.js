$(function(){
    var fromSmartReco = false;

    setTimeout(function() {
        $('.messages').fadeOut('slow');
    }, 2000);
    
    $("#message").css({"display":"none"});


    $("#btn_createoutfit").click(function(){
        $(".outfits_container").css({"display":"none"});
        $(".create_outfit_container").css({"display":"block"});
        $("#tops_container").css({"display":"block"});

    });

    $(".btn_back").click(function(){
        window.location.href = "/outfit_creation"; 

    });

    $(".btn_delete_outfit").click(function(){
        var outfit_id = $(this).attr("id");
        $("#txt_del_outfit_id").val(outfit_id);   
        $("#delete_item_modal").css({"display":"flex"});

    });

    $("#btn_delete_no").click(function(){
        $("#delete_item_modal").css({"display":"none"});
    });

    $("#btn_back1").click(function(){
        window.location.reload();

    });

    $("#btn_next1").click(function(){
        if($("#c_top").val() == ""){
            $("#message").css({"display":"block"});

            setTimeout(function() {
                $('#message').fadeOut('slow');
            }, 2000);
        }else{
            $("#tops_container").css({"display":"none"});
            $("#bottoms_container").css({"display":"block"});
        }
        

        
    });

    $("#btn_back2").click(function(){
        $("#tops_container").css({"display":"block"});
        $("#bottoms_container").css({"display":"none"});
    });

    $("#btn_next2").click(function(){
        if($("#c_bottom").val() == ""){
            $("#message").css({"display":"block"});

            setTimeout(function() {
                $('#message').fadeOut('slow');
            }, 2000);
        }else{
            $("#footwears_container").css({"display":"block"});
            $("#bottoms_container").css({"display":"none"});
        }
        
    });

    $("#btn_back3").click(function(){
        $("#bottoms_container").css({"display":"block"});
        $("#footwears_container").css({"display":"none"});
    });

    $("#btn_next3").click(function(){
        if($("#c_footwear").val() == ""){
            $("#message").css({"display":"block"});

            setTimeout(function() {
                $('#message').fadeOut('slow');
            }, 2000);
        }else{
            $("#outerwears_container").css({"display":"block"});
            $("#footwears_container").css({"display":"none"});
        }
        
    });

    $("#btn_next0").click(function(){
        
        $("#footwears_container").css({"display":"block"});
        $("#tops_container").css({"display":"none"});
          
    });

    $("#btn_back0").click(function(){
        window.location.reload();
          
    });


    $("#btn_back4").click(function(){
        $("#footwears_container").css({"display":"block"});
        $("#outerwears_container").css({"display":"none"});
    });

    $("#btn_next4").click(function(){
        
        $("#accessories_container").css({"display":"block"});
        $("#outerwears_container").css({"display":"none"});
        
        
    });

    $("#btn_next5").click(function(){
        $("#namedesc_container").css({"display":"block"});
        $("#accessories_container").css({"display":"none"});
    });

    $("#btn_back5").click(function(){
        if(fromSmartReco){
            $("#smartcreate_value_container").css("display","block");
            $("#accessories_container").css({"display":"none"});
            $(".create_outfit_container").css({"display":"none"});
            fromSmartReco = false;
        }else{
            $("#outerwears_container").css({"display":"block"});
            $("#accessories_container").css({"display":"none"});
        }
        
    });

    $("#btn_back6").click(function(){
        $("#accessories_container").css({"display":"block"});
        $("#namedesc_container").css({"display":"none"});
    });
    


    //functions to choose image
    $(".img_category_container").hover(
        function() {
            if (!$(this).hasClass("clicked")) {
            $(this).css({"border":"2px solid black"});
            }
        },
        function() {
            if (!$(this).hasClass("clicked")) {
            $(this).css({"border":"none"});
            }
        }
        );

    $(".img_top_container2").click(function(){
        $(".img_top_container2").removeClass("clicked").css({"border":"none"});
        $(this).addClass("clicked").css({"border":"2px solid black"});
      
        top_id = $(this).attr("top_id");
        category = $(this).attr("category");
        subcategory = $(this).attr("subcategory");

        
        if(category == "Dress" || subcategory == "Evening Gown" || subcategory == "Cocktail Dress"){
            $("#btn_next0").css("display","inline-block");
            $("#btn_next1").css("display","none");
        }else{
            $("#btn_next0").css("display","none");
            $("#btn_next1").css("display","inline-block");
        }

        $("#c_top").val(top_id);
      });
      

    $(".img_bottoms_container2").click(function(){
        $(".img_bottoms_container2").removeClass("clicked").css({"border":"none"});
        $(this).addClass("clicked").css({"border":"2px solid black"});
      
        bottom_id = $(this).attr("bottom_id");
        $("#c_bottom").val(bottom_id);
      });
      


    $(".img_footwears_container2").click(function(){
        $(".img_footwears_container2").removeClass("clicked").css({"border":"none"});
        $(this).addClass("clicked").css({"border":"2px solid black"});
      
        footwear_id = $(this).attr("footwear_id");
        $("#c_footwear").val(footwear_id);
      });
      

    $(".img_outerwears_container2").click(function(){
        $(".img_outerwears_container2").removeClass("clicked").css({"border":"none"});
        $(this).addClass("clicked").css({"border":"2px solid black"});
      
        outerwear_id = $(this).attr("outerwear_id");
        $("#c_outerwear").val(outerwear_id);
      });

      $(".img_dress_container2").click(function(){
        $(".img_dress_container2").removeClass("clicked").css({"border":"none"});
        $(this).addClass("clicked").css({"border":"2px solid black"});
      
        dress_id = $(this).attr("dress_id");
        $("#c_dress").val(dress_id);
      });

      $(".img_accessory_container2").click(function(){
        // Toggle the 'clicked' class and border
        $(this).toggleClass("clicked").css("border", function() {
            return $(this).hasClass("clicked") ? "2px solid black" : "none";
        });
    
        // Initialize an array to store selected outfit IDs
        var selectedAccessory = [];
    
        // Iterate over all clicked outfit containers
        $(".img_accessory_container2.clicked").each(function() {
            // Push the outfit ID to the selectedAccessory array
            selectedAccessory.push($(this).attr("accessory_id"));
        });
    
        // Set the value of #eventOutfit input
        $("#c_accessory").val(selectedAccessory.join(","));

        
      });

      $("#btn_no_accessory").click(function() {
            $("#c_accessory").val("");
            $(".img_accessory_container2").each(function() {
                // Check if this container has the 'clicked' class
                if ($(this).hasClass("clicked")) {
                    // Remove the 'clicked' class and border from all containers
                    $(".img_accessory_container2").css("border", "none").removeClass("clicked");
                 
                    
                }
            });
            $(this).css("border", "2px solid black").addClass("clicked");
        });

      $("#btn_smartcreate").click(function(){
        $(".outfits_container").css({"display":"none"});
        $("#smartcreate_container").css("display","block");
      });


    function getRecommendations() {
        var event = $('#slct_event').val();
        if (!event) {
            alert("Please select an event.");
            return;
        }
        $.ajax({
            url: '/smart_recommend',
            data: {
                'event': event
            },
            success: function(data) {
                $("#c_event_type").text(data.event);
                
                $('.plan_outfit_container2').find('tr').empty();

                var container = $('.plan_outfit_container2').find('tr');
                

                var categories = ['top', 'bottom', 'outerwear', 'footwear'];
                var allEmpty = true;
                categories.forEach(function(category) {
                    var item = data[category];
                    if (item) {
                        allEmpty = false;
                        $("#c_"+category).val(item.id); 
                        var outfitHTML = `
                            <td>
                                <div class="smart_event_outfits event_outfit_container2">
                                    <img src="${item.image}" class="img_reco_item">
                                    <h5 class="outfit_title">${item.name}</h5>
                                    <h5>${item.category}</h5>
                                </div>
                            </td>
                        `;
                    } 

                    
                    container.append(outfitHTML);
                });
                
                if (allEmpty) {
                    var outfitHTML = `
                            <td>
                            <div class="smart_event_outfits event_outfit_container2" style='height: 400px;'>
                                <br><br><br><br>
                        
                                <h5>You have no suitable items for this kind of event.</h5><br>
                                <a href='/wardrobe/all'><button type='button' class='default_btn'>Add Items</button></a>
                            </div>
                            </td>
                        `;
                    container.append(outfitHTML);
                }

                $("#smartcreate_container").css("display","none");
                $("#smartcreate_value_container").css("display","block");
            }
        });
    }


    $("#btn_continue_smartreco").click(function(){
        getRecommendations();
    });

    $("#btn_generate_again").click(function(){
        getRecommendations();
    });

    $("#btn_backtoevent").click(function(){
        $("#smartcreate_container").css("display","block");
        $("#smartcreate_value_container").css("display","none");
    });

    $("#btn_continue_smartreco2").click(function(){
        $("#smartcreate_value_container").css("display","none");
        $(".create_outfit_container").css({"display":"block"});
        $("#accessories_container").css({"display":"block"});

        fromSmartReco = true;
    });

    
});

