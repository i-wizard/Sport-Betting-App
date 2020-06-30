window._ = require('lodash');

/**
 * We'll load jQuery and the Bootstrap jQuery plugin which provides support
 * for JavaScript based Bootstrap features such as modals and tabs. This
 * code may be modified to fit the specific needs of your application.
 */

try {
    window.Popper = require('popper.js').default;
    window.$ = window.jQuery = require('jquery');

    require('bootstrap');
} catch (e) {
}

window.axios = require('axios');

window.axios.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';

window.axios.defaults.xsrfCookieName = 'csrftoken'
window.axios.defaults.xsrfHeaderName = "X-CSRFTOKEN"

function formatDate(date) {
    let dd = date.getDate();
    let mm = date.getMonth() + 1;
    let yyyy = date.getFullYear();

    if (dd < 10) {
        dd = '0' + dd
    }
    if (mm < 10) {
        mm = '0' + mm
    }
    date = yyyy + '-' + mm + '-' + dd;
    return date
}

function showPasswordFunc(inputId) {
  var x = document.getElementById(inputId);
  if (x.type === "password") {
    x.type = "text";
  } else {
    x.type = "password";
  }
}

function getDayOfWeek(date) {
    let dayOfWeek = new Date(date).getDay();
    return isNaN(dayOfWeek) ? null : ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday'][dayOfWeek];
}

function Last7Days() {
    let result = [];
    for (let i = 0; i < 7; i++) {
        let d = new Date();
        d.setDate(d.getDate() - 1);
        d.setDate(d.getDate() - i);

        let data = {
            "day": getDayOfWeek(formatDate(d)),
            "date": formatDate(d)
        };
        result.push(data)
    }

    return (result);
}

function extractHostname(url) {
    var hostname;
    var protocol = 'http://';
    //find & remove protocol (http, ftp, etc.) and get hostname

    if (url.indexOf("//") > -1) {
        hostname = url.split('/')[2];
        protocol = url.split('/')[0]+'//'
    }
    else {
        hostname = url.split('/')[0];//
    }

    //find & remove "?"
    hostname = hostname.split('?')[0];

    return `${protocol}${hostname}`;
}

window.past7Days = Last7Days
window.hostName = extractHostname
window.showPassword = showPasswordFunc
