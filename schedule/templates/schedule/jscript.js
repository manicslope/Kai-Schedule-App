$(document).ready(function() {
        // JQuery code to be added in here.
        // var value=$.trim($("#group_number").val());
        // if(value.length=0)
        // {
        //     alert('Enter group number');
        // }
        // alert('Enter group number');
        $("#full").click( function(event) {
            var value=$.trim($("#group_number").val());
            if(value.length>0)
            {
                alert('Enter group number');
            }
    });
});
