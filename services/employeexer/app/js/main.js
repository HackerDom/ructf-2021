let messages = require('./request_pb');
const $ = require('jquery');


const xhrOverride = new XMLHttpRequest();
xhrOverride.responseType = 'arraybuffer';


function capitalize(string) {
    return string.charAt(0).toUpperCase() + string.slice(1);
}

function createObj(name, params) {
    let obj = new messages[name]();

    for (const [key, value] of Object.entries(params)) {
        obj['set' + capitalize(key)](value);
    }
    return obj;
}


function removeAllCookies() {
    const cookies = document.cookie.split(";");

    for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i];
        const eqPos = cookie.indexOf("=");
        const name = eqPos > -1 ? cookie.substr(0, eqPos) : cookie;
        document.cookie = name + "=;expires=Thu, 01 Jan 1970 00:00:00 GMT";
    }
}


function logout() {
    removeAllCookies();
    location.href = "/login_page";
}


function createEmployee() {
    let firstName = $("#first-name-f").val();
    let secondName = $("#second-name-f").val();
    let middleName = $("#middle-name-f").val();
    let number = $("#number-f").val();
    let cardholder = $("#cardholder-f").val();
    let cvv = $("#cvv-f").val();
    let country = $("#country-f").val();
    let city = $("#city-f").val();
    let description = $("#description-f").val();
    let tags = $("#tags-f").val();

    let newEmployee = createObj("NewEmployee", {
        "name": createObj("FullName", {
            "firstname": firstName,
            "secondname": secondName,
            "middlename": middleName,
        }),
        "card": createObj("BankCard", {
            "number": number,
            "cardholder": cardholder,
            "cvv": cvv,
        }),
        "location": createObj("Location", {
            "country": country,
            "city": city,
        }),
        "description": description,
        "tagsList": tags.split(', '),
    });

    makePostRequest("/add_employee", newEmployee.serializeBinary(), function (e) {
       console.log(e);
    });
}


function makePostRequest(url, data, callback) {
    $.ajax({
        url: url,
        method: 'POST',
        data: data,
        contentType: "application/protobuf",
        processData: false,
    }).then(callback);
}


function register(data) {
    $.ajax({
        url: "/register",
        method: 'POST',
        data: data,
        contentType: "application/protobuf",
        processData: false,
    }).then(function (responseData) {
        console.log(responseData);
        location.href = "/"
    });
}


function login(data) {
    $.ajax({
        url: "/login",
        method: 'POST',
        data: data,
        contentType: "application/protobuf",
        processData: false,
    }).then(function (responseData) {
        console.log(responseData);
        location.href = "/"
    });
}


function setHandlers() {
    $("#reg-btn").on('click', function (e) {
        let username = $("#login").val()
        let password = $("#password").val()
        let userPair = createObj("UserPair", {"username": username, "password": password});
        register(userPair.serializeBinary());
    });

    $("#log-btn").on('click', function (e) {
        let username = $("#login").val()
        let password = $("#password").val()
        let userPair = createObj("UserPair", {"username": username, "password": password});
        login(userPair.serializeBinary());
    });

    $("#logout-btn").on('click', function (e) {
        logout();
    });

    $("#ane-btn").on('click', function (e) {
        createEmployee();
    });
}


function main() {
    setHandlers();
}

$(document).ready(function() {
    main();
});
