$(document).ready(function(){
    // 切换浏览器窗口时自动更改网页title
    $(window).blur(function () {
        $('title').text('马上回来哟|･ω･｀)');
    });
    $(window).focus(function () {
        $('title').text('码客笔记');
    });
    // 初始化移动端侧栏
    $('.sidenav').sidenav();
    // 初始化tooltip
    $('.tooltipped').tooltip();
    // 初始化固定按钮
    $('#admin-mode').floatingActionButton();
    // 自动修改页脚年份
    let year = new Date().getFullYear();
    $('#footer-year').text(year);
	//为返回顶部元素添加点击事件
	$('#to-top').click(function(){
		//将当前窗口的内容区滚动高度改为0，即顶部
		$('html,body').animate({scrollTop:0},'fast');
		M.toast({html: '回到顶部'});
	});
	// 注销
    $('#logout, #logout-mobile').click(function () {
        $.ajax({
            url: '/api_logout/',
            type: 'POST',
            data: {
                msg: 'logout'
            },
            dataType: 'json',
            success: function (data) {
                if (data.status === 1) {
                    M.toast({html: '注销成功'});
                } else if (data.status === 0) {
                    M.toast({html: '注销过程中出了一点问题'});
                }
                window.location.reload();
            },
            error: function (jpXHR) {
                alert('Status Code: ' + jpXHR.status);
            },
        });
    });
});