$('#show').on('click',function(){
    $('#js-join').slideToggle();
});

$('#js-items').on('click',function(e){
    e.preventDefault();
    console.log('test');
    $('.menu-container').slideToggle();
    $('.item-container').slideToggle();
});
