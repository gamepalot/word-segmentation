// ! create project check character
$(document).ready(() => {
    let input = document.getElementById('recipient-name')
    input.oninput = function() {
        if (this.value.length == 0) {
            document.getElementById('btn_submit').setAttribute('disabled', '')
        } else if (this.value.length != 0) {
            document.getElementById('btn_submit').removeAttribute('disabled')
        }
    }

    $('#FormUploadFiles').on('submit', function(event) {
        event.preventDefault();
        if ($('input[id=mode-upload-only]:checked').length == 0 && $('input[id=mode-upload-seg]:checked').length == 0) {
            alert('Please select mode !')
            return false
        }
        let input = document.getElementById('file').files.length;
        if (input == 0) {
            alert('Please select file')
        } else {
            // let data = $('#FormUploadFiles').serializeArray()
            let formData = new FormData(this);
            let project_id = document.getElementById('edit_project').value
            formData.append("project_id", project_id)
            if ($('input[id=mode-upload-only]:checked').length == 1) {
                formData.append("mode", 1)
            } else if ($('input[id=mode-upload-seg]:checked').length == 1) {
                formData.append("mode", 0)
            }
            $('#statusUpload').html(`<div class="alert alert-info fade show" role="alert">
                <span class="spinner-grow spinner-grow-sm" role="status" aria-hidden="true"></span>
                Uploading...
            </div>`)
            uploadFiles(formData, this.action)
        }
        event.stopImmediatePropagation();
        return false
    })
})

// ! delete project safety
const delete_project = element => {
    document.getElementById('delete-alert').innerHTML = 'Do you want to delete Project " ' + element.getAttribute('data-name') + ' " ?'
    document.getElementById('delete_project').value = element.getAttribute('value');
}

// ! function on click edit project 
const edit_project = element => {
    let project_id = element.getAttribute('value')
    $("#DialogEdit").on('shown.bs.modal', event => {
        event.preventDefault();
        getInfoProject(project_id)
        event.stopImmediatePropagation();
    })
}

// ! get info project in modal
function getInfoProject(project_id) {
    let tbd = $('#table_files')
    if (tbd.html() != undefined) {
        tbd.remove()
    }
    $.ajax({
            url: "getinfoproject",
            type: "POST",
            dataType: "json",
            async: false,
            data: { 'project_id': project_id },
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
        })
        .done((response) => {
            if (response['id'].length != 0) {
                let tbd = document.getElementById('tbFile')
                t = tbd.createTBody()
                t.id = 'table_files'
                document.getElementById('project_name').innerHTML = `<h6>: ` + response['project_name'] + `</h6>`
                for (let val = 0; val != response['id'].length; val++) {
                    if (response['status'][val] == '1') {
                        response['status'][val] = 'Segmented'
                    } else {
                        response['status'][val] = 'Uploaded'
                    }
                    r = t.insertRow(val)
                    r.innerHTML = `<td>
                                    <div class="custom-control custom-control-nolabel custom-checkbox">
                                    <input type="checkbox" class="custom-control-input" value="` + response['id'][val] + `">
                                    </div>
                                </td>
                                <td>` + (val + 1) + `</td>
                                <td>` + '(' + response['id'][val] + ') ' + response['name'][val] + `</td>
                                <td>` + response['word'][val] + `</td>
                                <td>` + response['date'][val] + `</td>
                                <td>` + response['status'][val] + `</td>
                                <td class="text-center">
                                    <a class="btn text-primary" href="/segmentation/?project_id=` + project_id + `&file_id=` + response['id'][val] + `" type="button" value="` + response['id'][val] + `">
                                        <i class="bi bi-pencil-square"></i> Edit
                                    </a>
                                    <a class="btn text-success" href="/version/?project_id=` + project_id + `&file_id=` + response['id'][val] + `" type="button" value="` + response['id'][val] + `">
                                        <i class="fas fa-history fa-sm"></i> Version (` + response['version'][val] + `)
                                    </a>
                                </td>`
                    r.className = 'align-middle'
                }
            } else {
                document.getElementById('project_name').innerHTML = `<h6>: ` + response['project_name'] + `</h6>`
            }
        })
        .fail((error) => {
            console.log(error)
        })
}

//  ! upload files
const uploadFiles = (data, data_target) => {
    let isPost = 0
    if (isPost == 0) {
        $.ajax({
                url: data_target,
                enctype: 'multipart/form-data',
                type: "POST",
                dataType: "json",
                data: data,
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
                processData: false,
                contentType: false,
                timeout: 800000
            })
            .done((response) => {
                getInfoProject(response['project_id'])
                $('#statusUpload').empty()
                $('#statusUpload').html(`<div class="alert alert-success alert-dismissible fade show" role="alert">
                                                <i class="bi bi-check"></i>
                                                Uploaded successfully
                                                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                            </div>`)
            })
            .fail((err) => {
                console.log(err)
            })
    }
    isPost = 1
}

// ! check all files
const checkAll = () => {
    let tbd = document.getElementById('table_files')
    let checkall = document.getElementById('checkAll')
    let checkboxes = tbd.getElementsByTagName('input')
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked == false) {
            if (checkall.checked == true) {
                checkboxes[i].checked = true
            } else {
                checkboxes[i].checked = false
            }
        } else {
            if (checkall.checked == false) {
                checkboxes[i].checked = false
            } else {
                checkboxes[i].checked = true
            }
        }
    }
}

// ! deleteFiles checked
const deleteFiles = () => {
    let tbd = document.getElementById('table_files')
    let checkboxes = tbd.getElementsByTagName('input')
    let project_id = document.getElementById('edit_project').value
    let file_id = new Array()
    for (let i = 0; i < checkboxes.length; i++) {
        if (checkboxes[i].checked == true) {
            file_id.push(checkboxes[i].value)
        }
    }
    if (file_id.length == 0) {
        alert('Please select file')
    } else {
        $.ajax({
                url: "deletefiles",
                type: "POST",
                dataType: "json",
                data: {
                    'file_id': file_id
                },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                },
            })
            .done((response) => {
                getInfoProject(project_id)
                $('#statusUpload').empty()
                $('#statusUpload').html(`<div class="alert alert-success alert-dismissible fade show" role="alert">
                                            <i class="bi bi-check"></i>
                                            Deleted successfully
                                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                                        </div>`)
            })
            .fail((err) => {
                console.log(err)
            })
    }
}