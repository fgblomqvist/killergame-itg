var timelimit = 20;

window.onload = function() {
    if (window.location.pathname != '/' && window.location.pathname != '/players' && window.location.pathname != '/gameover') {
        var counter = document.createElement('p');
        counter.className = 'counter'
        counter.innerText = timelimit.toString();
        document.body.getElementsByClassName('wrapper')[0].appendChild(counter);

        var i = timelimit;

        setInterval(function() {
            i -= 1;
            var counter = document.getElementsByClassName('counter')[0];
            counter.innerText = i;
            if (i == 0) {
                window.location.pathname = '/';
            }

        }, 1000);
    }
};