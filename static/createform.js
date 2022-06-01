
function populate_courses(d) {
    let url = "/jquery/" + $("#subject").val() + "/";
    $.get(url, function(data, status){
        let subjects = data['subject']
        var $el = $("#course");
        $el.empty(); 
        $.each(subjects, function(key,value) {
            if(d==null)
                $el.append($(`<option hidden disabled selected> Course </option>`));

            if(d == value){
                $el.append($(`<option id='${value}' value='${value}' selected> ${value} </option>`));
            }
            else{
                $el.append($(`<option id='${value}' value='${value}' > ${value} </option>`));
            }
        });
    });
};

$('#subject').change(function(){
    populate_courses(null);
});


if($("#file1").attr('src')){
    var extention = $("#file1").attr('src').split('.').pop().trim();
    $(`#file1`).prop('width', "100%");
    if (extention == 'pdf'){
        $(`#file1`).css('min-height', '360px')
        
    }
    else{
        $(`#file1`).css('min-height', '0');
        $(`#file1`).prop('width', "100%");
    }
}

$('#attachment').change(function(){
    files = event.target.files;
    $("#file").prop('src', "");

    for(i=0; i<files.length; i++){
        var extention = files[i].name.split('.').pop().trim();
        console.log(extention);
        src = URL.createObjectURL(files[i]);
        $(`#file${i+1}`).prop('src', src);
        $(`#file${i+1}`).prop('width', "100%");

        if (extention == 'pdf'){
            $(`#file${i+1}`).css('min-height', '360px')
            
        }
        else{
            $(`#file${i+1}`).css('min-height', '0');
            $(`#file${i+1}`).prop('width', "100%");
        }
    }
});