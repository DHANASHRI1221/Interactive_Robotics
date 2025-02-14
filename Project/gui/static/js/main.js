// Updates joint slider value display smoothly
function updateJointValue(value) {
    document.getElementById("joint1Value").innerText = value + "°";
}

// Sends AJAX request to Flask API with animation effect
function sendCommand(action, data) {
    $("#status").html("<b>Processing...</b>").fadeIn(300);

    $.ajax({
        url: "http://127.0.0.1:5001/send-command",
        type: "POST",
        contentType: "application/json",
        data: JSON.stringify({ action: action, data: data }),
        success: function(response) {
            $("#status").html("<b>Success</b>").fadeOut(100).fadeIn(500); // Just "Success"
        },
        error: function(xhr) {
            let errorMessage = xhr.responseJSON ? xhr.responseJSON.message : "An error occurred";
            $("#status").html("<b>Error:</b> " + errorMessage).css("color", "red");
        }
    });
}
