let messages = require('./request_pb');
const $ = require('jquery');


const xhrOverride = new XMLHttpRequest();
xhrOverride.responseType = 'arraybuffer';


function createSketch(data) {
    $.ajax({
        url: "/createSketch",
        method: 'POST',
        // xhr: function () {
        //     return xhrOverride;
        // },
        data: data,
        contentType: "application/protobuf",
        processData: false,
    }).then(function (responseData) {
        location.href = `/sketch_page?id=${responseData}`
    });
}

function getAndDrawSketch(id, drawFunc) {
    $.get({
        url: `/sketch?id=${id}`,
        success: function (e) {
            drawFunc(messages.Sketch.deserializeBinary(e).toObject());
        },
        xhr: function () {
            return xhrOverride;
        },
    });
}


function drawText(ctx, text) {
    ctx.font = text.font;
    ctx.fillText(text.value, text.coords.left, text.coords.top);
}


function setStyles(ctx, options) {
    if (options) {
        const color = '#' + options.color.toString('16').padStart(6, 0);
        ctx.fillStyle = color;
        ctx.strokeStyle = color;
        ctx.lineWidth = options.linewidth;
    } else {
        ctx.fillStyle = '#000000';
        ctx.strokeStyle = '#000000';
    }
}


function drawCircle(ctx, circle, options) {
    setStyles(ctx, options);
    ctx.beginPath();
    ctx.arc(circle.center.left, circle.center.top, circle.radius, 0, Math.PI * 2, true);
    if (options.filled) {
        ctx.fill()
    } else {
        ctx.stroke();
    }
}


let left = 0;
let top = 0;


function drawLine(ctx, line, options) {
    setStyles(ctx, options);
    ctx.beginPath();
    ctx.moveTo(line.start.left, line.start.top);
    // ctx.lineTo(line.end.left, line.end.top);
    ctx.lineTo(left, top);
    ctx.stroke();
}

function drawRect(ctx, rect, options) {
    setStyles(ctx, options);
    let drawKey = options.filled ? "fillRect" : "strokeRect";
    ctx[drawKey](rect.lefttop.left, rect.lefttop.top, rect.rightbottom.left - rect.lefttop.left, rect.rightbottom.top - rect.lefttop.top);
}


const DRAW_LIST = [
    ['circle', drawCircle],
    ['line', drawLine],
    ['rect', drawRect],
];


function drawFigure(ctx, figure) {
    DRAW_LIST.forEach(function (drawPair) {
        let [name, drawer] = drawPair;
        if (figure[name]) {
            drawer(ctx, figure[name], figure['options']);
        }
    });
}


function drawGrid(canvas, ctx) {
    ctx.fillStyle = "#fff";
    ctx.fillRect(0, 0, canvas.width, canvas.height);

    const step = 10;
    ctx.lineWidth = 0.5;
    ctx.strokeStyle = '#aaaaaa';
    for (let i = 0; i < canvas.height; i += step) {
        ctx.beginPath();       // Start a new path
        ctx.moveTo(0, i);    // Move the pen to (30, 50)
        ctx.lineTo(canvas.width, i);  // Draw a line to (150, 100)
        ctx.stroke();
    }
    for (let i = 0; i < canvas.width; i += step) {
        ctx.beginPath();       // Start a new path
        ctx.moveTo(i, 0);    // Move the pen to (30, 50)
        ctx.lineTo(i, canvas.height);  // Draw a line to (150, 100)
        ctx.stroke();
    }
}


function draw() {
    const canvas = document.getElementById('canvas');
    if (canvas.getContext) {
        const ctx = canvas.getContext('2d');
        drawGrid(canvas, ctx);

        getAndDrawSketch(sketchId, function (sketch) {
            sketch.textsList.forEach(function (text) {
                drawText(ctx, text);
            });
            sketch.figuresList.forEach(function (figure) {
                drawFigure(ctx, figure);
            });
        });
    }
}

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
    // resizeCanvas();
    // draw();
}

$(document).ready(function() {
    main();
});
