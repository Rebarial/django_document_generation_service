//Вставка строки
function addRowDropLine(formId, modalId, prefix) {
    document.getElementById(formId).addEventListener('submit', function(e) {
        e.preventDefault();
        selectId = 'id_' + prefix;
        const formData = new FormData(this);
        formData.append('org_id', document.getElementById(selectId).value);
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
            } else 
            {
                document.querySelector(modalId + ' .btn-close').click();

                
                //data.statuses
                for (let i = 1; i <= 4; i++) {
                    let select = null
                    if (i == 1){
                        select = document.getElementById('id_organization');
                    }
                    else if (i == 2)
                    {
                        select = document.getElementById('id_buyer');
                    }
                    else if(i == 4)
                    {
                        select = document.getElementById('id_consignee');
                    }
                    else {
                        continue;
                    }

                    optionNotFound = true
                    for (let j = 0; j < select.options.length; j++) {
                        if (select.options[j].value == data.id) {
                            optionNotFound = false;
                            let selectedOption = select.options[j];
                            if (data.statuses.includes(i)){
                                let result_str = ""
                                if (data.name)
                                    result_str += data.name + " "
                                if (data.inn) 
                                    result_str += data.inn

                                selectedOption.textContent = result_str;
                            }
                            else {
                                select.remove(j);
                            }
                            break;
                        }
                    }
                    if (optionNotFound && data.statuses.includes(i)) 
                    {
                        let result_str = ""
                        if (data.name)
                            result_str += data.name + " "
                        if (data.inn) 
                            result_str += data.inn

                        let option = new Option(result_str, data.id, true, true);
                        select.add(option);
                    }
                    
                }

            }
        })
    });
}

addRowDropLine('organizationForm', '#addOrganizationModal', 'organization')
addRowDropLine('counterpartyForm', '#addCounterpartyModal', 'buyer')
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