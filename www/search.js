var form = document.getElementById("search-form");
form.addEventListener("submit", function(event) {
    event.preventDefault();
    var url = form.action;
    var data = new FormData(form);
    var query = new URLSearchParams(data).toString();
    url = url + "?" + query;
    var xhr = new XMLHttpRequest();
    xhr.open("GET", url);
    xhr.onload = function() {
        if (xhr.status == 200) {
            var text = xhr.responseText;
            var div = document.getElementById("output");
            div.innerHTML = "The address is: <b>" + text + "</b>";
        } else {
            alert("Error: " + xhr.statusText);
        }
    };
    xhr.send();
});