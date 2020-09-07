window.onload = function() {
    d = document.getElementsByClassName("sent")
    Array.from(d).forEach(function(element) {
        var cur = element.dataset['cur'];
        var prev = element.dataset['prev'];
        cur = parseFloat(cur);
        prev = parseFloat(prev);
        var diff = cur - prev;
        if (diff < 0)
            element.style.color = 'red'
        else
            element.style.color = 'green'
        element.innerHTML += cur.toFixed(5) + '(' + diff.toFixed(5) + ')';
    });

    d = document.getElementsByClassName("vol")
    Array.from(d).forEach(function(element) {
        var cur = element.dataset['cur'];
        var prev = element.dataset['prev'];
        cur = parseFloat(cur);
        prev = parseFloat(prev);
        var diff = cur - prev;
        if (diff < 0)
            element.style.color = 'red'
        else
            element.style.color = 'green'
        element.innerHTML += cur.toFixed(0) + '(' + diff.toFixed(0) + ')';
    });

}