$('#Exam').on('show.bs.modal', (e)=>{
    var data = $(e.relatedTarget).data('recordPath')
    $('.btn-confirm').click(function() {
        window.location.replace(data)
    })
})