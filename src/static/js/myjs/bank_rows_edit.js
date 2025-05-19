function bank_rows_by_organization(organization_row, bank_row){
    $(document).ready(function() {
        $(organization_row).on('change', function() {
            var orgId = $(this).val();
            var bankSelect = $(bank_row);
            bankSelect.empty();
            bankSelect.empty().append(
                $('<option>', {
                    value: '',
                    text: 'Новый банк'
                })
            );

            if (orgId === '') {
                return;
            }
                $.ajax({
                    url: '/fetch_bank_from_organization',
                    method: 'GET',
                    dataType: 'json',
                    data: {
                        'org_id': orgId
                    },
                    success: function(data) {
                        let firstBankSelected = false;
                        data.banks.forEach(function(bank) {
                            const option = $('<option>', {
                                value: bank.id,
                                text: bank.name
                            });

                            if (!firstBankSelected && bank.id != "") {
                                option.attr('selected', true);
                                firstBankSelected = true;
                            }
                            bankSelect.append(option);
                        });
                    },
                    error: function(xhr, status, error) {
                        console.error("Ошибка загрузки банков:", xhr.responseText);
                    }
                });
        });
    });
}

bank_rows_by_organization('#id_organization','#id_organization_bank')

bank_rows_by_organization('#id_buyer','#id_buyer_bank')