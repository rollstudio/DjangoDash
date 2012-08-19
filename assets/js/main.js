(function($, window, document) {
    var $body;

    function shareOnFacebook(url, title, text) {
        var data = {
            app_id: window.appId,
            link: url,
            name: title,
            description: text,
            method: 'feed'
        };

        FB.ui(data);
    }

    function share(type, url, description) {
        var data = {
            url: url,
            text: 'Check this quote!'
        };

        switch (type) {
            case 'share_fb':
                shareOnFacebook(url, data.text, description);
                return;
            case 'share_tw':
                url = 'https://twitter.com/intent/tweet?' + $.param(data);
            break;
            case 'share_gp':
                url = 'https://plus.google.com/share?' + $.param(data);
            break;
        }

        window.open(url, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600');
    }


    function setSharing() {
        $('.share').each(function() {
            var $$ = $(this);
            var url = $$.data('url');
            var description = $$.data('description');

            $$.on('click', '.share_buttons a', function(e) {
                e.preventDefault();
                share($(this).attr('class'), url, description);
            });
        });

        var vote = $('.vote').each(function() {
            var $$ = $(this);

            var id = $$.data('id');
            var token = $$.find('[name=csrfmiddlewaretoken]').val();

            $$.on('click', 'a:not(.disabled)', function(e) {
                var $$ = $(this);
                e.preventDefault();

                $.ajax({
                    type: 'post',
                    data: {
                        id: id,
                        csrfmiddlewaretoken: token
                    },
                    url: $$.attr('href')
                }).success(function(data) {
                    if (data !== 1) {
                        //already voted
                        return;
                    }

                    var $votes = $('.quote[data-id='+ id +'] .votes').each(function() {
                        var $$ = $(this);
                        $$.text(parseInt($$.text(), 10) + 1);
                    });
                }).fail(function(data) {
                    $$.text('Error!!1').addClass('disabled');
                });
            });
        });

        if ($body.attr('id') === 'home') {
            vote.on('click', 'a.login.disabled', function(e) {
                e.preventDefault();
                $('.write-your-dixit').trigger('click');
                $('#right_column').addClass('mini').on('mouseout', function() {
                    $(this).removeClass('mini');
                });
            });
        }
    }

    function setLogin() {
        var $form_signin = $('#form_signin');
        var $form_register = $('#form_register');

        $('.signup_list').on('click', 'a.login, a.register', function(e) {
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
        var $wrapper = $column.find('.wrapper');
        var $prev = $column.find('.prev');
        var $next = $column.find('.next');

        var current = 0;
        var lastId = 0;
        var url = window.prevQuoteUrl;
        var quotes = $column.find('.wrapper .quote');

        if (quotes.length < 2) {
            $column.find('.prev_next a').addClass('disabled');
            return;
        } else {
            lastId = quotes.eq(quotes.length - 1).data('id');
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
                    var $li = $('<li />');
                    var $quote = $(data).appendTo($li);

                    lastId = $quote.data('id');
                    console.log(lastId);
                    $wrapper.append($li);
                }).fail(function() {
                    if (current >= $wrapper.find('li .quote').length - 1) {
                        $next.addClass('disabled');
                    }
                });

            } else {
                current -= 1;
                $next.removeClass('disabled');
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
        if ($body.attr('id') !== 'home') {
            return;
        }

        var $column = $('#middle_column');
        var $prev = $column.find('.prev');
        var $next = $column.find('.next');

        $('.write-your-dixit').on('click', function(e) {
            e.preventDefault();
            $next.trigger('click');
        });

        $('.about-the-project').on('click', function(e) {
            e.preventDefault();
            $prev.trigger('click');
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
        setSharing();

        $('select').customSelect();
    });
})(jQuery, window, document);
