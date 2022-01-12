//This Javascript is run on the main web page to get the names form the API.
var request = new XMLHttpRequest()

request.open('GET', 'https://misnomers.herokuapp.com/api', true)

//Used for local testing.
//request.open('GET', 'http://127.0.0.1:5000/api', true)

request.onload = function () {
    var data = JSON.parse(this.response)
    
    //Update the relavent HTML element with a name.
    var index = 0

    function fill(name) {
        document.getElementById("name" + index).innerText = name.name
        ++index
    }

    data.forEach(fill)
}

request.send()
