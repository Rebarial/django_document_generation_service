function BankhandleModalEvent(modalSelector, orgIdInputSelector, prefix) {
    $(modalSelector).on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget),
            modalType = button.data('modal-type'),
            selectedOrgID = $(orgIdInputSelector).val(),
            form = $(this).find('form');

        if (!selectedOrgID){
            form.find(prefix + '-id').val('');
            form.find(prefix + '-name').val('');
            form.find(prefix + '-bic').val('');
            form.find(prefix + '-address').val('');
            form.find(prefix + '-correspondent_account').val('');
            form.find(prefix + '-current_account').val('');

            document.getElementById('modal_type').value = modalType;
            return
        }
        // Выполнение AJAX-запроса для получения данных
        $.ajax({
            url: '/fetch_organization_bank_data',
            type: 'GET',
            data: {'bank_id': selectedOrgID},
            success: function(response) {
                // Заполняем поля формы значениями из API
                form.find(prefix + '-id').val(response.id);
                form.find(prefix + '-name').val(response.name);
                form.find(prefix + '-bic').val(response.bic);
                form.find(prefix + '-address').val(response.address);
                form.find(prefix + '-correspondent_account').val(response.correspondent_account);
                form.find(prefix + '-current_account').val(response.current_account);

            },
            error: function() {
                form.find(prefix + '-id').val('');
                form.find(prefix + '-name').val('');
                form.find(prefix + '-bic').val('');
                form.find(prefix + '-address').val('');
                form.find(prefix + '-correspondent_account').val('');
                form.find(prefix + '-current_account').val('');
                let statusesCheckboxes = $('input[name="' + prefix + '_statuses[]"]');

                statusesCheckboxes.prop('checked', false)
            }
        });
    document.getElementById('modal_type').value = modalType;
    }
    );

};

$(document).ready(function () {
    BankhandleModalEvent('#addBankModal', '#id_organization_bank', '#id_organization_bank');
});

$(document).ready(function () {
    BankhandleModalEvent('#addBankCounModal', '#id_buyer_bank', '#id_buyer_bank');
});