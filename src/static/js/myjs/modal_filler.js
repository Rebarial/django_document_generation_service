function handleModalEvent(modalSelector, orgIdInputSelector, prefix, default_id) {
    $(modalSelector).on('show.bs.modal', function (event) {
        var button = $(event.relatedTarget),
            modalType = button.data('modal-type'),
            selectedOrgID = $(orgIdInputSelector).val(),
            form = $(this).find('form');
        if (!selectedOrgID){
            form.find(prefix + '-id').val('');
            form.find(prefix + '-name').val('');
            form.find(prefix + '-inn').val('');
            form.find(prefix + '-kpp').val('');
            let isIPValue = 'False';
            form.find(prefix + '-is_ip').val(isIPValue); 
            form.find(prefix + '-ogrn').val('');
            form.find(prefix + '-address').val('');
            form.find(prefix + '-telephone').val('');
            form.find(prefix + '-fax').val('');
            form.find(prefix + '-director_name').val('');
            form.find(prefix + '-director_position').val('');
            form.find(prefix + '-accountant_name').val('');
            form.find(prefix + '-conventional_name').val('');
            form.find(prefix + '-stamp').val('');
            form.find(prefix + '-signature').val('');
            document.getElementById(prefix + '-stamp_url').src = '';
            document.getElementById(prefix + '-signature_url').src = '';

            document.getElementById(prefix + '-signature-preview').innerHTML = '<small>Новое изображение:</small>';
            document.getElementById(prefix + '-stamp-preview').innerHTML = '<small>Новое изображение:</small>';

            form.find(`${prefix}-statuses input[type="checkbox"]`).each(function() {
                const value = Number($(this).val()); 

                if (default_id == value) {
                    this.checked = true;
                } else {
                    this.checked = false;
                }
            });
            document.getElementById('modal_type').value = modalType;
            return
        }
        // Выполнение AJAX-запроса для получения данных
        $.ajax({
            url: '/fetch_organization_data',
            type: 'GET',
            data: {'org_id': selectedOrgID},
            success: function(response) {
                // Заполняем поля формы значениями из API
                form.find(prefix + '-id').val(response.id);
                form.find(prefix + '-name').val(response.name);
                form.find(prefix + '-inn').val(response.inn);
                form.find(prefix + '-kpp').val(response.kpp);
                let isIPValue = response.is_ip ? 'True' : 'False';
                form.find(prefix + '-is_ip').val(isIPValue); 
                form.find(prefix + '-ogrn').val(response.ogrn);
                form.find(prefix + '-address').val(response.address);
                form.find(prefix + '-telephone').val(response.telephone);
                form.find(prefix + '-fax').val(response.fax);
                form.find(prefix + '-director_name').val(response.director_name);
                form.find(prefix + '-director_position').val(response.director_position);
                form.find(prefix + '-accountant_name').val(response.accountant_name);
                form.find(prefix + '-conventional_name').val(response.conventional_name);
                form.find(prefix + '-stamp').val('');
                form.find(prefix + '-signature').val('');

                document.getElementById(prefix + '-stamp_url').src = response.stamp_url;
                document.getElementById(prefix + '-signature_url').src = response.signature_url;
                
                document.getElementById(prefix + '-signature-preview').innerHTML = '<small>Новое изображение:</small>';
                document.getElementById(prefix + '-stamp-preview').innerHTML = '<small>Новое изображение:</small>';
            

                const selectedStatuses = response.statuses || [];
                form.find(`${prefix}-statuses input[type="checkbox"]`).each(function() {
                    const value = Number($(this).val());
                    // Проверка значения статуса
                    if (selectedStatuses.includes(value)) {
                        this.checked = true;
                    } else {
                        this.checked = false;
                    }
                });

            },
            error: function(jqXHR, textStatus, errorThrown) {
                alert(errorThrown)
                form.find(prefix + '-id').val('');
                form.find(prefix + '-name').val('');
                form.find(prefix + '-inn').val('');
                form.find(prefix + '-kpp').val('');
                let isIPValue = 'False';
                form.find(prefix + '-is_ip').val(isIPValue); 
                form.find(prefix + '-ogrn').val('');
                form.find(prefix + '-address').val('');
                form.find(prefix + '-telephone').val('');
                form.find(prefix + '-fax').val('');
                form.find(prefix + '-director_name').val('');
                form.find(prefix + '-director_position').val('');
                form.find(prefix + '-accountant_name').val('');
                form.find(prefix + '-conventional_name').val('');
                form.find(prefix + '-stamp').val('');
                form.find(prefix + '-signature').val('');
                document.getElementById(prefix + '-stamp_url').src = '';
                document.getElementById(prefix + '-signature_url').src = '';
                
                document.getElementById(prefix + '-signature-preview').innerHTML = '<small>Новое изображение:</small>';
                document.getElementById(prefix + '-stamp-preview').innerHTML = '<small>Новое изображение:</small>';

                let statusesCheckboxes = $('input[name="' + prefix + '_statuses[]"]');

                form.find(`${prefix}-statuses input[type="checkbox"]`).each(function() {
                    const value = Number($(this).val()); 
    
                    if (default_id == value) {
                        this.checked = true;
                    } else {
                        this.checked = false;
                    }
                });
                statusesCheckboxes.prop('checked', false)
            }
        });
    document.getElementById('modal_type').value = modalType;
    }
    );

};

$(document).ready(function () {
    handleModalEvent('#addOrganizationModal', '#id_organization', '#id_seller', 1);
});

$(document).ready(function () {
    handleModalEvent('#addCounterpartyModal', '#id_buyer', '#id_buyer', 2);
});

$(document).ready(function () {
    handleModalEvent('#addConsigneeModal', '#id_consignee', '#id_consignee', 4);
});
