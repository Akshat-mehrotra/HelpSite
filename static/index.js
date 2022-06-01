$(".solved").click(function(){

    var id = this.name;
    let url = `/jquery/solved/${id}/`;

    $.post(url, 
    {
        "id": id,
        csrfmiddlewaretoken: getCookie('csrftoken'),
    },
    function(data, status){
        $("#" + id).removeClass(['bg-solved', 'bg-unsolved']);
        if(data['solved'] == true){
            $("#"+ id).addClass('bg-solved');
            $(`#${id}_checkbtn`).html("Not Solved?"); 

        }
        else{
            $("#" + id).addClass('bg-unsolved');
            $(`#${id}_checkbtn`).html("Solved?"); 
        }
    }
)});


function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
}

$('.question_row').click(function (event) { 
    var parent_qr = event.target.closest('.question_row');
    var id = parent_qr.id;

    //console.log(`clicked on parent ${parent_qr.id}`);
    if(event.target.id == `${id}_checkbtn` || $(event.target).closest(`#${id}_checkbtn`).length)
      return; 
      
    url = `/question/${id}/`;
    window.location.href = url;
});


$('.form-check-input').click(function() {
    if($('#by_subject').is(':checked')) {
        $('.collapse[id="subjects_collapse"]').collapse('show') 
        $('#subject').attr("disabled", false);
    }
    else{
        $('#subject').attr("disabled", true);

        $('.collapse[id="subjects_collapse"]').collapse('hide') 
    }
 });