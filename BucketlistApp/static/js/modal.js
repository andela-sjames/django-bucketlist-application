$(function(){
  $( "#editme" ).hide( "fast" )


$( ".bucket-item" ).find('.edit').click(function() {
  var parent = $(this).parentsUntil('.bucket-item').parent();
  //console.log(parent.children()[1]);
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


