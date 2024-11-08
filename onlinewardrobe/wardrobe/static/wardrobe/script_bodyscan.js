$(document).ready(function() {
    const video = $('#video')[0];
    const outputCanvas = $('#output')[0];
    let net;

    async function setupBodyPix() {
        net = await bodyPix.load();
        renderFrame();
        return net;
    }

    async function renderFrame() {
        const segmentation = await net.segmentPerson(video);
        const canvas = $('<canvas></canvas>')[0];
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        const ctx = canvas.getContext('2d');
        ctx.drawImage(video, 0, 0);
    
        if (segmentation && segmentation.allPoses && segmentation.allPoses.length > 0) {
            const mask = bodyPix.toMask(segmentation);
            ctx.lineWidth = 2;
            ctx.strokeStyle = 'red';
            bodyPix.drawMask(canvas, video, mask, 0.5);
        
            const maskData = segmentation.allPoses[0].keypoints;
            const leftShoulder = maskData.find(part => part.part === 'leftShoulder');
            const rightShoulder = maskData.find(part => part.part === 'rightShoulder');
            const leftWrist = maskData.find(part => part.part === 'leftWrist'); 
            const rightWrist = maskData.find(part => part.part === 'rightWrist'); 
            const leftHip = maskData.find(part => part.part === 'leftHip');
            const rightHip = maskData.find(part => part.part === 'rightHip');
        
            drawIndicator(ctx, leftShoulder.position.x, leftShoulder.position.y, 'leftShoulder');
            drawIndicator(ctx, rightShoulder.position.x, rightShoulder.position.y, 'rightShoulder');
            drawIndicator(ctx, leftWrist.position.x, leftWrist.position.y, 'leftWrist'); 
            drawIndicator(ctx, rightWrist.position.x, rightWrist.position.y, 'rightWrist'); 
            drawIndicator(ctx, leftHip.position.x, leftHip.position.y, 'leftHip');
            drawIndicator(ctx, rightHip.position.x, rightHip.position.y, 'rightHip');
        }
    
        outputCanvas.getContext('2d').drawImage(canvas, 0, 0);
        requestAnimationFrame(renderFrame);
    }
    
    async function calculateMeasurements(segmentation, heightCm) {
        if (!segmentation || !segmentation.allPoses || segmentation.allPoses.length === 0) {
            console.error("Segmentation data is missing or invalid:", segmentation);
            return null;
        }
    
        const mask = segmentation.allPoses[0].keypoints;
        const leftShoulder = mask.find(part => part.part === 'leftShoulder');
        const rightShoulder = mask.find(part => part.part === 'rightShoulder');
        const leftWrist = mask.find(part => part.part === 'leftWrist'); 
        const rightWrist = mask.find(part => part.part === 'rightWrist'); 
        const leftHip = mask.find(part => part.part === 'leftHip');
        const rightHip = mask.find(part => part.part === 'rightHip');
    
        const heightPx = $('#video')[0].videoHeight;
        const scale = heightCm / heightPx;
        const shoulderWidthCm = Math.abs(leftShoulder.position.x - rightShoulder.position.x) * scale;
        const waistWidthCm = Math.abs(leftWrist.position.x - rightWrist.position.x) * scale;
        const hipWidthCm = Math.abs(leftHip.position.x - rightHip.position.x) * scale;
    
        return { shoulderWidthCm, waistWidthCm, hipWidthCm };
    }

    function classifyBodyShape(shoulderWidthCm, waistWidthCm, hipWidthCm) {
       
        var waistToHipRatio = waistWidthCm / hipWidthCm;
        var waistToShoulderRatio = waistWidthCm / shoulderWidthCm;
        
        if (waistToHipRatio < 0.85 && waistToShoulderRatio > 0.8) {
            return "Pear-shaped";
        } else if (waistToHipRatio >= 0.85 && waistToHipRatio <= 0.9) {
            return "Hourglass";
        } else if (waistToHipRatio > 0.9 && waistToHipRatio <= 1) {
            return "Apple-shaped";
        } else if (waistToShoulderRatio >= 1.1) {
            return "Inverted Triangle";
        } else if (waistToShoulderRatio < 0.8) {
            return "Rectangle";
        } else if (waistToHipRatio > 1 && waistToHipRatio <= 1.1 && waistToShoulderRatio <= 1.1) {
            return "Oval";
        } else {
            return "Undefined"; // If none of the conditions match
        }
    }

    navigator.mediaDevices.getUserMedia({ video: true })
        .then(stream => {
            video.srcObject = stream;
            video.onloadedmetadata = () => {
                setupBodyPix().then(() => {
                    $('#captureButton').click(async () => {
                        $('#countdownModal').css('display', 'block');

                    // Start the countdown
                    for (let i = 5; i > 0; i--) {
                        $('#countdownTimer').text(i);
                        await delay(1000);
                    }

                    // Hide the countdown modal
                    $('#countdownModal').css('display', 'none');

                        const heightInput = $('#heightInput').val();
                        const heightCm = parseFloat(heightInput);
                        const segmentation = await net.segmentPerson(video);

                        const measurements = await calculateMeasurements(segmentation, heightCm);
                        if (measurements) {
                            const bodyShape = classifyBodyShape(measurements.shoulderWidthCm, measurements.waistWidthCm, measurements.hipWidthCm);
                            console.log("Shoulder Width (cm):", measurements.shoulderWidthCm);
                            console.log("Waist Width (cm):", measurements.waistWidthCm);
                            console.log("Hip Width (cm):", measurements.hipWidthCm);
                            console.log("Body Shape:", bodyShape);

                            $.ajax({
                                url: '/get_recommended_outfits/',
                                type: 'GET',
                                dataType: 'json',
                                data: { 'body_shape': bodyShape }, // Pass the body shape as a parameter
                                success: function(response) {
                                    // Handle the successful response
                                    var recommendedOutfits = response.recommended_outfits;
                                    $('.plan_outfit_container2').find('tr').empty();
                                    // Iterate over the recommended outfits and construct HTML for each outfit
                                    $.each(recommendedOutfits, function(index, outfit) {
                                        // Create HTML for the outfit
                                        var outfitHtml = '<td>';
                                        outfitHtml += '<a href="/item/'+outfit.id+'" target="_blank"><div class="n_reco_outfit_container"><img class="img_reco_item" src="' + outfit.image_url + '" alt="' + outfit.name + '">';
                                        outfitHtml += '<h3>' + outfit.name + '</h3>';
                                        outfitHtml += '<p>Category: ' + outfit.category + '</p>';
                                        outfitHtml += '</div></a></td>';
                        
                                        // Append the outfit HTML to the table row
                                        $('.plan_outfit_container2 tr').append(outfitHtml);
                                        $("#reco_outfit_modal").css({"display":"flex"});
                                        $("#detected_bodyshape").text(bodyShape);
                                    });
                                },
                                error: function(xhr, status, error) {
                                    // Handle any errors
                                    console.error('Error fetching recommended outfits:', error);
                                }
                            });
                        }
                    });
                });
            };
        })
        .catch(err => console.error('getUserMedia() failed: ', err));

    function drawIndicator(ctx, x, y, label) {
        ctx.beginPath();
        ctx.arc(x, y, 5, 0, 2 * Math.PI);
        ctx.fillStyle = 'blue';
        ctx.fill();
        ctx.font = "12px Arial";
        ctx.fillStyle = "white";
        ctx.fillText(label, x - 20, y - 10);
    }

    async function delay(ms) {
        for (let i = ms / 1000; i > 0; i--) {
            console.log("Delay:", i);
            await new Promise(resolve => setTimeout(resolve, 1000));
        }
    }
    
    $('#btn_doneheight').click(function(){
        $('#enterheight_modal').css({"display":"none"});
    });

    $("#reco_outfit_modal").click(function (event) {
        if (event.target == $("#reco_outfit_modal")[0]) {
            $("#reco_outfit_modal").css("display", "none");
        }
    });
});
