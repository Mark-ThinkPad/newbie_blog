$(function () {
    // 编辑器
    let editor = editormd('article-editor', {
        path: '/static/editor.md/lib/',
        height: 800,
        htmlDecode: "style,script,iframe|on*",
        toolbarIcons: 'simple',
        tocm: true,
        tocTitle: 'Content',
        taskList: true,
        tex: true,
        flowChart: true,
        sequenceDiagram: true,
        saveHTMLToTextarea: true,
    });
    editor.on('change', function () {
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
    });
    // 文章上传
    $('#add-article').click(function () {
        // 构建表单数据
        let md_code = $('#editor-input').val();
        let md_file = $('#md-file').val();
        let url_suffix = $('#url_suffix').val();
        let title = $('#title').val();
        let authors = $('#authors').val();
        let tags = $('#tags').val();
        let categories = $('#categories').val();
        let top = $("#top").is(":checked");

        let form_data = new FormData();
        form_data.append('md_code', md_code);
        if (!md_file) {
            form_data.append('md_file', md_file);
        } else {
            let localfile = document.getElementById('md-file');
            form_data.append('md_file', localfile.files[0]);
        }
        form_data.append('url_suffix', url_suffix);
        form_data.append('title', title);
        for (let a of authors) {
            form_data.append('authors', a);
        }
        for (let t of tags) {
            form_data.append('tags', t);
        }
        for (let c of categories) {
            form_data.append('categories', c)
        }
        form_data.append('top', top);


        $.ajax({
            url: '/api_add_article/',
            type: 'POST',
            data: form_data,
            dataType: 'json',
            cache: false,
            contentType: false,
            processData: false,
            success: function (data) {
                if (data.status === 1) {
                    alert(data.message);
                } else if (data.status === 0) {
                    alert(data.message);
                }
            },
            error: function (jpXHR) {
                alert('Status Code: ' + jpXHR.status);
            },
        });
    });
});