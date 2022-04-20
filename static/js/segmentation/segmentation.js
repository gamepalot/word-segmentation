var resultText, diff_when_edit, filename, action_index
var check_word, listIndex, listPara, word_selected, para_selected
check_word = false
listIndex = []
listPara = []

const select_word = element => {
    word_selected = listIndex.indexOf(element.getAttribute("nid"))
    para_selected = listPara.indexOf(element.getAttribute("pid"))
    if (listIndex.includes(element.getAttribute("nid"), 0) == false) {
        check_word = false
    } else {
        check_word = true
    }

    if (check_word = !check_word) {
        listIndex.push(element.getAttribute("nid"))
        listPara.push(element.getAttribute("pid"))
        listIndex.sort()
    } else {
        listIndex.splice(word_selected, 1)
        listPara.splice(para_selected, 1)
    }
    setBtnAction()
}

const setBtnAction = () => {
    if (listIndex.length == 1) {
        $('#btn-split').attr('class', 'btn btn-sm btn-outline-danger')
        $('#btn-edit').attr('class', 'btn btn-sm btn-outline-danger')
        $('#btn-merge').attr('class', 'btn btn-sm btn-outline-dark disabled')
    } else if (listIndex.length > 1) {
        $('#btn-merge').attr('class', 'btn btn-sm btn-outline-danger')
        $('#btn-edit').attr('class', 'btn btn-sm btn-outline-dark disabled')
        $('#btn-split').attr('class', 'btn btn-sm btn-outline-dark disabled')
    } else {
        $('#btn-split').attr('class', 'btn btn-sm btn-outline-dark disabled')
        $('#btn-merge').attr('class', 'btn btn-sm btn-outline-dark disabled')
        $('#btn-edit').attr('class', 'btn btn-sm btn-outline-dark disabled')
    }
}

$("#btn-split").on('click', () => {
    $('#inputSplit').empty()
    let word = $("[id='btn-select'][nid='" + listIndex + "']").text()
    $('#inputSplit').text(word)
})

$('#submit-split').on('click', () => {
    arr_id = []
    arr_text = []
    let val = $('#inputSplit').text()
    for (let i = 0; i != listIndex.length; i++) {
        let word = $("[id='btn-select'][nid='" + listIndex[i] + "']")
        arr_id.push(word.attr('wid'))
    }
    arr_text.push(val)
    edit_wordseg('split', arr_id, arr_text)
    $('#modalSplit').modal('hide')
})

$("#btn-edit").on('click', () => {
    $('#inputEdit').text('')
    let word = $("[id='btn-select'][nid='" + listIndex + "']").text()
    $('#inputEdit').text(word)
})

$('#submit-edit').on('click', () => {
    arr_text = []
    arr_id = []
    let val = $('#inputEdit').text()
    for (let i = 0; i != listIndex.length; i++) {
        let word = $("[id='btn-select'][nid='" + listIndex[i] + "']")
        arr_id.push(word.attr('wid'))
    }
    arr_text.push(val)
    edit_wordseg('edit', arr_id, arr_text)
    $('#modalEdit').modal('hide')
})

$('#btn-merge').on('click', () => {
    arr_text = []
    arr_id = []
    for (let i = 0; i != listIndex.length; i++) {
        const word = $("[id='btn-select'][nid='" + listIndex[i] + "']")
        arr_text.push(word.text())
        arr_id.push(word.attr('wid'))
    }
    edit_wordseg('merge', arr_id, arr_text)
})

const reAction = api_url => {
    $("#btnUndo").addClass("disabled")
    $("#btnRedo").addClass("disabled")
    $.ajax({
            url: api_url,
            type: "POST",
            dataType: "json",
            data: {
                'file_encrypt': getFileSelect(),
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // don't forget to include the 'getCookie' function
            }
        })
        .done((response) => {
            setWordspace(response)
        })
        .fail((error) => {
            console.log(error)
        })
}

const edit_wordseg = (api_url, word_id, word_text) => {
    $('#btn-split').attr('class', 'btn btn-sm btn-outline-dark disabled')
    $('#btn-merge').attr('class', 'btn btn-sm btn-outline-dark disabled')
    $('#btn-edit').attr('class', 'btn btn-sm btn-outline-dark disabled')
    $.ajax({
            url: api_url,
            type: "POST",
            dataType: "json",
            data: {
                'file_encrypt': getFileSelect(),
                'id': word_id,
                'text': word_text,
                'action': action_index,
            },
            headers: {
                "X-CSRFToken": getCookie("csrftoken"), // don't forget to include the 'getCookie' function
            }
        })
        .done((response) => {
            api_url = ''
            listPara,
            listIndex = []
            setWordspace(response)
        })
        .fail((error) => {
            console.log(error)
        })
}

const setWordspace = data => {
    listIndex = []
    listPara = []
    $('#original_file').empty()
    $('#segmented_file').empty()
    $('#keepVersion').addClass('disabled')
    for (let i = 0; i != data['segmented_file'].length; i++) {
        $('#segmented_file').append("<button id='btn-select' nid='" + [i] + "' wid='" + data['id'][i] + "' class='btn btn-light btn-sm m-1 rounded border' onclick='select_word(this)'>" + data['segmented_file'][i] + "</button>");
    }
    for (let i = 0; i != data['original_file'].length; i++) {
        $('#original_file').append("<span oid='" + [i] + "'>" + data['original_file'][i] + "</span>");
    }
    if (data['action_count'] == 0) {
        $('#btnUndo').addClass('disabled')
        $('#btnRedo').addClass('disabled')
        $('#keepVersion').addClass('disabled')
    } else {
        if (data['action_index'] == data['action_count']) {
            $('#btnUndo').removeClass('disabled')
            $('#btnRedo').addClass('disabled')
            $('#keepVersion').removeClass('disabled')
        } else if (data['action_index'] < data['action_count'] && data['action_index'] != 0) {
            $('#btnUndo').removeClass('disabled')
            $('#btnRedo').removeClass('disabled')
        } else if (data['action_index'] < data['action_count'] && data['action_index'] == 0) {
            $('#btnUndo').addClass('disabled')
            $('#btnRedo').removeClass('disabled')
        }
    }
    action_index = data['action_index']
    setBtnAction()
    let font = $('input[name="options-font"]:checked').attr('id')
    settingFonts(font)
    hov()
}

function hov() {
    $('button[id^="btn-select"]').mouseover(function() {
        $(this).css({
            'background-color': '#b3e5fc',
            'font-weight': 'bold',
            'color': 'green'
        })
        if ($('#highlight1').prop('checked') == true) {
            $('span[oid="' + $(this).attr('wid') + '"]').css({ 'background-color': '#b3e5fc' })
        }
    })
    $('button[id^="btn-select"]').mouseout(function() {
        if (listIndex.includes($(this).attr('nid')) == true) {
            $(this).css({
                'background-color': '#b3e5fc',
                'font-weight': 'bold',
                'color': 'green'
            })
        } else {
            $(this).css({
                'background-color': 'white',
                'font-weight': 'normal',
                'color': 'black'
            })
        }
        $('span[oid="' + $(this).attr('wid') + '"]').removeAttr('style')
    })
}