$(function () {
    // 初始化input的计数器
    $('input#username, input#password').characterCounter();
    // 初始化消息对话框
    $('#login-modal').modal({dismissible: false, onOpenEnd: function () {
            $(document).keydown(function (event) {
                if (event.keyCode === 13) {
                    $('#message-confirm').click();
                }
            });
        },
    });
    // 前端判断输入是否为空, 为空时禁用按钮
    $('input#username, input#password').bind('input propertychange', function (event) {
        let username = $('#username').val();
        let password = $('#password').val();
        if (username && password) {
            $('#login-button').attr('disabled', false);
        } else {
            $('#login-button').attr('disabled', true);
        }
    });
    // 回车触发按钮点击事件
    $('#username, #password').keydown(function (event) {
        if (event.keyCode === 13) {
            if ($('#login-button').prop('disabled') === true) {
                M.toast({html: '请输入完整的用户名和密码'})
            } else {
                $('#login-button').click();
            }
        }
    });
    // 点击登录按钮后向后端API发送数据
    $('#login-button').click(function () {
        $.ajax({
            url: '/api_login/',
            type: 'POST',
            data: {
                username: $('#username').val(),
                password: $('#password').val()
            },
            dataType: 'json',
            success: function (data) {
                if (data.status === 1) {
                    $('#message-title').text('登陆成功');
                    let username = $('#username').val();
                    let date = new Date();
                    let message = '管理员 ' + username + ' 您好' + ', 现在是 ' + date.toLocaleString();
                    $('#message-words').text(message);
                    $('#message-confirm').text('确认并返回上一页');
                    $('#message-confirm').click(function () {
                        // 返回上一页并刷新
                        window.location.href=document.referrer||host + '';
                    });
                } else if (data.status === 0) {
                    $('#message-title').text('登陆失败');
                    $('#message-words').text('请问您是管理员吗? 不是就别在这儿瞎忙活了');
                    $('#message-confirm').text('确认');
                    $('#message-confirm').click(function () {
                        window.location.reload();
                    });
                }
                $('#login-modal').modal('open');
            },
            error: function (jpXHR) {
                alert('Status Code: ' + jpXHR.status);
            },
        });
    });
});