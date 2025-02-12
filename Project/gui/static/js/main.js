// Updates joint slider value display smoothly
function updateJointValue(value) {
    document.getElementById("joint1Value").innerText = value + "°";
}

// Sends AJAX request to Flask API with animation effect
function sendCommand(action, data) {
    $("#status").html("<b>Processing...</b>").fadeIn(300);

    $.ajax({
        url: "/voice-command",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ action: action, data: data }),
        success: function(response) {
            $("#status").html("<b>Success:</b> " + response.message).fadeOut(100).fadeIn(500);
        },
        error: function(xhr) {
            $("#status").html("<b>Error:</b> " + xhr.responseJSON.message).css("color", "red");
        }
    });
}

