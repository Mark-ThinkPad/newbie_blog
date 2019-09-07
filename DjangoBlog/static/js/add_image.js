$(function () {
    $('#reset-button').click(function () {
        $('#images-preview').empty();
        $('#add-images').attr('disabled', true);
    });
    $('#images').change(function () {
        if ($('#images').val()) {
            $('#reset-button, #add-images').attr('disabled', false);
        } else {
            $('#reset-button, #add-images').attr('disabled', true);
        }

        $('#images-preview').empty();

        let preview = document.querySelector('#images-preview');
        let files   = document.querySelector('input[type=file]').files;

        function readAndPreview(file) {

            // 确保 `file.name` 符合我们要求的扩展名
            if ( /\.(jpe?g|png|gif|ico)$/i.test(file.name) ) {
                let reader = new FileReader();

                reader.addEventListener("load", function () {
                    let image = new Image();
                    image.className = 'materialboxed';
                    image.title = file.name;
                    image.src = this.result;
                    preview.appendChild( image );
                }, false);

                reader.readAsDataURL(file);
            } else {
                alert('图片格式不在验证范围内(jpg, jpeg, png, gif, ico)');
                window.location.reload();
            }
        }

        if (files) {
            [].forEach.call(files, readAndPreview);
        }
    });
    $('#add-images').click(function () {
        let files = document.querySelector('input[type=file]').files;
        let form_data = new FormData();

        for (let i = 0; i < files.length; i++) {
            form_data.append("images", files[i]);
        }

        $.ajax({
            url: '/api_add_images/',
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