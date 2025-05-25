//Вставка строки
function addBankRowDropLine(formId, modalId, rows_id, OrganizationSelect) {
    document.getElementById(formId).addEventListener('submit', function(e) {
        e.preventDefault();
        
        const formData = new FormData(this);

        const organizationSelect = document.getElementById(OrganizationSelect);
        const selectedOrganization = organizationSelect.value;

        const bankSelect = document.getElementById(rows_id);
        const selectedBank = bankSelect.value;
        if (!selectedOrganization) {
            alert('Пожалуйста, выберите организацию из списка');
            return;
        }
    
        formData.append('org', selectedOrganization);
        formData.append('bank', selectedBank);

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


                const select = document.getElementById(rows_id);
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

            }
        }).catch(error => console.error('Ошибка:', error));
    });
}

addBankRowDropLine('bankCounForm', '#addBankCounModal', 'id_buyer_bank', 'id_buyer')
addBankRowDropLine('bankForm', '#addBankModal', 'id_organization_bank', 'id_seller')