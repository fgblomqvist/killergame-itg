var timelimit = 10;

window.onload = function() {

    var noCounter = ['/',
                     '/players',
                     '/gameover',
                     '/manage'];

    if (noCounter.indexOf(window.location.pathname) == -1) {
        var counter = document.createElement('p');
        counter.className = 'counter'
        counter.innerHTML = timelimit.toString();
        document.body.getElementsByClassName('wrapper')[0].appendChild(counter);

        var i = timelimit;

        setInterval(function() {
            i -= 1;
            var counter = document.getElementsByClassName('counter')[0];
            counter.innerHTML = i;
            if (i == 0) {
                window.location.pathname = '/';
            }

        }, 1000);
    }
};