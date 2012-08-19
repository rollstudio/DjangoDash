/*
CSS:
.custom-select {
    position: relative;
}
.custom-select select {
    position: absolute;
    top: 0;
    left: 0;
    z-index: 10;
    opacity: 0;
    width: 100%;
    height: 100%;
    -webkit-appearance: listbox;
}
 */
(function($){
    $.fn.extend({
        customSelect: function(options) {
            return this.each(function() {
                var $$ = $(this);
                var currentSelected = $$.find(':selected');

                var $container = $('<div />', {
                    'class': 'custom-select'
                });

                var $text = $('<span />', {
                    'text': currentSelected.text()
                });

                $$.wrap($container);
                $$.after($text);

                $$.change(function(){
                    $text.text($$.find(':selected').text());
                    $container.addClass('changed');
                });
            });
        }
    });
})(jQuery);
