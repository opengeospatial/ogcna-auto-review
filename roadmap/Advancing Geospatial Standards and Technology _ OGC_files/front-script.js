jQuery(document).ready(function () {

    document.addEventListener('wpcf7mailsent', function (event) {
        jQuery('form.wpcf7-form').find(".evcf7_email_sent, .evcf7_error_sending_mail").remove();
    }, false);

    document.addEventListener('wpcf7submit', function (event) {
        jQuery(this).parents('form.wpcf7-form').find(".evcf7_email_sent, .evcf7_error_sending_mail").remove();
    }, false);

    if (jQuery('form.wpcf7-form').find('input[name=verification]')) {

        if (typeof evcf7Obj.evcf7_options.verify_button_text !== 'undefined') {
            jQuery('form.wpcf7-form').each(function () {
                if (jQuery(this).find('input[name=verification]:first').parents('span.verification').length > 0) {
                    jQuery(this).find('input[name=verification]:first').parents('span.verification').after('<p class="evcf7-verify-btn"><input type="button" name="evcf7-verify-email" value="' + evcf7Obj.evcf7_options.verify_button_text + '"><span class="loader"></span></p>');
                } else {
                    jQuery(this).find('input[name=verification]:first').parents('span[data-name="verification"]').after('<p class="evcf7-verify-btn"><input type="button" name="evcf7-verify-email" value="' + evcf7Obj.evcf7_options.verify_button_text + '"><span class="loader"></span></p>');
                }
            });
        }

        jQuery('body').on('click', 'form.wpcf7-form input[name=evcf7-verify-email]', function () {
            var $this = jQuery(this);
            jQuery(this).parents('form.wpcf7-form').find(".evcf7_email_sent, .evcf7_error_sending_mail, .wpcf7-not-valid-tip").remove();
            var form_id = $this.parents('form.wpcf7-form').find('input[name=_wpcf7]').val();
            var data_email = $this.parents('form.wpcf7-form').find('input[name=verification]').val();

            var currentrequest = null;
            if (!Geekcodelab_isEmail(data_email)) {
                alert(evcf7Obj.evcf7_options.invalid_format_message);
                currentrequest = 1;
            } else {
                $this.prop('disabled', true);
                $this.next().css("visibility", "visible");
            }

            if (form_id != undefined && data_email != undefined && data_email != '') {
                jQuery.ajax({
                    url: evcf7Obj.ajaxurl,
                    type: 'POST',
                    beforeSend: function (xhr) {
                        if (currentrequest == 1) {
                            xhr.abort();
                        }
                    },
                    data: {
                        'action': 'evcf7_verify_email',
                        'data_email': data_email,
                        'form_id': form_id
                    },
                    success: function (response) {
                        var form_parent = $this.parents('form.wpcf7-form');
                        response = response.trim();
                        form_parent.find('input[name=verification]:first').after(response.trim());

                        var len = form_parent.find('.evcf7_email_sent').length;
                        if (len > 0) form_parent.find('.evcf7-verify-btn').remove();

                        $this.next().css("visibility", "hidden");
                        $this.prop('disabled', false);

                    }
                });
            }
        });
    }
});

function Geekcodelab_isEmail(email) {
    var regex = /^([a-zA-Z0-9_.+-])+\@(([a-zA-Z0-9-])+\.)+([a-zA-Z0-9]{2,4})+$/;
    return regex.test(email);
}