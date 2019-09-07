$(function () {
    // 初始化多选框
    $('select').formSelect();
    // 初始化input计数器
    $('#url_suffix, #title, #new-author, #new-tag, #new-category').characterCounter();
    // 即时添加作者/标签/分类三件套
    // 判空函数
    function isEmpty(input_id, button_id) {
        let input = $(input_id).val();
        if (input !== '') {
            $(button_id).attr('disabled', false);
        } else {
            $(button_id).attr('disabled', true);
        }
    }
    // 输入判空
    $('#new-author').bind('input propertychange', function () {
        isEmpty('#new-author', '#add-author');
    });
    $('#new-tag').bind('input propertychange', function () {
        isEmpty('#new-tag', '#add-tag');
    });
    $('#new-category').bind('input propertychange', function () {
        isEmpty('#new-category', '#add-category');
    });
    // 向后台发送添加请求
    function add_info(msg, input_id, refresh_id) {
        $.ajax({
            url: '/api_add_info/',
            type: 'POST',
            data: {
                msg: msg,
                new: $(input_id).val(),
            },
            dataType: 'json',
            success: function (data) {
                if (data.status === 1) {
                    M.toast({html: data.message});
                    // 添加后自动刷新作者列表
                    $(refresh_id).click();
                } else if (data.status === 0) {
                    M.toast({html: data.message});
                }
            },
            error: function (jpXHR) {
                alert('Status Code: ' + jpXHR.status);
            },
        });
    }
    // 添加新作者/标签/分类
    $('#add-author').click(function () {
        add_info('add_author', '#new-author', '#refresh-authors');
    });
    $('#add-tag').click(function () {
        add_info('add_tag', '#new-tag', '#refresh-tags');
    });
    $('#add-category').click(function () {
        add_info('add_category', '#new-category', '#refresh-categories');
    });
    // 手动刷新作者/标签/分类选项列表
    $('#refresh-authors, #refresh-tags, #refresh-categories').click(function () {
        window.is_leave = false;
        window.location.reload();
    });

    // 输入判空
    // 判空主函数
    function judgeEmpty() {
        let md_code = $('#editor-input').val();
        let md_file = $('#md-file').val();
        let url_suffix = $('#url_suffix').val();
        let title = $('#title').val();
        let authors = $('#authors').val();
        let tags = $('#tags').val();
        let categories = $('#categories').val();

        if (md_code || md_file) {
            if (md_code && md_file) {
                alert('在线编辑器和本地md文档只能选择一个哦~');
                $('#add-article').attr('disabled', true);
            } else if (url_suffix && title && authors.length > 0 && tags.length > 0 && categories.length > 0) {
                $('#add-article').attr('disabled', false);
            } else {
                $('#add-article').attr('disabled', true);
            }
        } else {
            $('#add-article').attr('disabled', true);
        }
    }
    $('#md-file, #url_suffix, #title').bind('input propertychange', function () {
        judgeEmpty()
    });
    $('#authors, #tags, #categories').change(function () {
        judgeEmpty();
    });

    // 检查文件类型
    $('#md-file').change(function () {
        if ( !/\.(md)$/.test(this.files[0].name)) {
            alert('文件类型必须是markdown文档!');
            // 清空文件
            $('#md-file').val('');
            $('#md-file-wrapper').val('');
        }
    });

    // 防止页面意外刷新和关闭页面导致的输入丢失
    $(window).bind('beforeunload', function () {
        // 文章内容
        sessionStorage.article = $('#editor-input').val();
        // 自定义url后缀
        sessionStorage.url_suffix = $('#url_suffix').val();
        // 文章标题
        sessionStorage.title = $('#title').val();
        // 添加新的作者/标签/分类
        sessionStorage.new_author = $('#new-author').val();
        sessionStorage.new_tag = $('#new-tag').val();
        sessionStorage.new_category = $('#new-category').val();
        // sessionStorage和localStorage只支持储存字符串, 对于多选框的值需要稍作处理
        // 实现思路: 数组转对象, 对象字符化
        /**
         * @return {string}
         */
        function ListToString(list_array) {
            let obj = {};
            for (let seq in list_array) {
                obj[seq] = list_array[seq];
            }
            return JSON.stringify(obj);
        }
        // 已选作者/标签/分类
        sessionStorage.authors = ListToString($('#authors').val());
        sessionStorage.tags = ListToString($('#tags').val());
        sessionStorage.categories = ListToString($('#categories').val());
        // 文章置顶选项
        sessionStorage.top = $("#top").is(":checked");

        if (window.is_leave !== false) {
            // Chrome, Safari, Firefox 4+, Opera 12+ , IE 9+
            return '关闭此页面将不会保留已输入的数据';
        }
    });

    // 刷新后恢复缓存数据
    function getStorage() {
        window.is_leave = true;
        // 解析在上方已经字符串化的对象并操作select option
        function restoreOption(select_id, obj_str) {
            let obj = JSON.parse(obj_str);
            for (let key in obj) {
                let selector = 'select' + select_id + ' option[value="' + obj[key] + '"]';
                $(selector).prop('selected', true);
            }
        }
        // 恢复已输入的数据
        // 恢复文章内容
        if (sessionStorage.article) {
            $('#editor-input').val(sessionStorage.article);
            M.toast({html: '已为您自动恢复已输入的文章内容'});
        }
        // 恢复自定义url后缀
        if (sessionStorage.url_suffix) {
            $('#url_suffix').val(sessionStorage.url_suffix);
            M.toast({html: '已为自动您恢复已输入的自定义url后缀'});
        }
        // 恢复文章标题
        if (sessionStorage.title) {
            $('#title').val(sessionStorage.title);
            M.toast({html: '已为自动您恢复已输入的文章标题'});
        }
        // 恢复添加新的作者/标签/分类输入栏
        if (sessionStorage.new_author) {
            $('#new-author').val(sessionStorage.new_author);
            M.toast({html: '已为自动您恢复已输入的新的作者名'});
        }
        if (sessionStorage.new_tag) {
            $('#new-tag').val(sessionStorage.new_tag);
            M.toast({html: '已为自动您恢复已输入的新的标签名'});
        }
        if (sessionStorage.new_category) {
            $('#new-category').val(sessionStorage.new_category);
            M.toast({html: '已为自动您恢复已输入的新的分类名'});
        }
        // 恢复选中的作者/标签/分类
        if (sessionStorage.authors.length > '{}'.length) {
            restoreOption('#authors', sessionStorage.authors);
            M.toast({html: '已为自动您恢复已选择的作者'});
        }
        if (sessionStorage.tags.length > '{}'.length) {
            restoreOption('#tags', sessionStorage.tags);
            M.toast({html: '已为自动您恢复已选择的标签'});
        }
        if (sessionStorage.categories.length > '{}'.length) {
            restoreOption('#categories', sessionStorage.categories);
            M.toast({html: '已为自动您恢复已选择的分类'});
        }
        // 恢复文章置顶设置
        if (sessionStorage.top === 'true') {
            $('#top').prop('checked', true);
            M.toast({html: '已为自动您恢复已选择的文章置顶设置'});
        }
    }
    getStorage();
    // 防止自动填充缓存数据后label无法自动收起
    M.updateTextFields();
});