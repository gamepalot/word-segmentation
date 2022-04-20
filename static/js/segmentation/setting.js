$('input[name^="options-font"]').change(function() {
    // console.log($(this).attr('id'))
    let font = $(this).attr('id')
    settingFonts(font)
})

const settingFonts = font => {
    if (font == 'font1') {
        $('#original_file').css({
            'line-height': '26pt',
            'font-size': '1rem',
            'letter-spacing': '1px'
        })
        $('button[id^="btn-select"]').css({
            'line-height': '15pt',
            'font-size': '1rem',
            'letter-spacing': '1px'
        })
        $('#segmented_file').removeAttr('style')
    } else if (font == 'font2') {
        $('#original_file').css({
            'line-height': '26pt',
            'font-size': '1.25rem',
            'letter-spacing': '1px'
        })
        $('button[id^="btn-select"]').css({
            'line-height': '15pt',
            'font-size': '1.25rem',
            'letter-spacing': '1px'
        })
        $('#segmented_file').removeAttr('style')
    } else if (font == 'font3') {
        $('#original_file').css({
            'line-height': '30pt',
            'font-size': '1.5rem',
            'letter-spacing': '1px'
        })
        $('button[id^="btn-select"]').css({
            'line-height': '15pt',
            'font-size': '1.5rem',
            'letter-spacing': '1px'
        })
        $('#segmented_file').css({
            'line-height': '30pt'
        })
    }
}