/* Function to get the value of a URL parameter from the window,
   needed here to pass the search parameter to the API URL
 */

function GetURLParameter(sParam) {
    var sPageURL = window.location.search.substring(1);
    var sURLVariables = sPageURL.split('&');
    for (var i = 0; i < sURLVariables.length; i++) {
        var sParameterName = sURLVariables[i].split('=');
        if (sParameterName[0] == sParam) {
            return sParameterName[1];
        }
    }
}


var url = "/api/results/" + GetURLParameter("s").replace("+", "_");