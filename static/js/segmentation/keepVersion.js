const keepVersion = () => {
    let footer = document.getElementById('modal-footer-version')
    footer.innerHTML = `<div class="spinner-border text-warning" role="status">
                            <span class="sr-only">Loading...</span>
                        </div>`
    let btnVersion = document.getElementById('keepVersion')
    btnVersion.className += ' disabled'
    $.ajax({
            url: "keepVersion",
            type: "POST",
            dataType: "json",
            data: {
                'filename': getFileSelect(),
                'version': btnVersion.getAttribute('version').value
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // don't forget to include the 'getCookie' function
            }
        })
        .done((response) => {
            console.log(response)
                // filterFiles()
                // footer.innerHTML = `<button type="button" class="btn btn-primary" onclick='keepVersion()'>เก็บเวอร์ชัน</button>
                //                     <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ปิด</button>`
            $('#modalVersion').modal('hide')
            window.location = '/segmentation/?project_id=' + getProjectSelect() + '&file_id=' + getFileSelect('id')
        })
        .fail((error) => {
            footer.innerHTML = `<button type="button" class="btn btn-primary" onclick='keepVersion()'>เก็บเวอร์ชัน</button>
                                <button type="button" class="btn btn-secondary" data-bs-dismiss="modal">ปิด</button>`
            console.log(error)
        })
}