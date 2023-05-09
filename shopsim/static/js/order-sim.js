var simItems = $('.char_col');
var sortButtons = $('.shop_sorting_button');

// Add event listeners to the sorting buttons
sortButtons.on('click', function () {
    // Get the sort option from the data attribute of the button
    var sortOption = JSON.parse($(this).attr('data-isotope-option'));
    // sortChose = sortOption.sortBy;
    if (sortOption.sortBy != $('#order').val()) {
        $('#order').val(sortOption.sortBy);
        if (sortOption.sortBy == 'price_increasing') {
            $('#orderDisplay').html("Giá tăng dần");
        } else if (sortOption.sortBy == 'price_decreasing') {
            $('#orderDisplay').html("Giá giảm dần");
        }
        handleGetData(true);
    }

    // simItems.each(function () {
    //     var itemPrice = parseFloat($(this).attr('data-price'));
    //     if (sortOption.sortBy === 'price_increasing') {
    //         $(this).css('order', itemPrice);
    //     } else if (sortOption.sortBy === 'price_decreasing') {
    //         $(this).css('order', -itemPrice);
    //     }
    // });
});