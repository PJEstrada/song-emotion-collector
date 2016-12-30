
$(document).ready(function() {

    var background = $('#main-background');

    // Initial BG adjustment
    bgResize(background);

    // Watch on window resize
    window.onresize = function() {
        bgResize(background);
    }
});

function bgResize(backgroundImg) {

    bgH = backgroundImg.height();

    if($(window).height() >= bgH) {
        backgroundImg.css({
            width: 'auto',
            height: '100%'
        });
    } else {
        backgroundImg.css({
            width: '100%',
            height: 'auto'
        });
    }
}