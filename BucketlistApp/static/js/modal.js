$(function(){
  $( "#editme" ).hide( "fast" )


$( ".bucket-item" ).find('.edit').click(function() {
  var parent = $(this).parentsUntil('.bucket-item').parent();
  //console.log(parent.children()[1]);
  parent.find('.edit-form').slideToggle('fast');
});
    

});

