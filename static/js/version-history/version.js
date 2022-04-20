$("#filterProjects").change(() => {
    let project_id = $("#filterProjects").val()
    $('#filterFiles').empty();
    $('#filterFiles').append('<option value="0">Select your file</option>');
    if (project_id != 0) {
        $.ajax({
                url: "filterfiles",
                type: "POST",
                data: { 'project_id': project_id },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                }
            })
            .done((response) => {
                for (let val = 0; val != response['id'].length; val++) {
                    let opt = document.createElement('option')
                    opt.innerText = "(" + response["id"][val] + ") " + response["name"][val].replace(/.json/, '')
                    opt.value = response["name_encrypt"][val]
                    opt.setAttribute('data-id', response["id"][val])

                    // ! optional
                    const url = window.location.search
                    const urlParam = new URLSearchParams(url)
                    const file_id = urlParam.get('file_id')
                    if (file_id != null && file_id == response["id"][val]) {
                        opt.selected = true
                    }
                    $('#filterFiles').append(opt)
                    $('#filterFiles').change()
                }
                document.getElementById("filterFiles").disabled = false
            })
            .fail((error) => {
                console.log(error)
            })
    } else {
        document.getElementById("filterFiles").disabled = true
    }
});

$(document).ready(() => {
    $('#filterProjects').change()
})

$("#filterFiles").change(() => {
    let filename = getFileSelect()
    let version = document.getElementById('accordionHistory')
    version.innerHTML = ''
    if (filename != 0) {
        $.ajax({
                url: "selectfiles",
                type: "POST",
                data: { 'file_encrypt': filename },
                headers: {
                    "X-CSRFToken": getCookie("csrftoken"),
                }
            })
            .done((response) => {
                for (var key in Object.keys(response['segmented_file'])) {
                    var current
                    if (parseInt(key) + 1 == response['current']) {
                        current = (parseInt(key) + 1) + '<strong class="text-danger">&nbsp;&nbsp;active</strong>'
                        version.innerHTML += `  <div class="accordion-item shadow-sm m-3">
                                                <h2 class="accordion-header" id="panelsStayOpen-heading` + (parseInt(key) + 1) + `">
                                                    <button class="accordion-button collapsed text-secondary" id="version` + (parseInt(key) + 1) + `" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse` + (parseInt(key) + 1) + `" aria-expanded="false" aria-controls="panelsStayOpen-collapse` + (parseInt(key) + 1) + `">
                                                        Version ` + current + `
                                                    </button>
                                                </h2>
                                                <div id="panelsStayOpen-collapse` + (parseInt(key) + 1) + `" class="multi-collapse collapse" aria-labelledby="panelsStayOpen-heading` + (parseInt(key) + 1) + `">
                                                    <div class="row accordion-body text-secondary">
                                                        <div class="col">
                                                            <div class="text-break text-white bg-secondary rounded-3" id="diff_file_` + (parseInt(key) + 1) + `" style="font-size: 2.5vh; padding: 5px; line-height: 26pt; letter-spacing: 1px">
                                                            ` + (Object.values(response['segmented_file'])[key].join('|')) + `
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row mb-2 mx-2 justify-content-end">
                                                        <div class="col-auto">
                                                            <a onclick="export_file(this)" value="` + (Object.keys(response['segmented_file'])[key]) + `" class="btn btn-primary" target="_blank" >Download</a>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>`
                    } else {
                        current = (parseInt(key) + 1)
                        version.innerHTML += `  <div class="accordion-item shadow-sm m-3">
                                                <h2 class="accordion-header" id="panelsStayOpen-heading` + (parseInt(key) + 1) + `">
                                                    <button class="accordion-button collapsed text-secondary" id="version` + (parseInt(key) + 1) + `" type="button" data-bs-toggle="collapse" data-bs-target="#panelsStayOpen-collapse` + (parseInt(key) + 1) + `" aria-expanded="false" aria-controls="panelsStayOpen-collapse` + (parseInt(key) + 1) + `">
                                                        Version ` + current + `
                                                    </button>
                                                </h2>
                                                <div id="panelsStayOpen-collapse` + (parseInt(key) + 1) + `" class="multi-collapse collapse" aria-labelledby="panelsStayOpen-heading` + (parseInt(key) + 1) + `">
                                                    <div class="row accordion-body text-secondary">
                                                        <div class="col">
                                                            <div class="text-break text-white bg-secondary rounded-3" id="diff_file_` + (parseInt(key) + 1) + `" style="font-size: 2.5vh; padding: 5px; line-height: 26pt; letter-spacing: 1px">
                                                            ` + (Object.values(response['segmented_file'])[key].join('|')) + `
                                                            </div>
                                                        </div>
                                                    </div>
                                                    <div class="row mb-2 mx-2">
                                                        <div class="col-auto me-auto">
                                                            <a onclick="use_version(this)" value="` + (parseInt(key) + 1) + `" class="btn btn-primary">Use this version</a>
                                                        </div>
                                                        <div class="col-auto">
                                                            <a onclick="export_file(this)" value="` + (Object.keys(response['segmented_file'])[key]) + `" class="btn btn-primary" target="_blank" >Download</a>
                                                        </div>
                                                    </div>
                                                </div>
                                            </div>`
                    }

                }
                document.getElementById('backEdit').setAttribute('href', '/segmentation/?project_id=' + getProjectSelect() + '&file_id=' + getFileSelect('id'))
            })
            .fail((error) => {
                console.log(error)
            })
    } else {
        version.innerHTML = ''
    }
});


function export_file(element) {
    $.ajax({
            url: "export",
            type: "POST",
            data: { 'file_encrypt': element.getAttribute('value') },
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            },
            responseType: 'blob'
        })
        .done((response) => {
            let a = document.createElement('a')
            a.setAttribute('href', '../static/export/' + response['filename']);
            a.setAttribute('download', '')
            document.body.appendChild(a);
            a.click();
            a.remove();
        })
        .fail((error) => {
            console.log(error)
        })
}

function use_version(element) {
    let selected = document.getElementById('filterFiles')
    let filename = selected.options[selected.selectedIndex].value
    $.ajax({
            url: "use_version",
            type: "POST",
            data: {
                'version': element.getAttribute('value'),
                'file_encrypt': filename
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken"),
            }
        })
        .done((response) => {
            window.location.reload()
        })
        .fail((error) => {
            console.log(error)
        })
}