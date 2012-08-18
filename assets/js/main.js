(function($, window, document) {
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

    $(function() {
        setLogin();
    });
})(jQuery, window, document);
