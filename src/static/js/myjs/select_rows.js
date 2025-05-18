//Вставка строки
function addRowDropLine(formId, modalId, prefix) {
    document.getElementById(formId).addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);
        const modalType = document.getElementById('modal_type').value;
        
        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest'
            }
        }).then(response => response.json()).then(data => {
            if (data.errors) {
                alert('Ошибка: ' + JSON.stringify(data.errors));
            } else {
                document.querySelector(modalId + ' .btn-close').click();

                selectId = 'id_' + prefix;

                const select = document.getElementById(selectId);
                const selectedIndex = select.selectedIndex;
                
                if (selectedIndex != 0) {
                    
                    const selectedOption = select.options[selectedIndex];
                    selectedOption.textContent = data.name;
                }
                else
                {
                    const option = new Option(data.name, data.id, true, true);
                    select.add(option);
                }

                 //Добавить обход всех dropline
            }
        }).catch(error => console.error('Ошибка:', error));
    });
}

addRowDropLine('organizationForm', '#addOrganizationModal', 'organization')
addRowDropLine('counterpartyForm', '#addCounterpartyModal', 'counterparty')
addRowDropLine('consigneeForm', '#addConsigneeModal', 'consignee')

/*
document.getElementById('counterpartyForm').addEventListener('submit', function (e) {
    e.preventDefault();
    const formData = new FormData(this);
    const modalType = document.getElementById('modal_type_consignee').value;

    fetch(this.action, {
        method: 'POST',
        body: formData,
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        if (data.errors) {
            alert('Ошибка: ' + JSON.stringify(data.errors));
        } else {
            document.querySelector('#addCounterpartyModal .btn-close').click();

            if (modalType === 'counterparty') {
                const select = document.getElementById('id_counterparty');
                const option = new Option(data.name, data.id, true, true);
                select.add(option);

                const select_bank = document.getElementById('id_bank_counterparty');
                if (select_bank) {
                    const option_bank = new Option(data.bank_name, data.bank_id, true, true);
                    select_bank.add(option_bank);
                }

                const select_consignee = document.getElementById('id_consignee');
                if (select_consignee) {
                    const option_consignee = new Option(data.name, data.id, true, true);
                    select_consignee.add(option_consignee);
                };

                const select_investor = document.getElementById('id_investor');
                if (select_investor) {
                    const option_investor = new Option(data.name, data.id, true, true);
                    select_investor.add(option_investor);
                };
            }
            else {
                const select = document.getElementById('id_consignee');
                if (select) {
                    const option = new Option(data.name, data.id, true, true);
                    select.add(option);
                };

                const select_investor = document.getElementById('id_investor');
                if (select_investor) {
                    const option_investor = new Option(data.name, data.id, true, true);
                    select_investor.add(option_investor);
                };

            }

            this.reset();
        }
    })
    .catch(error => console.error('Ошибка:', error));
});
/*
//Вставка строки
function addRowDropLine(formId, modalId, prefix){
    document.getElementById(formId).addEventListener('submit', function (e) {
        e.preventDefault();
        const formData = new FormData(this);
        const modalType = document.getElementById('modal_type').value;

        fetch(this.action, {
            method: 'POST',
            body: formData,
            headers: {
                'X-Requested-With': 'XMLHttpRequest',
            },
        })
        .then(response => response.json())
        .then(data => {
            if (data.errors) {
                alert('Ошибка:' + JSON.stringify(data.errors));
            } else {
                document.querySelector(modalId + ' .btn-close').click();

                if (modalType === 'organization') {
                    if (document.getElementById("id_" + prefix +"-id").value == ""){
                        const select = document.getElementById('id_organization');
                        const option = new Option(data.name, data.id, true, true);
                        select.add(option);
                    }
                    else
                    {
                        const select = document.getElementById('id_organization');
        
                        const selectedIndex = select.selectedIndex;
                        const selectedOption = select.options[selectedIndex];
                    
                        if (selectedOption) {
                            selectedOption.textContent = data.name;
                        }
                    }
                }
                else {const select = document.getElementById('id_shipper');
                    const option = new Option(data.name, data.id, true, true);
                    select.add(option);
                    }

                this.reset();

            }
        })
        .catch(error => console.error('Ошибка:', error));
    })
};

addRowDropLine('organizationForm', 'addOrganizationModal', 'organization')
addRowDropLine('counterpartyForm', 'addCounterpartyModal', 'counterparty')
*/