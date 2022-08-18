$('#show').on('click',function(){
    $('#js-join').slideToggle();
});

$('#js-items').on('click',function(e){
    e.preventDefault();
    $('.menu-container').slideToggle();
    $('.item-container').slideToggle();
});
$('#js-sales').on('click',function(e){
    e.preventDefault();
    $('.sales-container').slideToggle();
    $('.item-container').slideToggle();
});

