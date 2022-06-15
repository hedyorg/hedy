(function() {
    $('.option-block').on("click", function () {
        // Remove active attribute and hide possible answer button
        $('.option-block').removeClass('border-double border-8 active');
        $('.submit-button').hide();

        // Add active attribute and show correct answer button
        $(this).addClass('border-double border-8 active');
        $(this).find(".submit-button").show();
    });
})();