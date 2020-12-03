function carouselNormalization() {
    var items = $("#review-carousel .carousel-item"), //grab all slides
        heights = [], //create empty array to store height values
        tallest; //create variable to make note of the tallest slide
    var normalizeHeights = function () {

        items.each(function () { //add heights to array
            heights.push($(this).height());
        });
        tallest = Math.max.apply(null, heights); //cache largest value
        items.each(function () {
            $(this).css('min-height', tallest + 'px');
            $(".carousel-row").css('min-height', tallest + 'px');
        });
    };

    normalizeHeights();

    $(window).on('resize orientationchange', function () {
        //reset vars
        tallest = 0;
        heights.length = 0;

        items.each(function () {
            $(this).css('min-height', '0'); //reset min-height
            $(".carousel-row").css('min-height', tallest + 'px');
        });
        normalizeHeights(); //run it again 
    });

};
