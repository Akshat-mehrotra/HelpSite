var extension = $('#attachment').attr('data').split('.').pop();
switch (extension) {
    case 'pdf':
        $('#attachment').css('height', '100%');
        break;
}

function change_solved(id, csrf_token){
    let url = `/jquery/solved/${id}/`;

    $.post(url, 
    {
        "id": id,
        csrfmiddlewaretoken: csrf_token,
    },
    function(data, status){
        $(`#${id}_checkbtn`).removeClass(['btn-success', 'btn-danger']);

        if(data['solved'] == true){
            $(`#${id}_checkbtn`).html("Not Solved?").addClass('btn-success'); 
        }
        else{
            $(`#${id}_checkbtn`).html("Solved?").addClass('btn-danger'); 
        }
    });
};