function setCookie(name, value) {
    if (name != '')
        today = new Date();
    expires = new Date(today.getTime() + (8 * 7 * 86400000));
    document.cookie = name + '=' + value + '; expires=' + expires;
}

function getCookie(name) {
    if (name == '')
        return ('');

    name_index = document.cookie.indexOf(name + '=');

    if (name_index == -1)
        return ('');

    cookie_value = document.cookie.substr(name_index + name.length + 1, document.cookie.length);

    end_of_cookie = cookie_value.indexOf(';');
    if (end_of_cookie != -1)
        cookie_value = cookie_value.substr(0, end_of_cookie);

    space = cookie_value.indexOf('+');
    while (space != -1) {
        cookie_value = cookie_value.substr(0, space) + ' ' +
            cookie_value.substr(space + 1, cookie_value.length);
        space = cookie_value.indexOf('+');
    }

    return (cookie_value);
}
var userAgent = navigator.userAgent.toLowerCase();
var browserId = userAgent.match(/(firefox|chrome|safari|opera|msie)/)[1];
var browserVersion = (userAgent.match(new RegExp('.+(?:version)[\/: ]([\\d.]+)')) || userAgent.match(new RegExp('(?:' + browserId + ')[\/: ]([\\d.]+)')) || [0, '0'])[1];
var isIe6 = (browserId + browserVersion == "msie6.0");

var isIE = !!window.ActiveXObject;
if (isIE) {
    //var warning_url = '/warring.html';
    //location.href = warning_url + '?return=' + location.href;

    if (getCookie('warning_has_shown') != 'yes') {
        // your warning html url

        var warning_url = '/warring.html';
        location.href = warning_url + '?return=' + location.href;

    }
}
