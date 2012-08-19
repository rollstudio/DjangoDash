(function($, window, document) {
    var $body;

    function setLogin() {
        var $form_signin = $('#form_signin');
        var $form_register = $('#form_register');

        $('.signup_list').on('click', 'a', function(e) {
            e.preventDefault();
            var $$ = $(this);

            if ($$.attr('class') === 'login') {
                $form_register.fadeOut('fast', function() {
                    $form_signin.fadeIn('fast');
                });
            } else {
                $form_signin.fadeOut('fast', function() {
                    $form_register.fadeIn('fast');
                });
            }
        });
    }

    function setNextPrev() {
        if ($body.attr('id') !== 'home') {
            return;
        }

        var $column = $('#right_column');
        var $prev = $column.find('.prev');
        var $next = $column.find('.next');

        var current = 0;
        var lastId = window.lastQuoteId;
        var url = window.nextQuoteUrl;

        if ($column.find('.wrapper li').length === 0) {
            $column.find('.prev_next a').addClass('disabled');
            return;
        }

        $column.on('click', '.prev_next a:not(.disabled)', function(e) {
            e.preventDefault();

            var $$ = $(this);

            var ajaxPromise;

            if ($$.attr('class') === 'next') {
                current += 1;

                ajaxPromise = $.ajax({
                    url: url,
                    type: 'get',
                    data: {
                        id: lastId,
                        limit: 1
                    }
                }).success(function(data) {
                    if (data.length > 0) {
                        lastId = data[0].pk;
                    } else {
                        $next.addClass('disabled');
                    }
                });
            } else {
                current -= 1;
            }

            $.when(ajaxPromise, $column.animate({
                scrollTop: $column.height() * current
            }, 500)).done(function() {
                if (current === 0) {
                    $prev.addClass('disabled');
                } else {
                    $prev.removeClass('disabled');
                }
            });
        });
    }

    function setMiddleColumn() {
        var $column = $('#middle_column');
        var $prev = $column.find('.prev');
        var $next = $column.find('.next');

        $('#write-your-dixit').on('click', function(e) {
            e.preventDefault();
            $next.trigger('click');
        });

        $next.on('click', function(e) {
            e.preventDefault();
            $column.animate({
                scrollLeft: $column.width()
            }, 500, function() {
                $next.addClass('disabled');
                $prev.removeClass('disabled');
            });
        });

        $prev.on('click', function(e) {
            e.preventDefault();
            $column.animate({
                scrollLeft: 0
            }, 500, function() {
                $prev.addClass('disabled');
                $next.removeClass('disabled');
            });
        });
    }

    $(function() {
        $body = $('body');
        setLogin();
        setMiddleColumn();
        setNextPrev();
    });
})(jQuery, window, document);
