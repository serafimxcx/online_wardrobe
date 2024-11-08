$(document).ready(function () {
    var startDate, endDate;

    var calendar = $('#calendar').fullCalendar({
        header: {
            left: 'prev,next today',
            center: 'title',
            right: 'month,agendaWeek,agendaDay'
        },
        events: '/all_events',
        selectable: true,
        selectHelper: true,
        editable: true,
        eventLimit: true,
        select: function (start, end, allDay) {
            startDate = $.fullCalendar.formatDate(start, "Y-MM-DD HH:mm:ss");
            endDate = $.fullCalendar.formatDate(end, "Y-MM-DD HH:mm:ss");
            $("#addEventModal").css("display", "flex");
            // Save event when clicking the save button
             
        },
        eventResize: function (event) {
            var start = $.fullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
            var end = $.fullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");    
            var id = event.id;
            $.ajax({
                type: "GET",
                url: '/update_event',
                data: {'start': start, 'end': end, 'id': id},
                dataType: "json",
                success: function (data) {
                    calendar.fullCalendar('refetchEvents');
                    alert('Event Update');
                },
                error: function (data) {
                    alert('There is a problem!!!');
                }
            });
        },

        eventDrop: function (event) {
            var start = $.fullCalendar.formatDate(event.start, "Y-MM-DD HH:mm:ss");
            var end = $.fullCalendar.formatDate(event.end, "Y-MM-DD HH:mm:ss");
            var id = event.id;
            $.ajax({
                type: "GET",
                url: '/update_event',
                data: {'start': start, 'end': end, 'id': id},
                dataType: "json",
                success: function (data) {
                    calendar.fullCalendar('refetchEvents');
                    alert('Event Update');
                },
                error: function (data) {
                    alert('There is a problem!!!');
                }
            });
        },

        eventClick: function (event) {
            var startDate = moment(event.start);
            var endDate = moment(event.end);
            var daysDifference = endDate.diff(startDate, 'days');
            $("#event_title").text(event.title);
            if (daysDifference == 1 && event.start.format("HH:mm:ss") === "00:00:00" && event.end.format("HH:mm:ss") === "00:00:00") {
                $("#eventTime").html("All day");
            } else {
                var startTime = moment(event.start);
                var endTime = moment(event.end);
            
                var formattedStartTime = startTime.format("MMMM DD, YYYY - h:mm a");
                if(daysDifference > 1){
                    var formattedEndTime = endTime.format("MMMM DD, YYYY - h:mm a");
                }else{
                    var formattedEndTime = endTime.format("h:mm a");
                }
                
            
                // Combine formatted start and end times
                var formattedTimeRange = formattedStartTime + " to " + formattedEndTime;
                
                
                if(daysDifference > 1){
                    $("#eventTime").html("<b>Time</b>: " + formattedTimeRange + "<br><b>Duration: </b>"+ daysDifference +" Days");
                }else{
                    $("#eventTime").html("<b>Time</b>: " + formattedTimeRange);
                }
            }

            $('.plan_outfit_container3').find('tr').empty();

            var container = $('.plan_outfit_container3').find('tr');

            var eventHTML = '';
                
                // Loop through each user outfit in the event
                $.each(event.user_outfits, function(index, outfit) {
                    eventHTML += `<td>${generateOutfitHTML(outfit)}</td>`;
                });
                
                // Append the generated HTML for the event to the container
                container.append(eventHTML);
        
            $("#eventDetailsModal").css("display", "flex");
            $("#event_id").val(event.id);
            
        },

    });

     // Close modal when clicking the close button
     $(".btn_close").click(function () {
        $("#addEventModal").css("display", "none");
        $("#eventDetailsModal").css("display", "none");
     });

     // Close modal when clicking outside of it
     $("#addEventModal").click(function (event) {
         if (event.target == $("#addEventModal")[0]) {
             $("#addEventModal").css("display", "none");
         }
     });

     $("#eventDetailsModal").click(function (event) {
        
        if (event.target == $("#eventDetailsModal")[0]) {
            $("#eventDetailsModal").css("display", "none");
        }
    });

    $(".outfit_container2").click(function(){
        // Toggle the 'clicked' class and border
        $(this).toggleClass("clicked").css("border", function() {
            return $(this).hasClass("clicked") ? "2px solid black" : "none";
        });
    
        // Initialize an array to store selected outfit IDs
        var selectedOutfits = [];
    
        // Iterate over all clicked outfit containers
        $(".outfit_container2.clicked").each(function() {
            // Push the outfit ID to the selectedOutfits array
            selectedOutfits.push($(this).attr("outfit_id"));
        });
    
        // Set the value of #eventOutfit input
        $("#eventOutfit").val(selectedOutfits.join(","));
    });

    $("#saveEvent").click(function () {
        var title = $("#eventTitle").val();
        var outfit = $("#eventOutfit").val();
        if (title) {
            
            $.ajax({
                type: "GET",
                url: '/add_event',
                data: { 'title': title, 'start': startDate, 'end': endDate, 'eventOutfit': outfit },
                dataType: "json",
                success: function (data) {
                    calendar.fullCalendar('refetchEvents');
                    alert("Added Successfully");
                    $("#addEventModal").css("display", "none");
                    $("#eventTitle").val("");
                    $("#eventOutfit").val("");
                },
                error: function (data) {
                    alert('There is a problem!!!');
                }
            });
        } else {
            alert('Please enter event title and select a date range.');
        }
    });


      $("#deleteEvent").click(function () {
        var event_id = $("#event_id").val();
        if (confirm("Are you sure you want to delete this event?")) {
            $.ajax({
                type: "GET",
                url: '/remove_event',
                data: {'id': event_id},
                dataType: "json",
                success: function (data) {
                    calendar.fullCalendar('refetchEvents');
                    $("#eventDetailsModal").css("display", "none");
                    alert('Event Removed');
                  
                },
                error: function (data) {
                    alert('There is a problem!!!');
                }
            });
        }
    });
    

    function generateOutfitHTML(outfit) {
        var outfitHTML = `
            <a href="/outfit_details/${outfit.id}"><div class="event_outfits event_outfit_container2">`;
            if (outfit.outerwear.image) {
                outfitHTML += `<img src="${outfit.outerwear.image}" class="img_item_outfit" id="img_outerwear" alt="Outerwear Image">`;
            }
            outfitHTML +=`
            <img src="${outfit.top.image}" class="img_item_outfit" id="img_top" alt="Top Image"><br><br><br>
            <img src="${outfit.bottom.image}" class="img_item_outfit" id="img_bottom" alt="Bottom Image"><br><br><br>
            <img src="${outfit.footwear.image}" class="img_item_outfit" id="img_footwear" alt="Footwear Image"><br><br><br>
        `;   
        
        outfitHTML += `
                <h5 class="outfit_title">${outfit.outfit_name}</h5>
            </div></a>
        `;
        
        return outfitHTML;
    }

     
});