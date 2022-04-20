$("#filterProjects").change(() => {
    let project_id = $("#filterProjects").val()
    $('#original_file').empty()
    $('#segmented_file').empty()
    $('#filterFiles').empty();
    $('#filterFiles').append('<option value="0">Select your file</option>');
    document.getElementById("button-action").className = "container-fluid invisible"

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
                document.getElementById("button-action").className = "container-fluid invisible"
                console.log(error)
            })
    } else {
        document.getElementById("filterFiles").disabled = true
        document.getElementById("button-action").className = "container-fluid invisible"
    }
})

$(document).ready(() => {
    $('#filterProjects').change()
})


const filterFiles = () => {
    let filename = getFileSelect()
    $('#original_file').empty()
    $('#segmented_file').empty()
    document.getElementById("button-action").className = "container-fluid visible"
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
                setWordspace(response)
                let btnVersion = $('#keepVersion')
                btnVersion.text('')
                btnVersion.attr('version', '')
                btnVersion.text('เก็บเป็นเวอร์ชัน ' + response['version'])
                btnVersion.attr('version', response['version'])
                document.getElementById('history').setAttribute('href', '/version/?project_id=' + getProjectSelect() + '&file_id=' + getFileSelect('id'))
            })
            .fail((error) => {
                document.getElementById("button-action").className = "container-fluid invisible"
                console.log(error)
            })
    } else {
        document.getElementById("button-action").className = "container-fluid invisible"
    }
}

$("#filterFiles").change(() => {
    filterFiles()
});