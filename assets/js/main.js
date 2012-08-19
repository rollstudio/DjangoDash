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

    function share(type, url, title, description) {
        if ($.trim(title) === '') {
            title = 'Check this quote!';
        }

        var data = {
            url: url,
            text: title
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

        var left = (screen.width/2)- 300;
        var top = (screen.height/2)-300;

        window.open(url, '', 'menubar=no,toolbar=no,resizable=yes,scrollbars=yes,height=600,width=600, top='+top+', left='+left);
    }


    function setSharing() {
        $('.share').each(function() {
            var $$ = $(this);
            var url = $$.data('url');
            var title = $$.data('title');
            var description = $$.data('description');

            $$.on('click', '.share_buttons a', function(e) {
                e.preventDefault();
                share($(this).attr('class'), url, title, description);
            });
        });

        var vote = $('.vote').each(function() {
            var $vote = $(this);

            var id = $vote.data('id');
            var token = $vote.find('[name=csrfmiddlewaretoken]').val();

            var addLikeUrl = $vote.data('add');
            var deleteLikeUrl = $vote.data('delete');

            $vote.on('click', 'a:not(.disabled)', function(e) {
                var $$ = $(this);
                e.preventDefault();

                var url = addLikeUrl;
                if ($vote.hasClass('liked')) {
                    url = deleteLikeUrl;
                }

                $$.text('Updating...');

                $.ajax({
                    type: 'post',
                    data: {
                        id: id,
                        csrfmiddlewaretoken: token
                    },
                    url: url
                }).success(function(data) {
                    var vote = 1;

                    if ($vote.hasClass('liked')) {
                        $vote.removeClass('liked');
                        $$.text('vote');
                        vote = -1;
                    } else {
                        $vote.addClass('liked');
                        $$.text('voted');
                    }

                    var $votes = $('.quote[data-id='+ id +'] .votes').each(function() {
                        var $$ = $(this);
                        $$.text(parseInt($$.text(), 10) + vote);
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
                var $c = $('#right_column').addClass('mini');

                window.setTimeout(function() {
                    $c.on('mouseout mouseover', function() {
                        $(this).off().removeClass('mini');
                    });
                }, 200);
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

        var prevNext = $column.find('.prev_next');

        $(window).resize(function() {
            $column.scrollTop($column.height() * current);
        });

        $column.on('click', '.prev_next:not(.loading) a:not(.disabled)', function(e) {
            e.preventDefault();

            var $$ = $(this);

            prevNext.fadeOut('fast', function() {
                var ajaxPromise;

                if ($$.attr('class') === 'next') {
                    current += 1;
                    $column.find('.prev_next').addClass('loading');
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

                        $wrapper.append($li);
                        setScroller();
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
                }, 500)).always(function() {
                    if (current === 0) {
                        $prev.addClass('disabled');
                    } else {
                        $prev.removeClass('disabled');
                    }

                    prevNext.fadeIn('fast').removeClass('loading');
                });
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

        var left = 0;

        var $writeLink = $('.write-your-dixit').on('click', function(e) {
            e.preventDefault();
            $next.trigger('click');
        });

        var $aboutLink = $('.about-the-project').on('click', function(e) {
            e.preventDefault();
            $prev.trigger('click');
        });


        $(window).resize(function() {
            var l = (left === 0) ? 0 : $column.width();
            $column.scrollLeft(l);
        });


        $next.on('click', function(e) {
            left = 1;
            e.preventDefault();
            $column.animate({
                scrollLeft: $column.width()
            }, 500, function() {
                $next.addClass('disabled');
                $prev.removeClass('disabled');
            });

            $writeLink.addClass('active');
            $aboutLink.removeClass('active');
        });

        $prev.on('click', function(e) {
            left = 0;
            e.preventDefault();
            $column.animate({
                scrollLeft: 0
            }, 500, function() {
                $prev.addClass('disabled');
                $next.removeClass('disabled');
            });

            $aboutLink.addClass('active');
            $writeLink.removeClass('active');
        });
    }

    function setKeyboardNavigation() {
        if ($body.attr('id') !== 'home') {
            return;
        }

        var $left = $('#middle_column .prev');
        var $right = $('#middle_column .next');
        var $up = $('#right_column .prev');
        var $down = $('#right_column .next');

        $(document).on('keyup', function(e) {
            switch (e.keyCode) {
                case 37:
                    $left.trigger('click');
                break;
                case 38:
                    $up.trigger('click');
                break;
                case 39:
                    $right.trigger('click');
                break;
                case 40:
                    $down.trigger('click');
                break;
                default:
                return;
            }

            e.preventDefault();
        });
    }

    function animateLogo(from, to) {
        from = from || '#000';
        to = to || '#fe57a1';

        var logo = $('header h1 a').animate({
            color: to
        }, 4000, function() {
            animateLogo(to, from);
        });
    }

    function setScroller() {
        var $panels = $("#right_column .dixit_text").nanoScroller();

        $panels.each(function() {
            var $$ = $(this);
            var $p = $$.find('.content > p');

            var h = $$.height();
            var ph = $p.outerHeight(true);

            if (h > ph) {
                $$.height(ph);
            }
        });
    }

    $(function() {
        $body = $('body');
        setLogin();
        setMiddleColumn();
        setNextPrev();
        setSharing();
        setKeyboardNavigation();

        $('select').customSelect();

        setScroller();
        animateLogo();

        $(window).resize(function() {
            setScroller();
        });
    });
})(jQuery, window, document);
