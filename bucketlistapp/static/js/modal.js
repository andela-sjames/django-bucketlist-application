var deleteBuckelist = {
   config: {
       button: ".delete",
   },
   init: function(config) {
       if (config && typeof config == 'object') $.extend(deleteBuckelist.config, config);
       $("body").on('click', deleteBuckelist.config.button, function(e) {
           e.preventDefault();
           if (!confirm("Are you sure you want to delete this bucketlist")) return;
           deleteBuckelist.sendAction($(this));
       })
   },
   sendAction: function(_this) {
       $.ajax({
           url: _this.closest("a").attr("href"),
           type: "GET",
           success: function(data){
            location.reload();
           },
           error: function(res) {
               console.log(res.responseText);
           }
       });
   }
};


$(document).ready(function(){
    deleteBuckelist.init({
        button: '.glyphicon-trash'
    })
  $.material.init();


    $('#tool').tooltip();
    $( "#editme" ).hide( "fast" )

    $( ".bucket-item" ).find('.edit').click(function() {
          var parent = $(this).parentsUntil('.bucket-item').parent();

          parent.find('.edit-form').slideToggle('fast');
    });

    $('#additemmodal').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget) // Button that triggered the modal
          var bucketlistId = button.data('bucketlistId')
          var modalForm = $(this).find('form')
          var modalFormAction = "/bucketlist/" + bucketlistId + "/items/"

          modalForm.attr( "action", modalFormAction );
    })

    $('#editmodal').on('show.bs.modal', function (event) {
          var button = $(event.relatedTarget) // Button that triggered the modal
          var bucketlistId = button.data('bucketlistId')
          var modalForm = $(this).find('form')
          var modalFormAction = "/bucketlist/" + bucketlistId + "/"

          modalForm.attr( "action", modalFormAction );
    })

});


