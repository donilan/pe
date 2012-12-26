window.CURRENT_OFFSET = 0;
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
	$('#digit-'+id+',#ascii-'+id+',#unicode-'+unicodeId).
	    addClass('cell-hover');

    }).live('mouseout', function(){
	var id = $(this).attr('id');
	id = (/[^-]-(\d+)/.exec(id) || [null, null])[1];
	var unicodeId = id;
	if(id % 2 == 1)
	    unicodeId =  id-1;
	$('#digit-'+id+',#ascii-'+id+',#unicode-'+unicodeId).
	    removeClass('cell-hover');
    });
    loadDataFirst();
    $(window).scroll(function(){
	var _val = ($(document).height() - $(window).height());
	if($(window).scrollTop() ==  _val){
	    loadData();
	}
    });

});

function loadDataFirst() {
    var _val = $(document).height() - $(window)[0].outerHeight;
    loadData(function(d, len){
	console.log(d);
	if(_val < 1 && d.digit != '') {
	    loadDataFirst();
	}
    });
}

function loadData(callback) {
    var length = 1024;
    window.CURRENT_OFFSET = window.CURRENT_OFFSET+length;
    $.ajax({
	url: '/load/' + (window.CURRENT_OFFSET-length)+'/'+length,
	type: 'GET',
	dataType: 'json'
    }).done(function(d){
	$('#digit').append(d.digit);
	$('#ascii').append(d.ascii);
	$('#unicode').append(d.unicode);
	$('#position').append(d.position);
	callback && callback(d, length);
    });
}
