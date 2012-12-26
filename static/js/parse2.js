$(function(){
    $(document).scroll(function(){
	$('.title-cells').css('top', $(this).scrollTop());
    });

    $('.cell').live('mouseover', function(){
	var id = $(this).attr('id');
	id = (/[^-]-(\d+)/.exec(id) || [null, null])[1];
	var unicodeId = id;
	if(id % 2 == 1)
	    unicodeId =  id-1;
	$('#data-'+id+',#ascii-'+id+',#unicode-'+unicodeId).addClass('cell-hover');
    }).live('mouseout', function(){
	var id = $(this).attr('id');
	id = (/[^-]-(\d+)/.exec(id) || [null, null])[1];
	var unicodeId = id;
	if(id % 2 == 1)
	    unicodeId =  id-1;
	$('#data-'+id+',#ascii-'+id+',#unicode-'+unicodeId).removeClass('cell-hover');
    });

    $.ajax({
	url: '/load/0',
	type: 'GET',
	dataType: 'json'
    }).done(function(d){
	$('#digit').append(d.digit);
	$('#ascii').append(d.ascii);
	$('#unicode').append(d.unicode);
    });
});
